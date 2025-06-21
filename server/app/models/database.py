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
    # PostgreSQL configuration
    engine = create_engine(
        connection_string,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.debug
    )
else:
    # SQLite configuration (fallback)
    engine = create_engine(
        connection_string,
        connect_args={"check_same_thread": False},
        echo=settings.debug
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 