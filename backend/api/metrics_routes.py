"""
API routes for metrics and monitoring.
"""
import logging
from flask import Blueprint, jsonify
from metrics import metrics_collector

logger = logging.getLogger(__name__)

metrics_bp = Blueprint('metrics', __name__)


@metrics_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Get current application metrics.
    
    Returns:
        JSON response with metrics data
    """
    logger.info("Metrics requested")
    
    try:
        metrics = metrics_collector.get_metrics()
        return jsonify(metrics), 200
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to retrieve metrics'}), 500
