import asyncio
import logging
from typing import Any, Dict

from app.services.recording_service import recording_service
from app.services.transcription_service import transcription_service
from app.services.analysis_service import analysis_service
from app.services.visual_summary_service import visual_summary_service

logger = logging.getLogger(__name__)


def process_transcription_task(recording_id: int, media_url: str, file_content: bytes, **kwargs):
    """
    Background task to process transcription and analysis for uploaded media files
    This runs in a separate worker process
    """
    logger.info(f"🎯 Starting background transcription for recording ID: {recording_id}")
    
    try:
        # Update status to processing
        recording_service.update_transcription(
            recording_id=recording_id,
            transcript="",
            status="processing"
        )
        
        # Run the async transcription in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Perform transcription
            transcription_result = loop.run_until_complete(
                transcription_service.transcribe_media(
                    media_url=media_url,
                    file_content=file_content
                )
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
                
                analysis_result = loop.run_until_complete(
                    analysis_service.analyze_transcript(
                        transcript=transcription_result["transcript"],
                        transcript_with_speakers=transcription_result["transcript_with_speakers"]
                    )
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
                    # Update with successful analysis and start visual generation
                    recording_service.update_analysis(
                        recording_id=recording_id,
                        summary=analysis_result["summary"],
                        action_items=analysis_result["action_items"],
                        decisions=analysis_result["decisions"],
                        status="generating_visuals"  # Set status to generating visuals
                    )
                    logger.info(f"✅ Analysis completed for recording {recording_id}")
                    
                    # Generate visual summary using DALL·E 3
                    logger.info(f"🎨 Starting visual summary generation for recording {recording_id}")
                    try:
                        # Get recording object to access filename
                        current_recording = recording_service.get_recording(recording_id)
                        filename = current_recording.original_filename if current_recording else f"recording_{recording_id}"
                        
                        visual_summary_url = loop.run_until_complete(
                            visual_summary_service.generate_visual_summary(
                                recording_id=recording_id,
                                summary=analysis_result["summary"],
                                action_items=analysis_result["action_items"],
                                decisions=analysis_result["decisions"],
                                filename=filename
                            )
                        )
                        
                        if visual_summary_url:
                            # Update recording with visual summary URL and mark as completed
                            recording_service.update_recording(
                                recording_id=recording_id,
                                visual_summary_url=visual_summary_url
                            )
                            # Update status to completed
                            recording_service.update_analysis(
                                recording_id=recording_id,
                                status="completed"
                            )
                            logger.info(f"✅ Visual summary generated and saved for recording {recording_id}")
                        else:
                            # Failed to generate visual summary, but mark as completed since analysis succeeded
                            recording_service.update_analysis(
                                recording_id=recording_id,
                                status="completed",
                                error="Visual summary generation failed"
                            )
                            logger.warning(f"⚠️  Failed to generate visual summary for recording {recording_id}")
                            
                    except Exception as visual_error:
                        logger.error(f"❌ Error generating visual summary for recording {recording_id}: {visual_error}")
                        # Mark as completed with error since analysis succeeded
                        recording_service.update_analysis(
                            recording_id=recording_id,
                            status="completed",
                            error=f"Visual summary generation failed: {str(visual_error)}"
                        )
                
                # Processing completed
                logger.info(f"✅ Processing completed for recording {recording_id} (transcription + analysis + visual)")
                
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"❌ Processing failed for recording {recording_id}: {e}")
        recording_service.update_transcription(
            recording_id=recording_id,
            transcript="",
            status="failed",
            error=str(e)
        ) 