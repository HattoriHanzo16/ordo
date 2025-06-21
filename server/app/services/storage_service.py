from supabase import create_client, Client
from typing import Optional, Dict, Any
import uuid
import os
import logging
from datetime import datetime
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger(__name__)


class SupabaseStorageService:
    """Service class for handling Supabase Storage operations"""
    
    def __init__(self):
        logger.info("🏗️  Initializing SupabaseStorageService")
        self._client: Optional[Client] = None
        # Don't initialize client during import - do it lazily
    
    def _initialize_client(self) -> None:
        """Initialize the Supabase client with credentials from settings"""
        logger.info("🔗 Initializing Supabase client...")
        
        if not settings.supabase_url:
            logger.error("❌ Supabase URL not configured")
            raise ValueError("Supabase URL not configured")
        
        # Use service key for server-side operations, fall back to regular key
        supabase_key = settings.supabase_service_key or settings.supabase_key
        if not supabase_key:
            logger.error("❌ Supabase key not configured")
            raise ValueError("Supabase key not configured")
        
        try:
            logger.debug(f"🌐 Connecting to Supabase: {settings.supabase_url}")
            self._client = create_client(
                settings.supabase_url,
                supabase_key
            )
            key_type = 'service key' if settings.supabase_service_key else 'anon key'
            logger.info(f"✅ Supabase client initialized with {key_type}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Supabase client: {str(e)}")
            raise ValueError(f"Failed to initialize Supabase client: {str(e)}")
    
    @property
    def client(self):
        """Get the Supabase client, initializing if necessary"""
        if self._client is None:
            self._initialize_client()
        return self._client
    
    def upload_file(
        self, 
        file_content: bytes, 
        filename: str, 
        content_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to Supabase Storage bucket
        
        Args:
            file_content: The file content as bytes
            filename: Original filename
            content_type: MIME type of the file
            
        Returns:
            Dict containing upload details
            
        Raises:
            HTTPException: If upload fails
        """
        logger.info(f"📤 Starting file upload: {filename} ({len(file_content)} bytes, {content_type})")
        
        try:
            # Generate unique storage path
            storage_path = self._generate_storage_path(filename)
            logger.debug(f"🗂️  Generated storage path: {storage_path}")
            
            # Upload to Supabase Storage
            logger.info(f"☁️  Uploading to Supabase bucket: {settings.storage_bucket_name}")
            response = self.client.storage.from_(settings.storage_bucket_name).upload(
                path=storage_path,
                file=file_content,
                file_options={
                    "content-type": content_type or 'application/octet-stream',
                    "cache-control": "3600",
                    "upsert": "false"
                }
            )
            
            if response.status_code not in [200, 201]:
                logger.error(f"❌ Upload failed with status {response.status_code}: {response.text}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Upload failed: {response.text}"
                )
            
            # Generate public URL
            public_url = self._generate_public_url(storage_path)
            logger.debug(f"🔗 Generated public URL: {public_url}")
            
            upload_result = {
                'original_filename': filename,
                'storage_path': storage_path,
                'public_url': public_url,
                'file_size': len(file_content),
                'content_type': content_type,
                'upload_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ File upload completed successfully: {filename}")
            return upload_result
            
        except Exception as e:
            logger.error(f"❌ Upload failed for {filename}: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=500,
                detail=f"Upload failed: {str(e)}"
            )
    
    def check_bucket_access(self) -> bool:
        """
        Check if the Supabase Storage bucket is accessible
        
        Returns:
            bool: True if bucket is accessible, False otherwise
        """
        try:
            # Try to list files in the bucket to check access
            response = self.client.storage.from_(settings.storage_bucket_name).list()
            return True
        except Exception:
            return False
    
    def get_bucket_info(self) -> Dict[str, str]:
        """
        Get information about Supabase Storage bucket connectivity
        
        Returns:
            Dict with bucket status information
        """
        if not settings.supabase_url or not settings.supabase_key:
            return {"status": "not configured"}
        
        try:
            # Try to access the bucket
            self.client.storage.from_(settings.storage_bucket_name).list()
            return {"status": "connected"}
        except Exception as e:
            return {"status": f"error: {str(e)}"}
    
    def _generate_storage_path(self, filename: str) -> str:
        """
        Generate a unique storage path with timestamp folder structure
        
        Args:
            filename: Original filename
            
        Returns:
            str: Generated storage path
        """
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        timestamp = datetime.now().strftime("%Y/%m/%d")
        return f"uploads/{timestamp}/{unique_filename}"
    
    def _generate_public_url(self, storage_path: str) -> str:
        """
        Generate the public URL for a file in Supabase Storage
        
        Args:
            storage_path: The storage path
            
        Returns:
            str: Public URL
        """
        try:
            response = self.client.storage.from_(settings.storage_bucket_name).get_public_url(storage_path)
            return response
        except Exception as e:
            # Fallback to constructed URL if get_public_url fails
            return f"{settings.supabase_url}/storage/v1/object/public/{settings.storage_bucket_name}/{storage_path}"


# Global Supabase storage service instance
storage_service = SupabaseStorageService() 