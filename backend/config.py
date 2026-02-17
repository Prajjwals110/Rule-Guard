"""
Configuration settings for RuleGuard backend.
"""
import os

class Config:
    """Base configuration."""
    
    # Database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'ruleguard.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # CORS
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/ruleguard.log')
    
    # Metrics configuration
    METRICS_ENABLED = os.environ.get('METRICS_ENABLED', 'true').lower() == 'true'

