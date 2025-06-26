from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.models.recording import Recording
from app.models.database import SessionLocal

logger = logging.getLogger(__name__)


class RecordingService:
    """Service for handling Recording database operations"""
    
    def create_recording(
        self,
        original_filename: str,
        media_url: str,
        storage_path: str,
        file_size: Optional[int] = None,
        content_type: Optional[str] = None
    ) -> Recording:
        """Create a new recording entry"""
        logger.info(f"📝 Creating new recording entry: {original_filename}")
        logger.debug(f"🔗 Media URL: {media_url}")
        logger.debug(f"📁 Storage path: {storage_path}")
        
        db = SessionLocal()
        try:
            recording = Recording(
                original_filename=original_filename,
                media_url=media_url,
                storage_path=storage_path,
                file_size=file_size,
                content_type=content_type,
                processing_status="pending"
            )
            db.add(recording)
            db.commit()
            db.refresh(recording)
            
            logger.info(f"✅ Recording created with ID: {recording.id}")
            return recording
        except Exception as e:
            logger.error(f"❌ Failed to create recording: {e}")
            db.rollback()
            raise e
        finally:
            db.close()
    
    def update_transcription(
        self,
        recording_id: int,
        transcript: str,
        transcript_with_speakers: Optional[str] = None,
        duration: Optional[float] = None,
        status: str = "completed",
        error: Optional[str] = None
    ) -> Optional[Recording]:
        """Update recording with transcription results"""
        db = SessionLocal()
        try:
            recording = db.query(Recording).filter(Recording.id == recording_id).first()
            if recording:
                recording.transcript = transcript
                recording.transcript_with_speakers = transcript_with_speakers
                recording.duration = duration
                recording.processing_status = status
                recording.processing_error = error
                recording.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(recording)
            return recording
        finally:
            db.close()
    
    def update_analysis(
        self,
        recording_id: int,
        summary: Optional[str] = None,
        action_items: Optional[List[Dict[str, Any]]] = None,
        decisions: Optional[List[Dict[str, Any]]] = None,
        status: str = "completed",
        error: Optional[str] = None
    ) -> Optional[Recording]:
        """Update recording with analysis results"""
        logger.info(f"📊 Updating analysis for recording {recording_id}")
        
        db = SessionLocal()
        try:
            recording = db.query(Recording).filter(Recording.id == recording_id).first()
            if recording:
                # Only update fields that are explicitly provided
                if summary is not None:
                    recording.summary = summary
                if action_items is not None:
                    recording.action_items = action_items
                if decisions is not None:
                    recording.decisions = decisions
                recording.processing_status = status
                if error:
                    recording.processing_error = error
                recording.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(recording)
                logger.info(f"✅ Analysis updated for recording {recording_id}")
            return recording
        except Exception as e:
            logger.error(f"❌ Failed to update analysis for recording {recording_id}: {e}")
            db.rollback()
            raise e
        finally:
            db.close()
    
    def update_recording(
        self,
        recording_id: int,
        visual_summary_url: Optional[str] = None,
        labels: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[Recording]:
        """Update recording with additional data like visual summary"""
        logger.info(f"📝 Updating recording {recording_id}")
        
        db = SessionLocal()
        try:
            recording = db.query(Recording).filter(Recording.id == recording_id).first()
            if recording:
                if visual_summary_url:
                    recording.visual_summary_url = visual_summary_url
                if labels is not None:
                    recording.labels = labels
                recording.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(recording)
                logger.info(f"✅ Recording {recording_id} updated successfully")
            return recording
        except Exception as e:
            logger.error(f"❌ Failed to update recording {recording_id}: {e}")
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_recording(self, recording_id: int) -> Optional[Recording]:
        """Get a recording by ID"""
        db = SessionLocal()
        try:
            return db.query(Recording).filter(Recording.id == recording_id).first()
        finally:
            db.close()
    
    def get_recordings(self, skip: int = 0, limit: int = 100) -> List[Recording]:
        """Get all recordings with pagination"""
        db = SessionLocal()
        try:
            return db.query(Recording).offset(skip).limit(limit).all()
        finally:
            db.close()
    
    def get_recordings_count(self) -> int:
        """Get total count of recordings"""
        db = SessionLocal()
        try:
            return db.query(Recording).count()
        finally:
            db.close()
    
    def delete_recording(self, recording_id: int) -> bool:
        """Delete a recording"""
        db = SessionLocal()
        try:
            recording = db.query(Recording).filter(Recording.id == recording_id).first()
            if recording:
                db.delete(recording)
                db.commit()
                return True
            return False
        finally:
            db.close()



# Global recording service instance
recording_service = RecordingService() 