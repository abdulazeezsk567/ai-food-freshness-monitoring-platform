from pydantic import BaseModel
from typing import List, Dict, Any

class DashboardStatsResponse(BaseModel):
    total_food_items: int
    active_batches: int
    expiring_soon: int
    expired_items: int
    fresh_items: int
    near_spoilage: int
    category_distribution: Dict[str, int]
    recent_activity: List[Dict[str, Any]]
