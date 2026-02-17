"""
Rule model - represents a decision rule.
"""
from database import db

class Rule(db.Model):
    """Rule model with field, operator, value, decision, and priority."""
    
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(50), nullable=False)  # 'amount' or 'category'
    operator = db.Column(db.String(10), nullable=False)  # '<', '<=', '>', '=='
    value = db.Column(db.String(100), nullable=False)  # Stored as string, converted during evaluation
    decision = db.Column(db.String(20), nullable=False)  # 'APPROVE', 'REJECT', 'REVIEW'
    priority = db.Column(db.Integer, nullable=False)  # Lower number = higher priority
    
    # Relationship to decisions
    decisions = db.relationship('Decision', backref='rule', lazy=True)
    
    def __repr__(self):
        return f'<Rule {self.id}: {self.field} {self.operator} {self.value} → {self.decision} (priority={self.priority})>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'field': self.field,
            'operator': self.operator,
            'value': self.value,
            'decision': self.decision,
            'priority': self.priority
        }
