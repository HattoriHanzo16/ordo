from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.orm import relationship
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
    
    # Analysis fields
    summary = Column(Text)  # Meeting/recording summary
    action_items = Column(JSON)  # List of action items with details
    decisions = Column(JSON)  # List of decisions with owners
    visual_summary_url = Column(String)  # DALL·E 3 generated visual summary
    labels = Column(JSON)  # List of applied labels based on rules
    
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    processing_error = Column(Text)
    duration = Column(Float)  # Duration in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to text chunks (using lazy loading to avoid circular imports)
    # Embeddings functionality removed - using simple text search instead 