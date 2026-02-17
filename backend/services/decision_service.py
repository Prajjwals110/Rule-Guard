"""
Decision Service - Orchestrates request evaluation and decision creation.
"""
import logging
from typing import Dict, Any
from models.request import Request
from models.rule import Rule
from models.decision import Decision
from database import db
from services.rule_engine import RuleEngine

logger = logging.getLogger(__name__)

class DecisionService:
    """
    Service for creating decisions based on request evaluation.
    """
    
    @staticmethod
    def evaluate_and_decide(request: Request) -> Decision:
        """
        Evaluate a request and create a decision.
        
        Args:
            request: Request object to evaluate
        
        Returns:
            Decision object with outcome and explanation
        """
        # Get all rules from database, sorted by priority
        rules = Rule.query.order_by(Rule.priority.asc()).all()
        logger.info(f"Evaluating request ID={request.id} against {len(rules)} rules")
        
        # Prepare request data for evaluation
        request_data = {
            'amount': request.amount,
            'category': request.category
        }
        
        # Find matching rule
        matching_rule = RuleEngine.evaluate_request(request_data, rules)
        logger.info(f"Matching rule for request ID={request.id}: {matching_rule.id if matching_rule else 'None'}")
        
        # Create decision based on result
        if matching_rule:
            decision = DecisionService._create_decision_from_rule(request, matching_rule)
        else:
            decision = DecisionService._create_needs_review_decision(request)
        
        # Save decision to database
        db.session.add(decision)
        db.session.commit()
        
        return decision
    
    @staticmethod
    def _create_decision_from_rule(request: Request, rule: Rule) -> Decision:
        """
        Create a decision based on a matching rule.
        
        Args:
            request: Request being evaluated
            rule: Matching rule
        
        Returns:
            Decision object
        """
        # Map rule decision to final decision format
        decision_map = {
            'APPROVE': 'APPROVED',
            'REJECT': 'REJECTED',
            'REVIEW': 'NEEDS_REVIEW'
        }
        
        decision = decision_map.get(rule.decision, 'NEEDS_REVIEW')
        explanation = DecisionService._generate_explanation(request, rule, decision)
        
        return Decision(
            request_id=request.id,
            decision=decision,
            explanation=explanation,
            rule_id=rule.id
        )
    
    @staticmethod
    def _create_needs_review_decision(request: Request) -> Decision:
        """
        Create a NEEDS_REVIEW decision when no rule matches.
        
        Args:
            request: Request being evaluated
        
        Returns:
            Decision object
        """
        explanation = (
            f"No matching rule found for this request. "
            f"Category: '{request.category}', Amount: ${request.amount:.2f}. "
            f"Manual review required."
        )
        
        return Decision(
            request_id=request.id,
            decision='NEEDS_REVIEW',
            explanation=explanation,
            rule_id=None
        )
    
    @staticmethod
    def _generate_explanation(request: Request, rule: Rule, decision: str) -> str:
        """
        Generate a clear explanation for the decision.
        
        Args:
            request: Request being evaluated
            rule: Matching rule
            decision: Final decision
        
        Returns:
            Human-readable explanation string
        """
        # Format the rule condition
        if rule.field == 'amount':
            condition = f"amount {rule.operator} ${rule.value}"
        else:
            condition = f"{rule.field} {rule.operator} '{rule.value}'"
        
        # Create explanation
        explanation = (
            f"Request {decision.lower()} based on rule: {condition}. "
            f"Your request has {rule.field}="
        )
        
        if rule.field == 'amount':
            explanation += f"${request.amount:.2f}"
        else:
            explanation += f"'{getattr(request, rule.field)}'"
        
        explanation += f", which matches this rule (priority {rule.priority})."
        
        return explanation
