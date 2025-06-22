from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Database connection configuration
connection_string = settings.database_connection_string
is_postgresql = connection_string.startswith("postgresql://")

logger.info(f"🗄️  Database type: {'PostgreSQL' if is_postgresql else 'SQLite'}")

# Create engine with appropriate configuration
if is_postgresql:
    # PostgreSQL configuration with proper connection pooling
    engine = create_engine(
        connection_string,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=20,  # Increase connection pool size
        max_overflow=30,  # Allow temporary connections beyond pool_size
        pool_timeout=30,  # Timeout for getting connection from pool
        echo=settings.debug
    )
else:
    # SQLite configuration (fallback)
    engine = create_engine(
        connection_string,
        connect_args={"check_same_thread": False},
        pool_size=20,  # Even for SQLite, increase pool size
        max_overflow=30,
        echo=settings.debug
    )

# Create a separate engine for background tasks to avoid connection pool exhaustion
if is_postgresql:
    background_engine = create_engine(
        connection_string,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,  # Separate pool for background tasks
        max_overflow=20,
        pool_timeout=30,
        echo=settings.debug
    )
else:
    background_engine = create_engine(
        connection_string,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        echo=settings.debug
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BackgroundSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=background_engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_background_db():
    """Get database session for background tasks (separate connection pool)"""
    return BackgroundSessionLocal() 