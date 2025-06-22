import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Settings
    api_title: str = "Ordo Audio Processing API"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # Supabase Storage Settings
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    supabase_service_key: Optional[str] = None
    storage_bucket_name: Optional[str] = None
    
    # OpenAI Settings
    openai_api_key: Optional[str] = None
    
    # HuggingFace Settings (for speaker diarization)
    huggingface_access_token: Optional[str] = None
    
    # Database Settings (PostgreSQL via Supabase)
    database_url: Optional[str] = None
    postgres_db: Optional[str] = None
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_host: Optional[str] = None
    postgres_port: int = 5432
    
    # Redis (for task queue)
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    @property
    def database_connection_string(self) -> str:
        """Build database connection string from Supabase or individual components"""
        if self.database_url:
            return self.database_url
        
        if not all([self.postgres_host, self.postgres_db, self.postgres_user, self.postgres_password]):
            # Fallback to SQLite for development
            return "sqlite:///./ordo.db"
            
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # CORS Settings
    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]
    
    # File Upload Settings
    max_file_size: int = 500 * 1024 * 1024  # 500MB
    allowed_file_types: list[str] = [
        # Audio formats
        "audio/mpeg", "audio/mp3", "audio/wav", "audio/m4a", "audio/flac", "audio/aac",
        # Video formats
        "video/mp4", "video/mov", "video/avi", "video/webm", "video/mkv", "video/wmv",
        "video/mpeg", "video/mpg",
        # Image formats (keeping existing)
        "image/jpeg", "image/png", "image/gif", "image/webp",
        # Document formats (keeping existing)
        "application/pdf", "text/plain", "application/json",
        "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    class Config:
        env_file = [".env", "../.env", "../../.env"]  # Check multiple paths
        case_sensitive = False


# Global settings instance
settings = Settings() 