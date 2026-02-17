"""
Test configuration and fixtures.
"""
import pytest
import sys
import os

# Add parent directory to path so we can import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database import db, reset_db
from models import Rule, Request, Decision

class TestConfig:
    """Test configuration."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = False
    CORS_ORIGINS = ['http://localhost:5173']

@pytest.fixture
def app():
    """Create test Flask application."""
    app = create_app(TestConfig)
    
    with app.app_context():
        reset_db(app)
        yield app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Create database session for tests."""
    with app.app_context():
        yield db.session
        db.session.rollback()
