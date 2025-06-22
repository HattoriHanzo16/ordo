from fastapi import APIRouter, File, UploadFile
from typing import Any, List
import logging

from app.models.schemas import FileUploadResponse, MultipleFileUploadResponse, RecordingResponse
from app.services.storage_service import storage_service
from app.services.file_service import file_service
from app.services.recording_service import recording_service
from app.services.task_service import task_service
from app.tasks.processing_tasks import process_transcription_task


logger = logging.getLogger(__name__)

router = APIRouter()


# Background processing moved to app.tasks.processing_tasks


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
            job_id = task_service.enqueue_task(
                process_transcription_task,
                recording.id,
                file_details['public_url'],
                file_content
            )
            logger.info(f"📋 Task queued with job ID: {job_id}")
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
                job_id = task_service.enqueue_task(
                    process_transcription_task,
                    recording.id,
                    file_details['public_url'],
                    file_content
                )
                logger.info(f"📋 Task queued with job ID: {job_id}")
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