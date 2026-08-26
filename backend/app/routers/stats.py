from datetime import date
from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.food_item import FoodItem
from app.models.inventory import Inventory
from app.models.user import User
from app.schemas.stats import DashboardStatsResponse
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
    for inv in all_inventory:
        if inv.food_item:
            category_counts[inv.food_item.category] += 1

        days_left, status_label = compute_inventory_status(inv)
        if status_label == "Spoiled":
            expired_items += 1
        elif status_label == "Near Spoilage":
            near_spoilage += 1
            expiring_soon += 1
        elif status_label in ["Acceptable", "Good"]:
            if days_left <= 3:
                expiring_soon += 1
        elif status_label == "Fresh":
            fresh_items += 1

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

    return {
        "total_food_items": total_food_items,
        "active_batches": active_batches,
        "expiring_soon": expiring_soon,
        "expired_items": expired_items,
        "fresh_items": fresh_items,
        "near_spoilage": near_spoilage,
        "category_distribution": dict(category_counts),
        "recent_activity": recent_activity
    }
