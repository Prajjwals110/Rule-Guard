"""
Decision schema for serialization.
"""
from marshmallow import Schema, fields

class DecisionSchema(Schema):
    """Schema for serializing decision output."""
    
    id = fields.Int(dump_only=True)
    request_id = fields.Int(required=True)
    decision = fields.Str(required=True)
    explanation = fields.Str(required=True)
    rule_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

# Create singleton instance for reuse
decision_schema = DecisionSchema()
