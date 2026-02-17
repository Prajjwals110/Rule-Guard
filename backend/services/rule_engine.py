"""
Rule Engine - Core business logic for evaluating rules.

CRITICAL: No eval() or exec() - uses safe operator mapping.
"""
from typing import Optional, Dict, Any
from models.rule import Rule

class RuleEngine:
    """
    Evaluates requests against rules using deterministic priority-based matching.
    
    Rules are evaluated in ascending priority order (lower number = higher priority).
    First matching rule determines the outcome.
    """
    
    # Safe operator mapping - NO EVAL OR EXEC
    OPERATORS = {
        '<': lambda a, b: a < b,
        '<=': lambda a, b: a <= b,
        '>': lambda a, b: a > b,
        '==': lambda a, b: a == b,
    }
    
    @staticmethod
    def evaluate_request(request_data: Dict[str, Any], rules: list[Rule]) -> Optional[Rule]:
        """
        Evaluate a request against all rules.
        
        Args:
            request_data: Dictionary containing request fields (amount, category)
            rules: List of Rule objects (pre-sorted by priority)
        
        Returns:
            First matching Rule or None if no rule matches
        """
        for rule in rules:
            if RuleEngine._matches_rule(request_data, rule):
                return rule
        
        return None
    
    @staticmethod
    def _matches_rule(request_data: Dict[str, Any], rule: Rule) -> bool:
        """
        Check if a request matches a specific rule.
        
        Args:
            request_data: Dictionary containing request fields
            rule: Rule to evaluate
        
        Returns:
            True if request matches rule, False otherwise
        """
        # Get the field value from request
        field_value = request_data.get(rule.field)
        
        if field_value is None:
            return False
        
        # Get the operator function
        operator_func = RuleEngine.OPERATORS.get(rule.operator)
        
        if operator_func is None:
            return False
        
        # Convert rule value to appropriate type based on field
        try:
            if rule.field == 'amount':
                # For amount, convert to float
                rule_value = float(rule.value)
                field_value = float(field_value)
            else:
                # For category and other string fields, compare as strings
                rule_value = str(rule.value)
                field_value = str(field_value)
            
            # Apply operator
            return operator_func(field_value, rule_value)
        
        except (ValueError, TypeError):
            # If conversion fails, rule doesn't match
            return False
