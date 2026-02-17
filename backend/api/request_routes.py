"""
Request API routes.
"""
import logging
from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from models.request import Request
from models.decision import Decision
from schemas.request_schema import request_schema
from schemas.decision_schema import decision_schema
from services.decision_service import DecisionService
from database import db
from metrics import metrics_collector

logger = logging.getLogger(__name__)

request_bp = Blueprint('requests', __name__, url_prefix='/api/requests')

@request_bp.route('', methods=['POST'])
def submit_request():
    """
    Submit a new request for evaluation.
    
    Request body:
        {
            "amount": float (required, > 0),
            "category": string (required),
            "description": string (optional)
        }
    Returns:
        {
            "request": {...},
            "decision": {...}
        }
    """
    try:
        # Validate input
        data = request_schema.load(request.json)
        logger.info(f"Received request submission: amount={data['amount']}, category={data['category']}")
        
        # Create request
        new_request = Request(
            amount=data['amount'],
            category=data['category'],
            description=data.get('description')
        )
        
        db.session.add(new_request)
        db.session.commit()
        logger.info(f"Created request ID={new_request.id}")
        
        # Evaluate and create decision
        decision = DecisionService.evaluate_and_decide(new_request)
        logger.info(f"Decision for request ID={new_request.id}: {decision.decision}")
        
        # Record decision metric
        metrics_collector.record_decision(decision.decision)
        
        # Return both request and decision
        return jsonify({
            'request': request_schema.dump(new_request),
            'decision': decision_schema.dump(decision)
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@request_bp.route('', methods=['GET'])
def list_requests():
    """
    List all requests.
    
    Returns:
        [
            {
                "id": int,
                "amount": float,
                "category": string,
                "description": string,
                "created_at": datetime
            },
            ...
        ]
    """
    try:
        requests = Request.query.order_by(Request.created_at.desc()).all()
        return jsonify(request_schema.dump(requests, many=True)), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@request_bp.route('/<int:request_id>', methods=['GET'])
def get_request(request_id):
    """
    Get a specific request with its decision.
    
    Returns:
        {
            "request": {...},
            "decision": {...}
        }
    """
    try:
        req = Request.query.get_or_404(request_id)
        
        # Get the most recent decision for this request
        decision = Decision.query.filter_by(request_id=request_id).order_by(Decision.created_at.desc()).first()
        
        return jsonify({
            'request': request_schema.dump(req),
            'decision': decision_schema.dump(decision) if decision else None
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
