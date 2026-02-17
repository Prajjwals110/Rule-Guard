"""
Tests for decision service.
"""
import pytest
from models import Rule, Request, Decision
from services.decision_service import DecisionService
from database import db

class TestDecisionService:
    """Test decision service logic."""
    
    def test_decision_with_matching_rule(self, app, db_session):
        """Test decision creation when a rule matches."""
        # Create a rule
        rule = Rule(
            field='amount',
            operator='>',
            value='1000',
            decision='APPROVE',
            priority=1
        )
        db_session.add(rule)
        db_session.commit()
        
        # Create a request
        request = Request(
            amount=1500,
            category='travel',
            description='Conference trip'
        )
        db_session.add(request)
        db_session.commit()
        
        # Evaluate and create decision
        decision = DecisionService.evaluate_and_decide(request)
        
        assert decision is not None
        assert decision.decision == 'APPROVED'
        assert decision.rule_id == rule.id
        assert 'amount > $1000' in decision.explanation
        assert decision.request_id == request.id
    
    def test_decision_needs_review_no_match(self, app, db_session):
        """Test NEEDS_REVIEW decision when no rule matches."""
        # Create a rule that won't match
        rule = Rule(
            field='amount',
            operator='>',
            value='5000',
            decision='REVIEW',
            priority=1
        )
        db_session.add(rule)
        db_session.commit()
        
        # Create a request that doesn't match
        request = Request(
            amount=500,
            category='office',
            description='Office supplies'
        )
        db_session.add(request)
        db_session.commit()
        
        # Evaluate and create decision
        decision = DecisionService.evaluate_and_decide(request)
        
        assert decision is not None
        assert decision.decision == 'NEEDS_REVIEW'
        assert decision.rule_id is None
        assert 'No matching rule found' in decision.explanation
        assert decision.request_id == request.id
    
    def test_decision_reject(self, app, db_session):
        """Test REJECTED decision."""
        # Create a reject rule
        rule = Rule(
            field='category',
            operator='==',
            value='restricted',
            decision='REJECT',
            priority=1
        )
        db_session.add(rule)
        db_session.commit()
        
        # Create a request that matches
        request = Request(
            amount=500,
            category='restricted',
            description='Restricted item'
        )
        db_session.add(request)
        db_session.commit()
        
        # Evaluate and create decision
        decision = DecisionService.evaluate_and_decide(request)
        
        assert decision is not None
        assert decision.decision == 'REJECTED'
        assert decision.rule_id == rule.id
        assert 'category == \'restricted\'' in decision.explanation
    
    def test_decision_persistence(self, app, db_session):
        """Test that decisions are persisted to database."""
        # Create a rule
        rule = Rule(
            field='amount',
            operator='<',
            value='100',
            decision='APPROVE',
            priority=1
        )
        db_session.add(rule)
        db_session.commit()
        
        # Create a request
        request = Request(
            amount=50,
            category='office'
        )
        db_session.add(request)
        db_session.commit()
        
        # Evaluate and create decision
        decision = DecisionService.evaluate_and_decide(request)
        
        # Verify decision is in database
        saved_decision = Decision.query.filter_by(request_id=request.id).first()
        assert saved_decision is not None
        assert saved_decision.id == decision.id
        assert saved_decision.decision == 'APPROVED'
    
    def test_explanation_generation(self, app, db_session):
        """Test that explanations are clear and informative."""
        # Create a rule
        rule = Rule(
            field='amount',
            operator='<=',
            value='1000',
            decision='APPROVE',
            priority=5
        )
        db_session.add(rule)
        db_session.commit()
        
        # Create a request
        request = Request(
            amount=750,
            category='travel'
        )
        db_session.add(request)
        db_session.commit()
        
        # Evaluate and create decision
        decision = DecisionService.evaluate_and_decide(request)
        
        # Check explanation contains key information
        assert 'amount <= $1000' in decision.explanation
        assert '$750.00' in decision.explanation
        assert 'priority 5' in decision.explanation
        assert 'approved' in decision.explanation.lower()
