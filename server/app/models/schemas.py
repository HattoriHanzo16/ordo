from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FileUploadResponse(BaseModel):
    """Response model for successful file upload"""
    message: str
    file_details: "FileDetails"


class MultipleFileUploadResponse(BaseModel):
    """Response model for multiple file upload"""
    message: str
    successful_uploads: int
    failed_uploads: int
    file_details: List["FileDetails"]
    failed_files: List[dict]


class FileDetails(BaseModel):
    """File details returned after successful upload"""
    original_filename: str
    storage_path: str
    public_url: str
    file_size: int
    content_type: Optional[str]
    upload_timestamp: str


class HealthResponse(BaseModel):
    """Health check response model"""
    api: str = "healthy"
    storage: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    error_code: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class BasicResponse(BaseModel):
    """Basic API response model"""
    message: str
    status: str


class RecordingResponse(BaseModel):
    """Recording response model"""
    id: int
    original_filename: str
    media_url: str
    storage_path: str
    file_size: Optional[int]
    content_type: Optional[str]
    transcript: Optional[str]
    transcript_with_speakers: Optional[str]
    processing_status: str
    processing_error: Optional[str]
    duration: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RecordingListResponse(BaseModel):
    """Recording list response model"""
    recordings: List[RecordingResponse]
    total: int 