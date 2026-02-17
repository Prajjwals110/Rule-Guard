"""
Rule validation schema using Marshmallow.
"""
from marshmallow import Schema, fields, validates, ValidationError

class RuleSchema(Schema):
    """Schema for validating rule input."""
    
    id = fields.Int(dump_only=True)
    field = fields.Str(required=True)
    operator = fields.Str(required=True)
    value = fields.Str(required=True)
    decision = fields.Str(required=True)
    priority = fields.Int(required=True)
    
    @validates('field')
    def validate_field(self, value):
        """Ensure field is either 'amount' or 'category'."""
        valid_fields = ['amount', 'category']
        if value not in valid_fields:
            raise ValidationError(f'Field must be one of: {", ".join(valid_fields)}')
    
    @validates('operator')
    def validate_operator(self, value):
        """Ensure operator is valid."""
        valid_operators = ['<', '<=', '>', '==']
        if value not in valid_operators:
            raise ValidationError(f'Operator must be one of: {", ".join(valid_operators)}')
    
    @validates('decision')
    def validate_decision(self, value):
        """Ensure decision is valid."""
        valid_decisions = ['APPROVE', 'REJECT', 'REVIEW']
        if value not in valid_decisions:
            raise ValidationError(f'Decision must be one of: {", ".join(valid_decisions)}')
    
    @validates('priority')
    def validate_priority(self, value):
        """Ensure priority is a positive integer."""
        if value < 0:
            raise ValidationError('Priority must be a non-negative integer')

# Create singleton instance for reuse
rule_schema = RuleSchema()
