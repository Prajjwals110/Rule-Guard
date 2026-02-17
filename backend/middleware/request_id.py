"""
Request ID middleware for request tracing.

Generates unique request ID for each request and adds to:
- Flask g object (accessible throughout request)
- Response headers (X-Request-ID)
- Log messages (via RequestIdFilter)
"""
import uuid
import logging
from flask import g, request

logger = logging.getLogger(__name__)


def setup_request_id_middleware(app):
    """
    Configure request ID middleware.
    
    Args:
        app: Flask application instance
    """
    
    @app.before_request
    def generate_request_id():
        """Generate unique request ID for each request."""
        # Check if request ID provided by client
        request_id = request.headers.get('X-Request-ID')
        
        # Generate new ID if not provided
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Store in Flask g object
        g.request_id = request_id
        
        # Log incoming request
        logger.info(
            f"Incoming request: {request.method} {request.path} "
            f"from {request.remote_addr}"
        )
    
    @app.after_request
    def add_request_id_header(response):
        """Add request ID to response headers."""
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        return response
    
    logger.info("Request ID middleware initialized")
