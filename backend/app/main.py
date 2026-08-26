from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database.session import Base, engine, SessionLocal
from app.routers import auth_router, users_router, food_items_router, inventory_router, stats_router
from app.services.seed import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)
    # Seed initial demo data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Food Freshness Monitoring Platform - Milestone 1 REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(food_items_router)
app.include_router(inventory_router)
app.include_router(stats_router)

@app.get("/", tags=["System Overview"])
def root():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
