"""
Logging configuration for RuleGuard.

Provides structured logging with:
- File rotation (max 10MB, keep 5 backups)
- Console and file output
- Request ID tracking
- Structured format with timestamps
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import g, has_request_context


class RequestIdFilter(logging.Filter):
    """Add request ID to log records."""
    
    def filter(self, record):
        """Add request_id attribute to log record."""
        if has_request_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = 'N/A'
        return True


def setup_logging(app):
    """
    Configure application logging.
    
    Args:
        app: Flask application instance
    """
    # Get configuration
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    log_file = app.config.get('LOG_FILE', 'logs/ruleguard.log')
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Create formatter with request ID
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(request_id)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIdFilter())
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestIdFilter())
    root_logger.addHandler(file_handler)
    
    # Log startup
    app.logger.info(f"Logging initialized - Level: {log_level}, File: {log_file}")
