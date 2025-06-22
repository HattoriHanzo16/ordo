import redis
from rq import Queue
import logging
from typing import Any, Dict

from app.core.config import settings

logger = logging.getLogger(__name__)


class TaskService:
    """Service for managing background tasks with Redis Queue"""
    
    def __init__(self):
        try:
            # Connect to Redis
            self.redis_conn = redis.Redis(
                host=getattr(settings, 'redis_host', 'localhost'),
                port=getattr(settings, 'redis_port', 6379),
                db=getattr(settings, 'redis_db', 0),
                decode_responses=False  # Keep binary data for file processing
            )
            
            # Create queue
            self.queue = Queue(connection=self.redis_conn)
            logger.info("✅ Task queue initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize task queue: {e}")
            self.redis_conn = None
            self.queue = None
    
    def enqueue_task(self, func, *args, **kwargs) -> str:
        """
        Enqueue a background task
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Job ID string
        """
        if not self.queue:
            logger.error("❌ Task queue not available - falling back to synchronous execution")
            # Fallback to synchronous execution
            func(*args, **kwargs)
            return "sync-fallback"
        
        try:
            job = self.queue.enqueue(func, *args, **kwargs, timeout='30m')  # 30 min timeout
            logger.info(f"📤 Task enqueued successfully. Job ID: {job.id}")
            return job.id
        except Exception as e:
            logger.error(f"❌ Failed to enqueue task: {e}")
            # Fallback to synchronous execution
            func(*args, **kwargs)
            return "sync-fallback"
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a background job"""
        if not self.queue or job_id == "sync-fallback":
            return {"status": "completed", "result": None}
        
        try:
            from rq import Job
            job = Job.fetch(job_id, connection=self.redis_conn)
            return {
                "status": job.get_status(),
                "result": job.result,
                "error": str(job.exc_info) if job.is_failed else None
            }
        except Exception as e:
            logger.error(f"❌ Failed to get job status: {e}")
            return {"status": "unknown", "error": str(e)}


# Global instance
task_service = TaskService() 