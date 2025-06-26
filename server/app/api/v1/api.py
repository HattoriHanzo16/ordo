from fastapi import APIRouter

from app.api.v1.endpoints import upload, health, recordings, search, labeling

api_router = APIRouter()

# Include health endpoints at root level
api_router.include_router(health.router, tags=["health"])

# Include upload endpoints
api_router.include_router(upload.router, tags=["upload"])

# Include recordings endpoints
api_router.include_router(recordings.router, tags=["recordings"])

# Include search endpoints
api_router.include_router(search.router, tags=["search"])

# Include labeling endpoints
api_router.include_router(labeling.router, prefix="/labeling", tags=["labeling"]) 