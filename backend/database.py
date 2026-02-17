"""
Database setup and initialization.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize database with Flask app."""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")

def reset_db(app):
    """Reset database (useful for testing)."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset successfully")
