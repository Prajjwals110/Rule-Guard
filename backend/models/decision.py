"""
Decision model - represents the outcome of evaluating a request.
"""
from datetime import datetime
from database import db

class Decision(db.Model):
    """Decision model with request_id, decision, explanation, and rule_id."""
    
    __tablename__ = 'decisions'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)
    decision = db.Column(db.String(20), nullable=False)  # 'APPROVED', 'REJECTED', 'NEEDS_REVIEW'
    explanation = db.Column(db.Text, nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=True)  # Null if no rule matched
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Decision {self.id}: Request {self.request_id} → {self.decision}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'request_id': self.request_id,
            'decision': self.decision,
            'explanation': self.explanation,
            'rule_id': self.rule_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
