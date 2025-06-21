from fastapi import FastAPI, HTTPException
import logging
import sys
from datetime import datetime

from app.core.config import settings
from app.core.middleware import setup_middleware
from app.core.exceptions import http_exception_handler, general_exception_handler
from app.api.v1.api import api_router
from app.models.database import engine, Base

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"ordo_app_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)

# Set specific log levels for different modules
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Setup exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # Add startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"🚀 Starting {settings.api_title} v{settings.api_version}")
        logger.info(f"🔧 Debug mode: {settings.debug}")
        logger.info(f"🗄️  Database: {settings.database_connection_string.split('://')[0].upper()}")
        logger.info(f"📦 Storage Bucket: {settings.storage_bucket_name or 'Not configured'}")
        logger.info(f"🌐 Supabase URL: {'Configured' if settings.supabase_url else 'Not configured'}")
        logger.info(f"🔑 Supabase Key: {'Configured' if settings.supabase_key else 'Not configured'}")
        logger.info(f"🔑 Supabase Service Key: {'Configured' if settings.supabase_service_key else 'Not configured'}")
        logger.info(f"🤖 OpenAI API Key: {'Configured' if settings.openai_api_key else 'Not configured'}")
        
        # Create database tables
        try:
            logger.info("📊 Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create database tables: {e}")
            raise e
    
    # Add shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down application")
    
    return app


# Create the FastAPI application
app = create_application() 