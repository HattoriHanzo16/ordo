from fastapi import APIRouter, File, UploadFile, Depends, BackgroundTasks
from typing import Any, List
import logging
import asyncio

from app.models.schemas import FileUploadResponse, MultipleFileUploadResponse, RecordingResponse
from app.services.storage_service import storage_service
from app.services.file_service import file_service
from app.services.recording_service import recording_service
from app.services.transcription_service import transcription_service
from app.services.analysis_service import analysis_service

logger = logging.getLogger(__name__)

router = APIRouter()


async def process_transcription(recording_id: int, media_url: str, file_content: bytes):
    """Background task to process transcription and analysis for uploaded media files"""
    logger.info(f"🎯 Starting background transcription for recording ID: {recording_id}")
    
    try:
        # Update status to processing
        recording_service.update_transcription(
            recording_id=recording_id,
            transcript="",
            status="processing"
        )
        
        # Perform transcription
        transcription_result = await transcription_service.transcribe_media(
            media_url=media_url,
            file_content=file_content
        )
        
        if transcription_result["error"]:
            # Update with error
            recording_service.update_transcription(
                recording_id=recording_id,
                transcript="",
                status="failed",
                error=transcription_result["error"]
            )
            logger.error(f"❌ Transcription failed for recording {recording_id}: {transcription_result['error']}")
        else:
            # Update with successful transcription
            recording_service.update_transcription(
                recording_id=recording_id,
                transcript=transcription_result["transcript"],
                transcript_with_speakers=transcription_result["transcript_with_speakers"],
                duration=transcription_result["duration"],
                status="analyzing"  # Set to analyzing status
            )
            logger.info(f"✅ Transcription completed for recording {recording_id}")
            
            # Now perform analysis
            logger.info(f"🧠 Starting analysis for recording {recording_id}")
            
            analysis_result = await analysis_service.analyze_transcript(
                transcript=transcription_result["transcript"],
                transcript_with_speakers=transcription_result["transcript_with_speakers"]
            )
            
            if analysis_result["error"]:
                # Update with analysis error but keep transcription
                recording_service.update_analysis(
                    recording_id=recording_id,
                    summary=analysis_result.get("summary"),
                    action_items=analysis_result.get("action_items", []),
                    decisions=analysis_result.get("decisions", []),
                    status="completed",  # Still mark as completed since transcription worked
                    error=f"Analysis failed: {analysis_result['error']}"
                )
                logger.warning(f"⚠️  Analysis failed for recording {recording_id}: {analysis_result['error']}")
            else:
                # Update with successful analysis
                recording_service.update_analysis(
                    recording_id=recording_id,
                    summary=analysis_result["summary"],
                    action_items=analysis_result["action_items"],
                    decisions=analysis_result["decisions"],
                    status="completed"
                )
                logger.info(f"✅ Analysis completed for recording {recording_id}")
            
    except Exception as e:
        logger.error(f"❌ Processing failed for recording {recording_id}: {e}")
        recording_service.update_transcription(
            recording_id=recording_id,
            transcript="",
            status="failed",
            error=str(e)
        )


def should_transcribe(content_type: str) -> bool:
    """Check if the file type should be transcribed"""
    audio_video_types = [
        "audio/mpeg", "audio/mp3", "audio/wav", "audio/m4a", "audio/flac", "audio/aac",
        "video/mp4", "video/mov", "video/avi", "video/webm", "video/mkv", "video/wmv",
        "video/mpeg", "video/mpg"
    ]
    return content_type in audio_video_types


@router.post("/upload", response_model=RecordingResponse)
async def upload_file(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
) -> Any:
    """
    Upload a single file to Supabase Storage bucket and create recording entry
    
    Args:
        background_tasks: FastAPI background tasks
        file: The uploaded file
        
    Returns:
        RecordingResponse: Recording entry with upload details
    """
    logger.info(f"📤 Starting single file upload: {file.filename}")
    
    try:
        logger.info(f"📋 File details - Size: {file.size}, Type: {file.content_type}")
        
        # Validate the file
        file_service.validate_file(file)
        logger.info("✅ File validation passed")
        
        # Read file content
        file_content = await file.read()
        logger.info(f"📖 Read {len(file_content)} bytes from file")
        
        # Upload to Supabase Storage
        file_details = storage_service.upload_file(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type
        )
        logger.info("☁️  File uploaded to storage successfully")
        
        # Create recording entry in database
        recording = recording_service.create_recording(
            original_filename=file_details['original_filename'],
            media_url=file_details['public_url'],
            storage_path=file_details['storage_path'],
            file_size=file_details['file_size'],
            content_type=file_details['content_type']
        )
        logger.info(f"📝 Recording entry created with ID: {recording.id}")
        
        # Start transcription and analysis process if it's an audio/video file
        if should_transcribe(file.content_type or ""):
            logger.info(f"🎤 Scheduling transcription and analysis for {file.filename}")
            background_tasks.add_task(
                process_transcription,
                recording.id,
                file_details['public_url'],
                file_content
            )
        else:
            logger.info(f"⏭️  Skipping transcription for {file.content_type} file")
        
        logger.info(f"✅ Single file upload completed: {file.filename}")
        return RecordingResponse.from_orm(recording)
        
    except Exception as e:
        logger.error(f"❌ Upload failed for {file.filename}: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise e


@router.post("/upload-multiple", response_model=MultipleFileUploadResponse)
async def upload_multiple_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
) -> Any:
    """
    Upload multiple files to Supabase Storage bucket and create recording entries
    
    Args:
        background_tasks: FastAPI background tasks
        files: List of uploaded files
        
    Returns:
        MultipleFileUploadResponse: Upload success response with all file details
    """
    logger.info(f"📤 Starting multiple file upload: {len(files)} files")
    
    uploaded_files = []
    failed_files = []
    
    for i, file in enumerate(files):
        logger.info(f"📁 Processing file {i+1}/{len(files)}: {file.filename}")
        
        try:
            logger.debug(f"📋 File details - Size: {file.size}, Type: {file.content_type}")
            
            # Validate the file
            file_service.validate_file(file)
            logger.debug("✅ File validation passed")
            
            # Read file content
            file_content = await file.read()
            logger.debug(f"📖 Read {len(file_content)} bytes from file")
            
            # Upload to Supabase Storage
            file_details = storage_service.upload_file(
                file_content=file_content,
                filename=file.filename,
                content_type=file.content_type
            )
            logger.debug("☁️  File uploaded to storage successfully")
            
            # Create recording entry in database
            recording = recording_service.create_recording(
                original_filename=file_details['original_filename'],
                media_url=file_details['public_url'],
                storage_path=file_details['storage_path'],
                file_size=file_details['file_size'],
                content_type=file_details['content_type']
            )
            logger.debug(f"📝 Recording entry created with ID: {recording.id}")
            
            # Start transcription and analysis process if it's an audio/video file
            if should_transcribe(file.content_type or ""):
                logger.info(f"🎤 Scheduling transcription and analysis for {file.filename}")
                background_tasks.add_task(
                    process_transcription,
                    recording.id,
                    file_details['public_url'],
                    file_content
                )
            else:
                logger.debug(f"⏭️  Skipping transcription for {file.content_type} file")
            
            uploaded_files.append(file_details)
            logger.info(f"✅ Successfully processed file {i+1}/{len(files)}: {file.filename}")
            
        except Exception as e:
            logger.error(f"❌ Upload failed for file {i+1}/{len(files)} ({file.filename}): {str(e)}")
            import traceback
            logger.error(f"Exception details: {traceback.format_exc()}")
            failed_files.append({
                "filename": file.filename,
                "error": str(e) if str(e) else f"Unknown error: {type(e).__name__}"
            })
    
    logger.info(f"📊 Multiple upload completed - Success: {len(uploaded_files)}, Failed: {len(failed_files)}")
    
    return MultipleFileUploadResponse(
        message=f"Uploaded {len(uploaded_files)} files successfully",
        successful_uploads=len(uploaded_files),
        failed_uploads=len(failed_files),
        file_details=uploaded_files,
        failed_files=failed_files
    ) 