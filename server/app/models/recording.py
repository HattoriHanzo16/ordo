from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime

from app.models.database import Base


class Recording(Base):
    """Recording model for storing uploaded files and transcripts"""
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    media_url = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    file_size = Column(Integer)
    content_type = Column(String)
    transcript = Column(Text)
    transcript_with_speakers = Column(Text)  # For diarized transcript
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    processing_error = Column(Text)
    duration = Column(Float)  # Duration in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 