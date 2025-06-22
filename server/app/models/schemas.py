from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class FileDetails(BaseModel):
    """File details returned after successful upload"""
    original_filename: str
    storage_path: str
    public_url: str
    file_size: int
    content_type: Optional[str]
    upload_timestamp: str


class FileUploadResponse(BaseModel):
    """Response model for successful file upload"""
    message: str
    file_details: FileDetails


class MultipleFileUploadResponse(BaseModel):
    """Response model for multiple file upload"""
    message: str
    successful_uploads: int
    failed_uploads: int
    file_details: List[FileDetails]
    failed_files: List[dict]


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


class ActionItemResponse(BaseModel):
    """Action item model"""
    description: str
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None


class DecisionResponse(BaseModel):
    """Decision model"""
    description: str
    owner: Optional[str] = None
    context: Optional[str] = None
    impact: Optional[str] = None


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
    
    # Analysis fields
    summary: Optional[str]
    action_items: Optional[List[Dict[str, Any]]]
    decisions: Optional[List[Dict[str, Any]]]
    visual_summary_url: Optional[str]
    
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