from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class FacilityTelemetryStats(BaseModel):
    avg_temperature: float
    avg_humidity: float
    temp_alert_count: int
    humidity_alert_count: int
    active_monitored_batches: int

class ShelfLifeAnalyticsStats(BaseModel):
    risk_distribution: Dict[str, int]
    avg_remaining_days: float
    total_predictions: int

class FreshnessAnalyticsStats(BaseModel):
    total_analyses: int
    avg_freshness_score: float
    classification_distribution: Dict[str, int]

class SpoilageAlertItem(BaseModel):
    id: str
    type: str  # "CRITICAL_RISK", "EXPIRING_SOON", "THERMAL_ABUSE", "SPOILED"
    severity: str  # "critical", "warning", "info"
    title: str
    message: str
    batch_number: str
    item_name: str
    created_at: str

class DashboardStatsResponse(BaseModel):
    total_food_items: int
    active_batches: int
    expiring_soon: int
    expired_items: int
    fresh_items: int
    near_spoilage: int
    category_distribution: Dict[str, int]
    recent_activity: List[Dict[str, Any]]
    facility_telemetry: Optional[FacilityTelemetryStats] = None
    shelf_life_analytics: Optional[ShelfLifeAnalyticsStats] = None
    freshness_analytics: Optional[FreshnessAnalyticsStats] = None
    spoilage_alerts: Optional[List[SpoilageAlertItem]] = None
