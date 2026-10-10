from datetime import date
from collections import defaultdict
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.food_item import FoodItem
from app.models.inventory import Inventory
from app.models.user import User
from app.models.storage import StorageCondition
from app.models.shelf_life import ShelfLifePrediction
from app.models.analysis import AnalysisResult
from app.schemas.stats import (
    DashboardStatsResponse,
    FacilityTelemetryStats,
    ShelfLifeAnalyticsStats,
    FreshnessAnalyticsStats,
    SpoilageAlertItem
)
from app.core.security import get_current_active_user
from app.routers.inventory import compute_inventory_status

router = APIRouter(prefix="/api/stats", tags=["Platform Dashboard Statistics"])

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    total_food_items = db.query(FoodItem).count()
    all_inventory = db.query(Inventory).options(joinedload(Inventory.food_item)).all()
    
    active_batches = len(all_inventory)
    expiring_soon = 0
    expired_items = 0
    fresh_items = 0
    near_spoilage = 0

    category_counts = defaultdict(int)
    temperatures: List[float] = []
    humidities: List[float] = []
    temp_alerts = 0
    hum_alerts = 0
    spoilage_alerts: List[Dict[str, Any]] = []

    remaining_days_list: List[int] = []

    for inv in all_inventory:
        if inv.food_item:
            category_counts[inv.food_item.category] += 1

        days_left, status_label = compute_inventory_status(inv)
        remaining_days_list.append(max(0, days_left))

        if status_label == "Spoiled":
            expired_items += 1
            spoilage_alerts.append({
                "id": f"spoil-{inv.id}",
                "type": "SPOILED",
                "severity": "critical",
                "title": f"Batch #{inv.batch_number} is Spoiled / Expired",
                "message": f"{inv.food_item.name if inv.food_item else 'Item'} exceeded expiration date ({inv.expiry_date}). Quarantined for disposal.",
                "batch_number": inv.batch_number,
                "item_name": inv.food_item.name if inv.food_item else "Unknown",
                "created_at": inv.created_at.isoformat()
            })
        elif status_label == "Near Spoilage":
            near_spoilage += 1
            expiring_soon += 1
            spoilage_alerts.append({
                "id": f"near-{inv.id}",
                "type": "EXPIRING_SOON",
                "severity": "warning",
                "title": f"Batch #{inv.batch_number} Nearing Expiration",
                "message": f"{inv.food_item.name if inv.food_item else 'Item'} has {days_left} days remaining. Prioritize dispatch or markdown.",
                "batch_number": inv.batch_number,
                "item_name": inv.food_item.name if inv.food_item else "Unknown",
                "created_at": inv.created_at.isoformat()
            })
        elif status_label in ["Acceptable", "Good"]:
            if days_left <= 3:
                expiring_soon += 1
                spoilage_alerts.append({
                    "id": f"exp-{inv.id}",
                    "type": "EXPIRING_SOON",
                    "severity": "warning",
                    "title": f"Batch #{inv.batch_number} Expiring Soon",
                    "message": f"Only {days_left} days left until expiry ({inv.expiry_date}).",
                    "batch_number": inv.batch_number,
                    "item_name": inv.food_item.name if inv.food_item else "Unknown",
                    "created_at": inv.created_at.isoformat()
                })
        elif status_label == "Fresh":
            fresh_items += 1

        # Real telemetry aggregation
        curr_temp = inv.storage_temperature
        curr_hum = inv.storage_humidity
        temperatures.append(curr_temp)
        humidities.append(curr_hum)

        # Environmental threshold checks
        if curr_temp > 8.0:
            temp_alerts += 1
            spoilage_alerts.append({
                "id": f"temp-{inv.id}",
                "type": "THERMAL_ABUSE",
                "severity": "warning",
                "title": f"Thermal Breach on Batch #{inv.batch_number}",
                "message": f"Storage temperature of {curr_temp}°C exceeds safety ceiling of 8.0°C.",
                "batch_number": inv.batch_number,
                "item_name": inv.food_item.name if inv.food_item else "Unknown",
                "created_at": inv.created_at.isoformat()
            })
        elif curr_temp < 0.0:
            temp_alerts += 1

        if curr_hum > 92.0 or curr_hum < 50.0:
            hum_alerts += 1

    # Format recent activity log
    recent_batches = db.query(Inventory).options(joinedload(Inventory.food_item)).order_by(Inventory.created_at.desc()).limit(5).all()
    recent_activity = []
    for r in recent_batches:
        days_left, status_label = compute_inventory_status(r)
        recent_activity.append({
            "id": r.id,
            "batch_number": r.batch_number,
            "item_name": r.food_item.name if r.food_item else "Unknown Item",
            "category": r.food_item.category if r.food_item else "Uncategorized",
            "quantity": f"{r.quantity} {r.unit}",
            "expiry_date": str(r.expiry_date),
            "status": status_label,
            "created_at": r.created_at.isoformat()
        })

    # 1. Real Facility Telemetry Stats
    avg_temp = round(sum(temperatures) / len(temperatures), 1) if temperatures else 4.0
    avg_hum = round(sum(humidities) / len(humidities), 1) if humidities else 85.0
    facility_telemetry = FacilityTelemetryStats(
        avg_temperature=avg_temp,
        avg_humidity=avg_hum,
        temp_alert_count=temp_alerts,
        humidity_alert_count=hum_alerts,
        active_monitored_batches=active_batches
    )

    # 2. Real Shelf-Life Risk Analytics
    all_predictions = db.query(ShelfLifePrediction).all()
    risk_dist = {"CRITICAL": 0, "HIGH RISK": 0, "MEDIUM RISK": 0, "LOW RISK": 0}
    pred_remaining_days: List[int] = []

    # Map latest prediction per inventory
    latest_pred_per_inv = {}
    for p in all_predictions:
        if p.inventory_id not in latest_pred_per_inv or p.created_at > latest_pred_per_inv[p.inventory_id].created_at:
            latest_pred_per_inv[p.inventory_id] = p

    for inv in all_inventory:
        if inv.id in latest_pred_per_inv:
            pred = latest_pred_per_inv[inv.id]
            r_level = pred.risk_level if pred.risk_level in risk_dist else "MEDIUM RISK"
            risk_dist[r_level] += 1
            pred_remaining_days.append(pred.estimated_remaining_days)
        else:
            # Baseline estimation from inventory days_left
            d_left, st = compute_inventory_status(inv)
            if st == "Spoiled" or d_left <= 1:
                risk_dist["CRITICAL"] += 1
            elif st == "Near Spoilage" or d_left <= 3:
                risk_dist["HIGH RISK"] += 1
            elif d_left <= 7:
                risk_dist["MEDIUM RISK"] += 1
            else:
                risk_dist["LOW RISK"] += 1
            pred_remaining_days.append(max(0, d_left))

    avg_remaining = round(sum(pred_remaining_days) / len(pred_remaining_days), 1) if pred_remaining_days else 0.0
    shelf_life_analytics = ShelfLifeAnalyticsStats(
        risk_distribution=risk_dist,
        avg_remaining_days=avg_remaining,
        total_predictions=len(all_predictions)
    )

    # 3. Real Freshness CV Analytics
    all_analyses = db.query(AnalysisResult).all()
    total_analyses = len(all_analyses)
    avg_score = round(sum(a.freshness_score for a in all_analyses) / total_analyses, 1) if total_analyses > 0 else 0.0
    class_dist = defaultdict(int)
    for a in all_analyses:
        class_dist[a.predicted_category] += 1

    freshness_analytics = FreshnessAnalyticsStats(
        total_analyses=total_analyses,
        avg_freshness_score=avg_score,
        classification_distribution=dict(class_dist)
    )

    return {
        "total_food_items": total_food_items,
        "active_batches": active_batches,
        "expiring_soon": expiring_soon,
        "expired_items": expired_items,
        "fresh_items": fresh_items,
        "near_spoilage": near_spoilage,
        "category_distribution": dict(category_counts),
        "recent_activity": recent_activity,
        "facility_telemetry": facility_telemetry,
        "shelf_life_analytics": shelf_life_analytics,
        "freshness_analytics": freshness_analytics,
        "spoilage_alerts": spoilage_alerts[:15]
    }
