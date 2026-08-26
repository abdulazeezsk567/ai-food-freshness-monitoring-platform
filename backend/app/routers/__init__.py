from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.food_items import router as food_items_router
from app.routers.inventory import router as inventory_router
from app.routers.stats import router as stats_router

__all__ = ["auth_router", "users_router", "food_items_router", "inventory_router", "stats_router"]
