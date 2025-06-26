from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import (
    LabelingRuleCreate, 
    LabelingRuleUpdate, 
    LabelingRuleResponse,
    BasicResponse,
    AppliedLabel
)
from app.services.labeling_service import labeling_service
from app.services.recording_service import recording_service

router = APIRouter()

@router.post("/", response_model=LabelingRuleResponse)
async def create_labeling_rule(
    rule_data: LabelingRuleCreate, 
    db: Session = Depends(get_db)
):
    """Create a new labeling rule"""
    return labeling_service.create_rule(db, rule_data)

@router.get("/", response_model=List[LabelingRuleResponse])
async def get_labeling_rules(
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all labeling rules"""
    return labeling_service.get_rules(db, active_only=active_only)

@router.get("/{rule_id}", response_model=LabelingRuleResponse)
async def get_labeling_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific labeling rule"""
    rule = labeling_service.get_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Labeling rule not found")
    return rule

@router.put("/{rule_id}", response_model=LabelingRuleResponse)
async def update_labeling_rule(
    rule_id: int, 
    rule_data: LabelingRuleUpdate,
    db: Session = Depends(get_db)
):
    """Update a labeling rule"""
    rule = labeling_service.update_rule(db, rule_id, rule_data)
    if not rule:
        raise HTTPException(status_code=404, detail="Labeling rule not found")
    return rule

@router.delete("/{rule_id}", response_model=BasicResponse)
async def delete_labeling_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Delete a labeling rule"""
    success = labeling_service.delete_rule(db, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Labeling rule not found")
    return BasicResponse(message="Labeling rule deleted successfully", status="success")

@router.post("/apply/{recording_id}", response_model=List[AppliedLabel])
async def apply_labels_to_recording(
    recording_id: int
):
    """Apply labeling rules to a specific recording on-demand"""
    # Get the recording
    recording = recording_service.get_recording(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    # Check if recording has the required data
    if not recording.summary:
        raise HTTPException(
            status_code=400, 
            detail="Recording must be analyzed before labeling"
        )
    
    # Apply labeling rules
    applied_labels = await labeling_service.apply_rules_to_recording(
        summary=recording.summary,
        action_items=recording.action_items or [],
        decisions=recording.decisions or [],
        transcript=recording.transcript or ""
    )
    
    # Update the recording with the labels
    recording_service.update_recording(
        recording_id=recording_id,
        labels=applied_labels
    )
    
    return applied_labels 