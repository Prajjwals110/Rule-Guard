"""
Request validation schema using Marshmallow.
"""
from marshmallow import Schema, fields, validates, ValidationError

class RequestSchema(Schema):
    """Schema for validating request input."""
    
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    category = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    
    @validates('amount')
    def validate_amount(self, value):
        """Ensure amount is greater than 0."""
        if value <= 0:
            raise ValidationError('Amount must be greater than 0')
    
    @validates('category')
    def validate_category(self, value):
        """Ensure category is not empty."""
        if not value or not value.strip():
            raise ValidationError('Category cannot be empty')

# Create singleton instance for reuse
request_schema = RequestSchema()
