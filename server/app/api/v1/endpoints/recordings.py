from fastapi import APIRouter, HTTPException, Query
from typing import List
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.models.schemas import RecordingResponse, RecordingListResponse
from app.services.recording_service import recording_service
from app.services.storage_service import storage_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/recordings", response_model=RecordingListResponse)
async def get_recordings(
    skip: int = Query(0, ge=0, description="Number of recordings to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of recordings to return")
):
    """Get all recordings with pagination"""
    logger.info(f"📋 Fetching recordings list - Skip: {skip}, Limit: {limit}")
    
    try:
        # Run database operations in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            recordings_task = loop.run_in_executor(
                executor, recording_service.get_recordings, skip, limit
            )
            count_task = loop.run_in_executor(
                executor, recording_service.get_recordings_count
            )
            
            recordings, total = await asyncio.gather(recordings_task, count_task)
        
        logger.info(f"✅ Retrieved {len(recordings)} recordings out of {total} total")
        
        return RecordingListResponse(
            recordings=[RecordingResponse.from_orm(r) for r in recordings],
            total=total
        )
    except Exception as e:
        logger.error(f"❌ Failed to fetch recordings: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch recordings")


@router.get("/recordings/{recording_id}", response_model=RecordingResponse)
async def get_recording(recording_id: int):
    """Get a specific recording by ID"""
    logger.info(f"🔍 Fetching recording with ID: {recording_id}")
    
    try:
        # Run database operation in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            recording = await loop.run_in_executor(
                executor, recording_service.get_recording, recording_id
            )
        
        if not recording:
            logger.warning(f"⚠️  Recording not found: {recording_id}")
            raise HTTPException(status_code=404, detail="Recording not found")
        
        logger.info(f"✅ Retrieved recording: {recording.original_filename} (Status: {recording.processing_status})")
        return RecordingResponse.from_orm(recording)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to fetch recording {recording_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch recording")


@router.delete("/recordings/{recording_id}")
async def delete_recording(recording_id: int):
    """Delete a recording"""
    logger.info(f"🗑️  Attempting to delete recording with ID: {recording_id}")
    
    try:
        # First get the recording to access its storage path
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            recording = await loop.run_in_executor(
                executor, recording_service.get_recording, recording_id
            )
        
        if not recording:
            logger.warning(f"⚠️  Recording not found for deletion: {recording_id}")
            raise HTTPException(status_code=404, detail="Recording not found")
        
        # Delete files from storage
        if recording.storage_path:
            logger.info(f"🗑️  Deleting recording file: {recording.storage_path}")
            storage_deleted = storage_service.delete_file(recording.storage_path)
            if not storage_deleted:
                logger.warning(f"⚠️  Failed to delete recording file: {recording.storage_path}")
        
        # Delete AI-generated visual summary if it exists
        if recording.visual_summary_url:
            logger.info(f"🎨 Deleting visual summary for recording {recording_id}")
            visual_deleted = storage_service.delete_visual_summary(recording_id, recording.visual_summary_url)
            if not visual_deleted:
                logger.warning(f"⚠️  Failed to delete visual summary for recording {recording_id}")
        
        # Run database operation in thread pool to avoid blocking
        with ThreadPoolExecutor() as executor:
            success = await loop.run_in_executor(
                executor, recording_service.delete_recording, recording_id
            )
        
        if not success:
            logger.warning(f"⚠️  Failed to delete recording from database: {recording_id}")
            raise HTTPException(status_code=500, detail="Failed to delete recording from database")
        
        logger.info(f"✅ Successfully deleted recording: {recording_id}")
        return {"message": "Recording deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete recording {recording_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete recording")