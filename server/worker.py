#!/usr/bin/env python3
"""
RQ Worker script for processing background tasks
"""
import logging
import sys
from rq import Worker, Connection
import redis

from app.core.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def run_worker():
    """Run RQ worker"""
    try:
        # Connect to Redis
        redis_conn = redis.Redis(
            host=getattr(settings, 'redis_host', 'localhost'),
            port=getattr(settings, 'redis_port', 6379),
            db=getattr(settings, 'redis_db', 0),
            decode_responses=False
        )
        
        logger.info("🚀 Starting RQ worker...")
        logger.info(f"📡 Redis connection: {redis_conn.connection_pool.connection_kwargs}")
        
        # Test Redis connection
        redis_conn.ping()
        logger.info("✅ Redis connection successful")
        
        # Create and run worker
        with Connection(redis_conn):
            worker = Worker(['default'])
            logger.info("👷 Worker ready to process tasks")
            worker.work()
            
    except Exception as e:
        logger.error(f"❌ Failed to start worker: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_worker() 