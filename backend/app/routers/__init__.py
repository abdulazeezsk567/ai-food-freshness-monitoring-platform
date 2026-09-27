from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.food_items import router as food_items_router
from app.routers.inventory import router as inventory_router
from app.routers.stats import router as stats_router
from app.routers.freshness import router as freshness_router
from app.routers.storage import router as storage_router
from app.routers.shelf_life import router as shelf_life_router

__all__ = [
    "auth_router",
    "users_router",
    "food_items_router",
    "inventory_router",
    "stats_router",
    "freshness_router",
    "storage_router",
    "shelf_life_router"
]
