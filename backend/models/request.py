"""
Request model - represents a request submitted for evaluation.
"""
from datetime import datetime
from database import db

class Request(db.Model):
    """Request model with amount, category, and description."""
    
    __tablename__ = 'requests'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship to decisions
    decisions = db.relationship('Decision', backref='request', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Request {self.id}: {self.category} ${self.amount}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
