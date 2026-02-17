"""
Tests for invalid input and edge cases.
"""
import pytest
import json

class TestInvalidInput:
    """Test validation and error handling."""
    
    def test_amount_zero_rejected(self, client):
        """Test that amount = 0 is rejected."""
        response = client.post('/api/requests', 
            json={'amount': 0, 'category': 'office'},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Validation failed' in data['error']
    
    def test_amount_negative_rejected(self, client):
        """Test that negative amount is rejected."""
        response = client.post('/api/requests',
            json={'amount': -100, 'category': 'office'},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_missing_amount_rejected(self, client):
        """Test that missing amount is rejected."""
        response = client.post('/api/requests',
            json={'category': 'office'},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_missing_category_rejected(self, client):
        """Test that missing category is rejected."""
        response = client.post('/api/requests',
            json={'amount': 500},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_empty_category_rejected(self, client):
        """Test that empty category is rejected."""
        response = client.post('/api/requests',
            json={'amount': 500, 'category': ''},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_invalid_rule_field_rejected(self, client):
        """Test that invalid rule field is rejected."""
        response = client.post('/api/rules',
            json={
                'field': 'invalid_field',
                'operator': '>',
                'value': '1000',
                'decision': 'APPROVE',
                'priority': 1
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_invalid_rule_operator_rejected(self, client):
        """Test that invalid operator is rejected."""
        response = client.post('/api/rules',
            json={
                'field': 'amount',
                'operator': '!=',
                'value': '1000',
                'decision': 'APPROVE',
                'priority': 1
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_invalid_rule_decision_rejected(self, client):
        """Test that invalid decision is rejected."""
        response = client.post('/api/rules',
            json={
                'field': 'amount',
                'operator': '>',
                'value': '1000',
                'decision': 'INVALID',
                'priority': 1
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_negative_priority_rejected(self, client):
        """Test that negative priority is rejected."""
        response = client.post('/api/rules',
            json={
                'field': 'amount',
                'operator': '>',
                'value': '1000',
                'decision': 'APPROVE',
                'priority': -1
            },
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

class TestEdgeCases:
    """Test edge cases and rule interactions."""
    
    def test_adding_rule_does_not_break_existing(self, client):
        """Test that adding a new rule doesn't break existing rule evaluation."""
        # Create initial rule
        response1 = client.post('/api/rules',
            json={
                'field': 'amount',
                'operator': '>',
                'value': '1000',
                'decision': 'APPROVE',
                'priority': 1
            },
            content_type='application/json'
        )
        assert response1.status_code == 201
        
        # Submit request that matches first rule
        response2 = client.post('/api/requests',
            json={'amount': 1500, 'category': 'office'},
            content_type='application/json'
        )
        assert response2.status_code == 201
        data2 = json.loads(response2.data)
        assert data2['decision']['decision'] == 'APPROVED'
        
        # Add a new rule with higher priority
        response3 = client.post('/api/rules',
            json={
                'field': 'amount',
                'operator': '>',
                'value': '500',
                'decision': 'REVIEW',
                'priority': 0
            },
            content_type='application/json'
        )
        assert response3.status_code == 201
        
        # Submit same request again - should now match new rule
        response4 = client.post('/api/requests',
            json={'amount': 1500, 'category': 'office'},
            content_type='application/json'
        )
        assert response4.status_code == 201
        data4 = json.loads(response4.data)
        assert data4['decision']['decision'] == 'NEEDS_REVIEW'
    
    def test_valid_request_with_optional_description(self, client):
        """Test that description is truly optional."""
        response = client.post('/api/requests',
            json={'amount': 500, 'category': 'office', 'description': 'Test description'},
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['request']['description'] == 'Test description'
        
        # Without description
        response2 = client.post('/api/requests',
            json={'amount': 500, 'category': 'office'},
            content_type='application/json'
        )
        
        assert response2.status_code == 201
