"""
Rule API routes.
"""
import logging
from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from models.rule import Rule
from schemas.rule_schema import rule_schema
from database import db

logger = logging.getLogger(__name__)

rule_bp = Blueprint('rules', __name__, url_prefix='/api/rules')

@rule_bp.route('', methods=['POST'])
def create_rule():
    """
    Create a new rule.
    
    Request body:
        {
            "field": "amount" | "category",
            "operator": "<" | "<=" | ">" | "==",
            "value": string,
            "decision": "APPROVE" | "REJECT" | "REVIEW",
            "priority": int
        }
    
    Returns:
        {
            "id": int,
            "field": string,
            "operator": string,
            "value": string,
            "decision": string,
            "priority": int
        }
    """
    try:
        # Validate input
        data = rule_schema.load(request.json)
        logger.info(f"Creating rule: field={data['field']}, operator={data['operator']}, priority={data['priority']}")
        
        # Create rule
        new_rule = Rule(
            field=data['field'],
            operator=data['operator'],
            value=data['value'],
            decision=data['decision'],
            priority=data['priority']
        )
        
        db.session.add(new_rule)
        db.session.commit()
        logger.info(f"Created rule ID={new_rule.id}")
        
        return jsonify(rule_schema.dump(new_rule)), 201
    
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@rule_bp.route('', methods=['GET'])
def list_rules():
    """
    List all rules ordered by priority.
    
    Returns:
        [
            {
                "id": int,
                "field": string,
                "operator": string,
                "value": string,
                "decision": string,
                "priority": int
            },
            ...
        ]
    """
    try:
        logger.info("Listing all rules")
        rules = Rule.query.order_by(Rule.priority.asc()).all()
        logger.info(f"Found {len(rules)} rules")
        return jsonify(rule_schema.dump(rules, many=True)), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@rule_bp.route('/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    """
    Delete a rule.
    
    Returns:
        {
            "message": "Rule deleted successfully"
        }
    """
    try:
        logger.info(f"Deleting rule ID={rule_id}")
        rule = Rule.query.get_or_404(rule_id)
        
        db.session.delete(rule)
        db.session.commit()
        logger.info(f"Successfully deleted rule ID={rule_id}")
        
        return jsonify({'message': 'Rule deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
