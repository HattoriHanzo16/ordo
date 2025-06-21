from fastapi import HTTPException, UploadFile
from typing import Optional
import magic
import mimetypes

from app.core.config import settings


class FileService:
    """Service class for file operations and validation"""
    
    def __init__(self):
        self.max_file_size = settings.max_file_size
        self.allowed_file_types = settings.allowed_file_types
    
    def validate_file(self, file: UploadFile) -> None:
        """
        Validate uploaded file against size and type restrictions
        
        Args:
            file: The uploaded file
            
        Raises:
            HTTPException: If file validation fails
        """
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file size
        self._validate_file_size(file)
        
        # Check file type
        self._validate_file_type(file)
    
    def _validate_file_size(self, file: UploadFile) -> None:
        """
        Validate file size
        
        Args:
            file: The uploaded file
            
        Raises:
            HTTPException: If file is too large
        """
        if file.size and file.size > self.max_file_size:
            max_size_mb = self.max_file_size / (1024 * 1024)
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size allowed: {max_size_mb:.1f}MB"
            )
    
    def _validate_file_type(self, file: UploadFile) -> None:
        """
        Validate file type based on content type
        
        Args:
            file: The uploaded file
            
        Raises:
            HTTPException: If file type is not allowed
        """
        if not self.allowed_file_types:
            return  # No restrictions
        
        content_type = file.content_type
        
        # If content_type is not provided, try to guess from filename
        if not content_type and file.filename:
            content_type, _ = mimetypes.guess_type(file.filename)
        
        if content_type not in self.allowed_file_types:
            raise HTTPException(
                status_code=415,
                detail=f"File type '{content_type}' not allowed. "
                       f"Allowed types: {', '.join(self.allowed_file_types)}"
            )
    
    def get_file_info(self, file: UploadFile) -> dict:
        """
        Get file information
        
        Args:
            file: The uploaded file
            
        Returns:
            dict: File information
        """
        return {
            'filename': file.filename,
            'content_type': file.content_type,
            'size': file.size
        }
    
    def is_file_type_allowed(self, content_type: Optional[str]) -> bool:
        """
        Check if a file type is allowed
        
        Args:
            content_type: MIME type to check
            
        Returns:
            bool: True if allowed, False otherwise
        """
        if not self.allowed_file_types:
            return True
        
        return content_type in self.allowed_file_types if content_type else False


# Global file service instance
file_service = FileService() 