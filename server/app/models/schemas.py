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


class AppliedLabel(BaseModel):
    """Schema for an applied label on a recording"""
    label_name: str
    label_color: str
    confidence: Optional[float] = None  # AI confidence in applying this label


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
    labels: Optional[List[AppliedLabel]] = None
    
    processing_status: str
    processing_error: Optional[str]
    duration: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LabelingRuleCreate(BaseModel):
    """Schema for creating a new labeling rule"""
    label_name: str = Field(..., min_length=1, max_length=100)
    label_color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$')  # Hex color validation
    rule_description: str = Field(..., min_length=10)
    is_active: bool = True


class LabelingRuleUpdate(BaseModel):
    """Schema for updating a labeling rule"""
    label_name: Optional[str] = Field(None, min_length=1, max_length=100)
    label_color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    rule_description: Optional[str] = Field(None, min_length=10)
    is_active: Optional[bool] = None


class LabelingRuleResponse(BaseModel):
    """Schema for labeling rule response"""
    id: int
    label_name: str
    label_color: str
    rule_description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RecordingListResponse(BaseModel):
    """Recording list response model"""
    recordings: List[RecordingResponse]
    total: int 