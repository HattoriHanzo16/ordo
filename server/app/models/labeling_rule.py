from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime

from app.models.database import Base


class LabelingRule(Base):
    """Model for storing user-defined labeling rules for automatic meeting categorization"""
    __tablename__ = "labeling_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    label_name = Column(String(100), nullable=False)  # e.g., "Effective", "Boring", "Too Long"
    label_color = Column(String(7), nullable=False, default="#3B82F6")  # Hex color code
    rule_description = Column(Text, nullable=False)  # Rule criteria for AI to follow
    is_active = Column(Boolean, default=True)  # Can be disabled without deletion
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 