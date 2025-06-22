from fastapi import APIRouter, HTTPException, Query, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Dict, Any
import logging

from app.models.database import get_db
from app.models.recording import Recording

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/search/semantic")
async def search_recordings(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    response: Response = Response,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Search through recording transcripts using simple text matching
    
    Args:
        query: The search query
        limit: Maximum number of results to return (1-50)
        db: Database session
        
    Returns:
        Dictionary containing search results and metadata
    """
    logger.info(f"🔍 Text search request - Query: '{query}', Limit: {limit}")
    
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        # Set cache control headers to prevent caching of search results
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        
        # Search in transcript and transcript_with_speakers fields
        search_term = f"%{query.strip()}%"
        
        recordings = db.query(Recording).filter(
            Recording.processing_status == "completed",  # Only search completed recordings
            or_(
                Recording.transcript.ilike(search_term),
                Recording.transcript_with_speakers.ilike(search_term),
                Recording.original_filename.ilike(search_term),
                Recording.summary.ilike(search_term)
            )
        ).limit(limit).all()
        
        results = []
        for recording in recordings:
            # Find the best matching excerpt from transcript
            transcript = recording.transcript_with_speakers or recording.transcript or ""
            
            # Find the position of the query in the transcript
            query_lower = query.lower()
            transcript_lower = transcript.lower()
            
            excerpt = ""
            similarity = 0.8  # Default similarity for text matches
            
            if query_lower in transcript_lower:
                # Find the position and create an excerpt around it
                pos = transcript_lower.find(query_lower)
                start = max(0, pos - 75)  # 75 chars before
                end = min(len(transcript), pos + len(query) + 75)  # 75 chars after
                excerpt = transcript[start:end]
                
                # Add ellipsis if we truncated
                if start > 0:
                    excerpt = "..." + excerpt
                if end < len(transcript):
                    excerpt = excerpt + "..."
                    
                similarity = 0.9  # Higher similarity for exact matches
            else:
                # Fallback to beginning of transcript
                excerpt = transcript[:150]
                if len(transcript) > 150:
                    excerpt += "..."
            
            results.append({
                "chunk_id": recording.id,  # Using recording ID as chunk ID for compatibility
                "recording_id": recording.id,
                "recording_title": recording.original_filename,
                "chunk_text": excerpt,
                "chunk_index": 0,  # Always 0 since we're not chunking
                "similarity": similarity,
                "created_at": recording.created_at.isoformat(),
                "duration": recording.duration
            })
        
        # Sort by relevance (exact filename matches first, then by date)
        results.sort(key=lambda x: (
            -1 if query.lower() in x["recording_title"].lower() else 0,
            -x["similarity"],
            x["created_at"]
        ), reverse=True)
        
        logger.info(f"✅ Text search completed - Found {len(results)} results")
        
        return {
            "query": query,
            "results": results,
            "total_results": len(results),
            "search_params": {
                "limit": limit,
                "search_type": "text_matching"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed") 