import logging
import json
from typing import Dict, List, Optional, Any
from openai import OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for analyzing transcripts to extract insights"""
    
    def __init__(self):
        logger.info("🧠 Initializing AnalysisService")
        
        if settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            logger.info("✅ OpenAI client initialized for analysis")
        else:
            self.openai_client = None
            logger.warning("⚠️  OpenAI API key not configured - analysis will not be available")
    
    async def analyze_transcript(self, transcript: str, transcript_with_speakers: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze transcript to extract summary, action items, and decisions
        
        Args:
            transcript: Raw transcript text
            transcript_with_speakers: Speaker-diarized transcript (preferred if available)
            
        Returns:
            Dict containing analysis results
        """
        if not self.openai_client:
            logger.error("❌ OpenAI API key not configured for analysis")
            return {
                "summary": None,
                "action_items": [],
                "decisions": [],
                "error": "OpenAI API key not configured"
            }
        
        # Use speaker-diarized transcript if available, otherwise use regular transcript
        text_to_analyze = transcript_with_speakers or transcript
        
        if not text_to_analyze or len(text_to_analyze.strip()) < 50:
            logger.warning("⚠️  Transcript too short for meaningful analysis")
            return {
                "summary": "Transcript too short for analysis",
                "action_items": [],
                "decisions": [],
                "error": None
            }
        
        logger.info(f"🔍 Starting transcript analysis ({len(text_to_analyze)} characters)")
        
        try:
            # Create comprehensive analysis prompt
            analysis_result = await self._perform_comprehensive_analysis(text_to_analyze)
            logger.info("✅ Transcript analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            return {
                "summary": None,
                "action_items": [],
                "decisions": [],
                "error": str(e)
            }
    
    async def _perform_comprehensive_analysis(self, transcript: str) -> Dict[str, Any]:
        """Perform comprehensive analysis using OpenAI GPT"""
        
        system_prompt = """You are an AI assistant specialized in analyzing meeting transcripts and recordings. Your task is to:

1. Provide a clear, concise summary of the main topics discussed
2. Extract specific action items with details about who should do what
3. Identify key decisions made and who owns them

Please analyze the transcript and return a JSON response with the following structure:

{
  "summary": "A 2-3 paragraph summary of the main discussion points and outcomes",
  "action_items": [
    {
      "description": "Clear description of what needs to be done",
      "assignee": "Person responsible (if mentioned) or null",
      "due_date": "Due date if mentioned (YYYY-MM-DD format) or null",
      "priority": "high/medium/low if indicated, or null"
    }
  ],
  "decisions": [
    {
      "description": "What was decided",
      "owner": "Person responsible for the decision or null",
      "context": "Brief context about why this decision was made",
      "impact": "Expected impact or next steps"
    }
  ]
}

Guidelines:
- Be specific and actionable
- Extract only clear, explicit action items and decisions
- If assignees/owners aren't clearly mentioned, set to null
- Keep descriptions concise but informative
- Focus on business outcomes and next steps"""

        user_prompt = f"""Please analyze this transcript and extract the summary, action items, and decisions:

TRANSCRIPT:
{transcript}

Return only valid JSON in the specified format."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # Use GPT-4 for better analysis quality
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent output
                max_tokens=2000,
                response_format={"type": "json_object"}  # Ensure JSON response
            )
            
            analysis_text = response.choices[0].message.content
            analysis_data = json.loads(analysis_text)
            
            # Validate and clean the response
            return {
                "summary": analysis_data.get("summary"),
                "action_items": analysis_data.get("action_items", []),
                "decisions": analysis_data.get("decisions", []),
                "error": None
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse analysis JSON: {e}")
            return await self._fallback_analysis(transcript)
        except Exception as e:
            logger.error(f"❌ OpenAI analysis failed: {e}")
            raise e
    
    async def _fallback_analysis(self, transcript: str) -> Dict[str, Any]:
        """Fallback analysis with simpler prompts if JSON parsing fails"""
        logger.info("🔄 Attempting fallback analysis with simpler prompts")
        
        try:
            # Simple summary
            summary_response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user", 
                    "content": f"Please provide a concise 2-3 paragraph summary of this transcript:\n\n{transcript}"
                }],
                temperature=0.3,
                max_tokens=500
            )
            
            summary = summary_response.choices[0].message.content
            
            return {
                "summary": summary,
                "action_items": [],
                "decisions": [],
                "error": "Used fallback analysis - action items and decisions extraction failed"
            }
            
        except Exception as e:
            logger.error(f"❌ Fallback analysis also failed: {e}")
            raise e


# Global analysis service instance
analysis_service = AnalysisService() 