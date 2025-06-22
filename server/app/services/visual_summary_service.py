import logging
import httpx
from typing import Dict, Any, Optional
from openai import OpenAI

from app.core.config import settings
from app.services.storage_service import storage_service

logger = logging.getLogger(__name__)


class VisualSummaryService:
    """Service for generating visual summaries using DALL·E 3"""
    
    def __init__(self):
        logger.info("🎨 Initializing VisualSummaryService")
        
        if settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            logger.info("✅ OpenAI client initialized for DALL·E 3")
        else:
            self.openai_client = None
            logger.warning("⚠️  OpenAI API key not configured - visual summaries will not be available")
    
    async def generate_visual_summary(self, recording_id: int, summary: str, action_items: list, decisions: list, filename: str) -> Optional[str]:
        """
        Generate a visual summary using DALL·E 3 based on meeting content
        
        Args:
            recording_id: ID of the recording
            summary: Meeting summary text
            action_items: List of action items
            decisions: List of decisions
            filename: Original filename for context
            
        Returns:
            URL of the uploaded visual summary image, or None if failed
        """
        if not self.openai_client:
            logger.error("❌ OpenAI client not available for visual summary")
            return None
        
        logger.info(f"🎨 Generating visual summary for recording {recording_id}")
        
        try:
            # Create a prompt for DALL·E 3 based on meeting content
            prompt = self._create_visual_prompt(summary, action_items, decisions, filename)
            logger.info(f"📝 Generated DALL·E prompt: {prompt[:200]}...")
            
            # Generate image using DALL·E 3
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            logger.info(f"✅ DALL·E 3 image generated: {image_url}")
            
            # Download the image
            image_content = self._download_image(image_url)
            if not image_content:
                logger.error("❌ Failed to download generated image")
                return None
            
            # Upload to Supabase storage
            visual_filename = f"visual_summary_{recording_id}.png"
            file_details = storage_service.upload_file(
                file_content=image_content,
                filename=visual_filename,
                content_type="image/png"
            )
            
            logger.info(f"✅ Visual summary uploaded to storage: {file_details['public_url']}")
            return file_details['public_url']
            
        except Exception as e:
            logger.error(f"❌ Failed to generate visual summary: {e}")
            return None
    
    def _create_visual_prompt(self, summary: str, action_items: list, decisions: list, filename: str) -> str:
        """Create a DALL·E 3 prompt for a decision tree based on meeting content"""
        
        # Analyze the structure of decisions and action items
        decision_flow = self._analyze_decision_flow(decisions, action_items, summary)
        
        # Build decision tree prompt
        prompt_parts = [
            "Create a professional decision tree flowchart diagram with a modern, clean design.",
            "The flowchart should show logical decision paths and action flows in a business context."
        ]
        
        # Add decision-specific elements
        if decisions and len(decisions) > 0:
            decision_count = len(decisions)
            prompt_parts.append(f"Include {decision_count} main decision nodes represented as diamond shapes.")
            prompt_parts.append("Each decision node should branch into different paths showing outcomes.")
        
        # Add action items as process nodes
        if action_items and len(action_items) > 0:
            action_count = len(action_items)
            prompt_parts.append(f"Include {action_count} action/process nodes shown as rectangular boxes.")
            prompt_parts.append("Connect action nodes to decision nodes with directional arrows.")
        
        # Add flow characteristics based on content analysis
        if decision_flow['complexity'] == 'simple':
            prompt_parts.append("Create a straightforward linear flow with 2-3 main branches.")
        elif decision_flow['complexity'] == 'moderate':
            prompt_parts.append("Create a moderate complexity tree with multiple decision points and 4-6 branches.")
        else:
            prompt_parts.append("Create a comprehensive decision tree with multiple levels and parallel processes.")
        
        # Add context-specific elements
        if decision_flow['has_timeline']:
            prompt_parts.append("Include timeline indicators or sequential numbering to show order of execution.")
        
        if decision_flow['has_priorities']:
            prompt_parts.append("Use color coding to indicate priority levels (red for high, yellow for medium, green for low priority).")
        
        # Style guidelines
        prompt_parts.extend([
            "Use a professional business color scheme with blues, greens, and gray tones.",
            "Include standard flowchart symbols: diamonds for decisions, rectangles for processes, circles for start/end points.",
            "Add directional arrows to show the flow between elements.",
            "Keep the design clean and readable with proper spacing between elements.",
            "No text or words in the diagram - use shapes, colors, and flow indicators only.",
            "The style should be similar to professional business process diagrams and organizational charts."
        ])
        
        return " ".join(prompt_parts)
    
    
    
    def _analyze_decision_flow(self, decisions: list, action_items: list, summary: str) -> dict:
        """Analyze the decision flow structure to determine visualization approach"""
        
        flow_analysis = {
            'complexity': 'simple',
            'has_timeline': False,
            'has_priorities': False,
            'has_dependencies': False,
            'decision_types': []
        }
        
        total_items = len(decisions or []) + len(action_items or [])
        
        # Determine complexity based on number of items
        if total_items <= 3:
            flow_analysis['complexity'] = 'simple'
        elif total_items <= 7:
            flow_analysis['complexity'] = 'moderate'
        else:
            flow_analysis['complexity'] = 'complex'
        
        # Analyze action items for timeline and priority indicators
        for item in (action_items or []):
            item_str = str(item).lower()
            
            # Check for timeline indicators
            timeline_keywords = ['due', 'deadline', 'by', 'until', 'before', 'after', 'next', 'first', 'then', 'finally']
            if any(keyword in item_str for keyword in timeline_keywords):
                flow_analysis['has_timeline'] = True
            
            # Check for priority indicators
            priority_keywords = ['priority', 'urgent', 'critical', 'important', 'high', 'low', 'medium']
            if any(keyword in item_str for keyword in priority_keywords):
                flow_analysis['has_priorities'] = True
                
            # Check for dependencies
            dependency_keywords = ['depends', 'after', 'before', 'requires', 'prerequisite', 'blocks', 'waiting']
            if any(keyword in item_str for keyword in dependency_keywords):
                flow_analysis['has_dependencies'] = True
        
        # Analyze decisions for types
        for decision in (decisions or []):
            decision_str = str(decision).lower()
            
            if any(keyword in decision_str for keyword in ['approve', 'approval', 'accept', 'reject']):
                flow_analysis['decision_types'].append('approval')
            elif any(keyword in decision_str for keyword in ['choose', 'select', 'option', 'alternative']):
                flow_analysis['decision_types'].append('selection')
            elif any(keyword in decision_str for keyword in ['continue', 'proceed', 'stop', 'halt']):
                flow_analysis['decision_types'].append('go_no_go')
            else:
                flow_analysis['decision_types'].append('general')
        
        return flow_analysis
    
    def _download_image(self, image_url: str) -> Optional[bytes]:
        """Download image from URL"""
        try:
            with httpx.Client(timeout=30) as client:
                response = client.get(image_url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.error(f"❌ Failed to download image: {e}")
            return None


# Global visual summary service instance
visual_summary_service = VisualSummaryService() 