"""
Tests for rule evaluation logic.
"""
import pytest
from models import Rule
from services.rule_engine import RuleEngine

class TestRuleEngine:
    """Test rule engine evaluation logic."""
    
    def test_amount_greater_than(self):
        """Test amount > value rule."""
        rule = Rule(field='amount', operator='>', value='1000', decision='APPROVE', priority=1)
        request_data = {'amount': 1500, 'category': 'travel'}
        
        result = RuleEngine._matches_rule(request_data, rule)
        assert result is True
    
    def test_amount_greater_than_false(self):
        """Test amount > value rule when condition is false."""
        rule = Rule(field='amount', operator='>', value='1000', decision='APPROVE', priority=1)
        request_data = {'amount': 500, 'category': 'travel'}
        
        result = RuleEngine._matches_rule(request_data, rule)
        assert result is False
    
    def test_amount_less_than(self):
        """Test amount < value rule."""
        rule = Rule(field='amount', operator='<', value='500', decision='APPROVE', priority=1)
        request_data = {'amount': 300, 'category': 'office'}
        
        result = RuleEngine._matches_rule(request_data, rule)
        assert result is True
    
    def test_amount_less_than_or_equal(self):
        """Test amount <= value rule."""
        rule = Rule(field='amount', operator='<=', value='1000', decision='APPROVE', priority=1)
        request_data = {'amount': 1000, 'category': 'office'}
        
        result = RuleEngine._matches_rule(request_data, rule)
        assert result is True
    
    def test_category_equals(self):
        """Test category == value rule."""
        rule = Rule(field='category', operator='==', value='restricted', decision='REJECT', priority=1)
        request_data = {'amount': 500, 'category': 'restricted'}
        
        result = RuleEngine._matches_rule(request_data, rule)
        assert result is True
    
    def test_category_equals_false(self):
        """Test category == value rule when condition is false."""
        rule = Rule(field='category', operator='==', value='restricted', decision='REJECT', priority=1)
        request_data = {'amount': 500, 'category': 'office'}
        
        result = RuleEngine._matches_rule(request_data, rule)
        assert result is False
    
    def test_priority_ordering(self):
        """Test that rules are evaluated in priority order."""
        # Rules should be pre-sorted by priority (as they come from database)
        rules = [
            Rule(field='amount', operator='>', value='500', decision='REVIEW', priority=1),
            Rule(field='amount', operator='>', value='1000', decision='APPROVE', priority=2),
        ]
        
        request_data = {'amount': 1500, 'category': 'travel'}
        
        # Should match the first rule by priority (priority=1)
        result = RuleEngine.evaluate_request(request_data, rules)
        assert result is not None
        assert result.priority == 1
        assert result.decision == 'REVIEW'
    
    def test_first_matching_rule_wins(self):
        """Test that first matching rule (by priority) determines outcome."""
        rules = [
            Rule(field='amount', operator='>', value='2000', decision='REJECT', priority=1),
            Rule(field='amount', operator='>', value='1000', decision='APPROVE', priority=2),
            Rule(field='amount', operator='>', value='500', decision='REVIEW', priority=3),
        ]
        
        request_data = {'amount': 1500, 'category': 'travel'}
        
        # Should match priority=2 rule (amount > 1000)
        result = RuleEngine.evaluate_request(request_data, rules)
        assert result is not None
        assert result.priority == 2
        assert result.decision == 'APPROVE'
    
    def test_no_matching_rule(self):
        """Test that None is returned when no rule matches."""
        rules = [
            Rule(field='amount', operator='>', value='5000', decision='REVIEW', priority=1),
            Rule(field='category', operator='==', value='restricted', decision='REJECT', priority=2),
        ]
        
        request_data = {'amount': 500, 'category': 'office'}
        
        result = RuleEngine.evaluate_request(request_data, rules)
        assert result is None
    
    def test_invalid_operator(self):
        """Test that invalid operators don't match."""
        rule = Rule(field='amount', operator='!=', value='1000', decision='APPROVE', priority=1)
        request_data = {'amount': 1500, 'category': 'travel'}
        
        result = RuleEngine._matches_rule(request_data, rule)
        assert result is False
    
    def test_missing_field(self):
        """Test that missing fields don't match."""
        rule = Rule(field='amount', operator='>', value='1000', decision='APPROVE', priority=1)
        request_data = {'category': 'travel'}  # Missing amount
        
        result = RuleEngine._matches_rule(request_data, rule)
        assert result is False
