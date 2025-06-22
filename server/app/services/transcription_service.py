import os
import tempfile
import httpx
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
import torch
from pyannote.audio import Pipeline
from pyannote.core import Segment
import json

from app.core.config import settings

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Service for handling audio/video transcription with speaker diarization"""
    
    def __init__(self):
        logger.info("🎤 Initializing TranscriptionService")
        
        if settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            logger.info("✅ OpenAI client initialized")
        else:
            self.openai_client = None
            logger.warning("⚠️  OpenAI API key not configured - transcription will not be available")
        
        # Initialize speaker diarization pipeline (requires HuggingFace token)
        self.diarization_pipeline = None
        self.hf_token = settings.huggingface_access_token
        if self.hf_token:
            logger.info("🔑 HuggingFace token found - speaker diarization will be available")
        else:
            logger.warning("⚠️  HuggingFace token not found - speaker diarization will not be available")
        
    def _initialize_diarization(self):
        """Initialize the speaker diarization pipeline"""
        if self.hf_token and not self.diarization_pipeline:
            try:
                # Use the newer token parameter instead of use_auth_token
                self.diarization_pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    token=self.hf_token
                )
                logger.info("✅ Speaker diarization pipeline initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize diarization pipeline: {e}")
                logger.error(f"❌ Make sure you have accepted user conditions for both pyannote/segmentation-3.0 and pyannote/speaker-diarization-3.1 models")
    
    async def transcribe_media(self, media_url: str, file_content: bytes) -> Dict[str, Any]:
        """
        Transcribe audio/video file using OpenAI Whisper and add speaker diarization
        
        Args:
            media_url: URL of the uploaded media file
            file_content: Raw file content as bytes
            
        Returns:
            Dict containing transcript and speaker-diarized transcript
        """
        logger.info(f"🎯 Starting transcription for media: {media_url} ({len(file_content)} bytes)")
        
        if not self.openai_client:
            logger.error("❌ OpenAI API key not configured")
            raise ValueError("OpenAI API key not configured")
        
        result = {
            "transcript": "",
            "transcript_with_speakers": "",
            "duration": None,
            "error": None
        }
        
        try:
            # Create temporary file for processing
            logger.debug("📁 Creating temporary file for transcription")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Get basic transcription from OpenAI Whisper
                logger.info("🤖 Starting OpenAI Whisper transcription...")
                with open(temp_file_path, "rb") as audio_file:
                    try:
                        # Try with word-level timestamps (newer API)
                        transcript_response = self.openai_client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            response_format="verbose_json",
                            timestamp_granularities=["word"]
                        )
                    except Exception as e:
                        logger.warning(f"⚠️  Word-level timestamps not supported, falling back to basic transcription: {e}")
                        # Fallback to basic transcription without word timestamps
                        transcript_response = self.openai_client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            response_format="verbose_json"
                        )
                
                result["transcript"] = transcript_response.text
                result["duration"] = transcript_response.duration
                
                logger.info(f"✅ Whisper transcription completed. Duration: {result['duration']}s")
                logger.debug(f"📝 Transcript length: {len(result['transcript'])} characters")
                
                # Perform speaker diarization
                logger.info("👥 Starting speaker diarization...")
                diarized_transcript = await self._add_speaker_diarization(
                    temp_file_path, 
                    transcript_response
                )
                result["transcript_with_speakers"] = diarized_transcript
                
            finally:
                # Clean up temporary file
                logger.debug(f"🗑️  Cleaning up temporary file: {temp_file_path}")
                os.unlink(temp_file_path)
                
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"❌ Transcription failed: {e}")
        
        logger.info("🎯 Transcription process completed")
        return result
    
    async def _add_speaker_diarization(self, audio_file_path: str, whisper_response) -> str:
        """
        Add speaker diarization to the Whisper transcript
        
        Args:
            audio_file_path: Path to the audio file
            whisper_response: Response from OpenAI Whisper
            
        Returns:
            String with speaker-diarized transcript
        """
        try:
            self._initialize_diarization()
            
            if not self.diarization_pipeline:
                logger.info("⚠️  Speaker diarization not available (no HuggingFace token), returning original transcript")
                return whisper_response.text
            
            logger.info("👥 Performing speaker diarization...")
            
            # Run diarization
            diarization = self.diarization_pipeline(audio_file_path)
            
            # Debug: log diarization results
            speaker_count = len(set(speaker for _, _, speaker in diarization.itertracks(yield_label=True)))
            logger.info(f"🎯 Detected {speaker_count} unique speakers")
            
            # Get word-level timestamps from Whisper
            words = whisper_response.words if hasattr(whisper_response, 'words') else []
            
            if not words:
                logger.info("📝 No word-level timestamps available, using segment-based diarization")
                # Fallback: Use segment-based diarization without word alignment
                return self._create_segment_based_transcript(diarization, whisper_response.text)
            
            logger.info(f"📝 Processing {len(words)} words for speaker alignment")
            
            # Combine diarization with transcript
            diarized_transcript = []
            current_speaker = None
            current_segment = []
            
            for word in words:
                word_start = word.start
                word_end = word.end
                word_text = word.word
                
                # Find which speaker is talking at this time
                speaker = self._get_speaker_at_time(diarization, word_start)
                
                if speaker != current_speaker:
                    # New speaker, finish previous segment
                    if current_segment:
                        speaker_text = f"[Speaker {current_speaker}]: {' '.join(current_segment)}"
                        diarized_transcript.append(speaker_text)
                        current_segment = []
                    
                    current_speaker = speaker
                
                current_segment.append(word_text.strip())
            
            # Add final segment
            if current_segment:
                speaker_text = f"[Speaker {current_speaker}]: {' '.join(current_segment)}"
                diarized_transcript.append(speaker_text)
            
            result = "\n\n".join(diarized_transcript)
            
            # Check if we actually have multiple speakers
            if speaker_count <= 1:
                logger.info("⚠️  Only one speaker detected, speaker diarization may not be meaningful")
                result = f"[Speaker A]: {whisper_response.text}"
            
            logger.info("✅ Speaker diarization completed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Speaker diarization failed: {e}")
            logger.error(f"❌ Error details: {str(e)}")
            return whisper_response.text
    
    def _create_segment_based_transcript(self, diarization, original_text: str) -> str:
        """Create a segment-based transcript when word-level timestamps aren't available"""
        try:
            segments = []
            for segment, _, speaker in diarization.itertracks(yield_label=True):
                duration = segment.end - segment.start
                segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'speaker': speaker,
                    'duration': duration
                })
            
            if not segments:
                return f"[Speaker A]: {original_text}"
            
            # Simple approximation: divide text proportionally by time
            total_duration = sum(s['duration'] for s in segments)
            words = original_text.split()
            
            result = []
            word_index = 0
            
            for segment in segments:
                proportion = segment['duration'] / total_duration
                words_for_segment = max(1, int(len(words) * proportion))
                
                segment_words = words[word_index:word_index + words_for_segment]
                if segment_words:
                    segment_text = f"[Speaker {segment['speaker']}]: {' '.join(segment_words)}"
                    result.append(segment_text)
                
                word_index += words_for_segment
            
            # Add any remaining words to the last speaker
            if word_index < len(words):
                remaining_words = words[word_index:]
                if result and remaining_words:
                    result[-1] += f" {' '.join(remaining_words)}"
            
            return "\n\n".join(result)
            
        except Exception as e:
            logger.error(f"❌ Segment-based transcript creation failed: {e}")
            return f"[Speaker A]: {original_text}"
    
    def _get_speaker_at_time(self, diarization, timestamp: float) -> str:
        """Get the speaker who is talking at a specific timestamp"""
        for segment, _, speaker in diarization.itertracks(yield_label=True):
            if segment.start <= timestamp <= segment.end:
                return speaker
        return "Unknown"


# Global transcription service instance
transcription_service = TranscriptionService() 