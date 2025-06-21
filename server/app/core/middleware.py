from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings

logger = logging.getLogger(__name__)


def setup_cors(app: FastAPI) -> None:
    """Setup CORS middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )


def setup_trusted_hosts(app: FastAPI) -> None:
    """Setup trusted host middleware for production"""
    if not settings.debug:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", "*.amazonaws.com"]
        )


async def log_requests(request: Request, call_next):
    """Middleware to log all requests"""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response: Response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(
        f"Response: {response.status_code} - "
        f"Time: {process_time:.4f}s - "
        f"Path: {request.url.path}"
    )
    
    # Add processing time to response headers
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware"""
    # Request logging middleware
    app.middleware("http")(log_requests)
    
    # CORS middleware
    setup_cors(app)
    
    # Trusted hosts middleware
    setup_trusted_hosts(app) 