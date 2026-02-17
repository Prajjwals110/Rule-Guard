"""
RuleGuard Flask Application.

Main entry point for the backend API.
"""
import logging
import time
from flask import Flask, g, request
from flask_cors import CORS
from config import Config
from database import db, init_db
from api import request_bp, rule_bp
from api.metrics_routes import metrics_bp
from models import Rule
from logging_config import setup_logging
from middleware import setup_request_id_middleware
from metrics import metrics_collector

logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize logging
    setup_logging(app)
    logger.info("Starting RuleGuard application")
    
    # Initialize CORS
    CORS(app, origins=config_class.CORS_ORIGINS)
    logger.info(f"CORS enabled for origins: {config_class.CORS_ORIGINS}")
    
    # Initialize database
    init_db(app)
    logger.info("Database initialized")
    
    # Setup middleware
    setup_request_id_middleware(app)
    
    # Setup metrics tracking
    if config_class.METRICS_ENABLED:
        setup_metrics_tracking(app)
        logger.info("Metrics collection enabled")
    
    # Register blueprints
    app.register_blueprint(request_bp)
    app.register_blueprint(rule_bp)
    app.register_blueprint(metrics_bp, url_prefix='/api')
    logger.info("Blueprints registered")
    
    # Create seed data
    with app.app_context():
        seed_data()
    
    return app

def setup_metrics_tracking(app):
    """Setup metrics tracking middleware."""
    
    @app.before_request
    def track_request_start():
        """Record request start time."""
        g.start_time = time.time()
    
    @app.after_request
    def track_request_end(response):
        """Record request metrics."""
        # Calculate response time
        if hasattr(g, 'start_time'):
            duration_ms = (time.time() - g.start_time) * 1000
            metrics_collector.record_response_time(duration_ms)
        
        # Record request
        metrics_collector.record_request(request.method, request.path)
        
        # Record errors
        if response.status_code >= 400:
            metrics_collector.record_error(response.status_code)
        
        return response

def seed_data():
    """Create initial seed data if database is empty."""
    # Check if rules already exist
    if Rule.query.count() > 0:
        logger.info("Database already contains rules, skipping seed data")
        return
    
    logger.info("Creating seed data...")
    
    sample_rules = [
        Rule(
            field='amount',
            operator='>',
            value='5000',
            decision='REVIEW',
            priority=1
        ),
        Rule(
            field='amount',
            operator='>',
            value='1000',
            decision='APPROVE',
            priority=2
        ),
        Rule(
            field='category',
            operator='==',
            value='restricted',
            decision='REJECT',
            priority=3
        ),
    ]
    
    db.session.add_all(sample_rules)
    db.session.commit()
    logger.info(f"Created {len(sample_rules)} sample rules")

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*50)
    print("RuleGuard Backend Server")
    print("="*50)
    print("API Endpoints:")
    print("  POST   /api/requests     - Submit new request")
    print("  GET    /api/requests     - List all requests")
    print("  GET    /api/requests/:id - Get specific request")
    print("  POST   /api/rules        - Create new rule")
    print("  GET    /api/rules        - List all rules")
    print("  DELETE /api/rules/:id    - Delete rule")
    print("  GET    /api/metrics      - Get application metrics")
    print("="*50)
    print("Logging: logs/ruleguard.log")
    print("="*50 + "\n")
    
    logger.info("Starting Flask development server")
    app.run(debug=True, port=5000)
