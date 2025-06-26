from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import json
from openai import OpenAI

from app.models.labeling_rule import LabelingRule
from app.models.database import SessionLocal
from app.core.config import settings

logger = logging.getLogger(__name__)


class LabelingService:
    """Service for managing labeling rules and applying them to recordings"""
    
    def __init__(self):
        logger.info("🏷️  Initializing LabelingService")
        
        if settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            logger.info("✅ OpenAI client initialized for labeling")
        else:
            self.openai_client = None
            logger.warning("⚠️  OpenAI API key not configured - labeling will not be available")
    
    def create_rule(
        self,
        db: Session,
        rule_data: Any
    ) -> LabelingRule:
        """Create a new labeling rule"""
        logger.info(f"📝 Creating new labeling rule: {rule_data.label_name}")
        
        try:
            rule = LabelingRule(
                label_name=rule_data.label_name,
                label_color=rule_data.label_color,
                rule_description=rule_data.rule_description,
                is_active=rule_data.is_active
            )
            db.add(rule)
            db.commit()
            db.refresh(rule)
            
            logger.info(f"✅ Labeling rule created with ID: {rule.id}")
            return rule
        except Exception as e:
            logger.error(f"❌ Failed to create labeling rule: {e}")
            db.rollback()
            raise e
    
    def get_rules(self, db: Session, active_only: bool = False) -> List[LabelingRule]:
        """Get all labeling rules"""
        query = db.query(LabelingRule)
        if active_only:
            query = query.filter(LabelingRule.is_active == True)
        return query.order_by(LabelingRule.created_at.desc()).all()
    
    def get_rule(self, db: Session, rule_id: int) -> Optional[LabelingRule]:
        """Get a labeling rule by ID"""
        return db.query(LabelingRule).filter(LabelingRule.id == rule_id).first()
    
    def update_rule(
        self,
        db: Session,
        rule_id: int,
        rule_data: Any
    ) -> Optional[LabelingRule]:
        """Update a labeling rule"""
        logger.info(f"📝 Updating labeling rule {rule_id}")
        
        try:
            rule = db.query(LabelingRule).filter(LabelingRule.id == rule_id).first()
            if rule:
                if rule_data.label_name is not None:
                    rule.label_name = rule_data.label_name
                if rule_data.label_color is not None:
                    rule.label_color = rule_data.label_color
                if rule_data.rule_description is not None:
                    rule.rule_description = rule_data.rule_description
                if rule_data.is_active is not None:
                    rule.is_active = rule_data.is_active
                rule.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(rule)
                logger.info(f"✅ Labeling rule {rule_id} updated")
            return rule
        except Exception as e:
            logger.error(f"❌ Failed to update labeling rule {rule_id}: {e}")
            db.rollback()
            raise e
    
    def delete_rule(self, db: Session, rule_id: int) -> bool:
        """Delete a labeling rule"""
        logger.info(f"🗑️  Deleting labeling rule {rule_id}")
        
        try:
            rule = db.query(LabelingRule).filter(LabelingRule.id == rule_id).first()
            if rule:
                db.delete(rule)
                db.commit()
                logger.info(f"✅ Labeling rule {rule_id} deleted")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to delete labeling rule {rule_id}: {e}")
            db.rollback()
            raise e
    
    async def apply_rules_to_recording(
        self,
        summary: str,
        action_items: List[Dict[str, Any]],
        decisions: List[Dict[str, Any]],
        transcript: str
    ) -> List[Dict[str, Any]]:
        """Apply labeling rules to a recording and return applicable labels"""
        if not self.openai_client:
            logger.warning("⚠️  OpenAI API key not configured for labeling")
            return []
        
        # Get active rules using a new session
        db = SessionLocal()
        try:
            active_rules = self.get_rules(db, active_only=True)
            if not active_rules:
                logger.info("📋 No active labeling rules found")
                return []
        finally:
            db.close()
        
        logger.info(f"🏷️  Applying {len(active_rules)} labeling rules to recording")
        
        try:
            # Prepare rules for AI analysis
            rules_prompt = "Apply the following labeling rules to this meeting recording:\n\n"
            for rule in active_rules:
                rules_prompt += f"**{rule.label_name}**: {rule.rule_description}\n"
            
            rules_prompt += f"""
Based on the meeting content below, determine which labels should be applied.
Return a JSON array of objects with: {{"label_name": "string", "confidence": 0.0-1.0, "reasoning": "string"}}

Meeting Summary: {summary or "No summary available"}

Action Items: {len(action_items)} items found
{json.dumps(action_items[:3], indent=2) if action_items else "None"}

Decisions: {len(decisions)} decisions found
{json.dumps(decisions[:3], indent=2) if decisions else "None"}

Transcript Preview: {transcript[:500] if transcript else "No transcript available"}...
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": rules_prompt
                }],
                temperature=0.3,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Convert AI response to our format and add colors
            applied_labels = []
            for ai_label in result.get("labels", []):
                # Find the matching rule to get the color
                matching_rule = next(
                    (rule for rule in active_rules if rule.label_name == ai_label["label_name"]),
                    None
                )
                if matching_rule and ai_label.get("confidence", 0) > 0.6:  # Only apply if confidence > 60%
                    applied_labels.append({
                        "label_name": matching_rule.label_name,
                        "label_color": matching_rule.label_color,
                        "confidence": ai_label.get("confidence", 0.8)
                    })
            
            logger.info(f"✅ Applied {len(applied_labels)} labels to recording")
            return applied_labels
            
        except Exception as e:
            logger.error(f"❌ Failed to apply labeling rules: {e}")
            return []


# Global labeling service instance
labeling_service = LabelingService() 