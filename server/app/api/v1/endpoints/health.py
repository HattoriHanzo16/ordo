from fastapi import APIRouter
from datetime import datetime
from typing import Any

from app.models.schemas import HealthResponse, BasicResponse
from app.services.storage_service import storage_service

router = APIRouter()


@router.get("/", response_model=BasicResponse)
async def root() -> Any:
    """Basic health check endpoint"""
    return BasicResponse(
        message="File Upload API is running",
        status="healthy"
    )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> Any:
    """Detailed health check including Supabase Storage connectivity"""
    bucket_info = storage_service.get_bucket_info()
    
    return HealthResponse(
        api="healthy",
        storage=bucket_info["status"],
        timestamp=datetime.now().isoformat()
    ) 