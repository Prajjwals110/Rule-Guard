"""
Metrics collection for monitoring and observability.

Tracks:
- Request counts by endpoint and method
- Decision outcomes (APPROVED/REJECTED/NEEDS_REVIEW)
- Response times
- Error counts by type
"""
import time
import threading
from collections import defaultdict
from datetime import datetime


class MetricsCollector:
    """Thread-safe metrics collector."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self._lock = threading.Lock()
        self._start_time = time.time()
        self._request_counts = defaultdict(int)  # (method, endpoint) -> count
        self._decision_counts = defaultdict(int)  # decision -> count
        self._error_counts = defaultdict(int)  # status_code -> count
        self._response_times = []  # List of response times
        self._total_requests = 0
    
    def record_request(self, method, endpoint):
        """
        Record an API request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
        """
        with self._lock:
            self._request_counts[(method, endpoint)] += 1
            self._total_requests += 1
    
    def record_decision(self, decision):
        """
        Record a decision outcome.
        
        Args:
            decision: Decision string (APPROVED, REJECTED, NEEDS_REVIEW)
        """
        with self._lock:
            self._decision_counts[decision] += 1
    
    def record_error(self, status_code):
        """
        Record an error response.
        
        Args:
            status_code: HTTP status code (400, 500, etc.)
        """
        with self._lock:
            self._error_counts[status_code] += 1
    
    def record_response_time(self, duration_ms):
        """
        Record response time.
        
        Args:
            duration_ms: Response time in milliseconds
        """
        with self._lock:
            self._response_times.append(duration_ms)
            # Keep only last 1000 response times to prevent memory growth
            if len(self._response_times) > 1000:
                self._response_times = self._response_times[-1000:]
    
    def get_metrics(self):
        """
        Get current metrics snapshot.
        
        Returns:
            dict: Current metrics
        """
        with self._lock:
            # Calculate uptime
            uptime_seconds = int(time.time() - self._start_time)
            
            # Calculate average response time
            avg_response_time = 0
            if self._response_times:
                avg_response_time = sum(self._response_times) / len(self._response_times)
            
            # Format request counts by endpoint
            requests_by_endpoint = {}
            for (method, endpoint), count in self._request_counts.items():
                key = f"{method} {endpoint}"
                requests_by_endpoint[key] = count
            
            return {
                'uptime_seconds': uptime_seconds,
                'total_requests': self._total_requests,
                'requests_by_endpoint': dict(requests_by_endpoint),
                'decisions': dict(self._decision_counts),
                'errors': dict(self._error_counts),
                'response_time_ms': {
                    'average': round(avg_response_time, 2),
                    'samples': len(self._response_times)
                },
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def reset(self):
        """Reset all metrics (useful for testing)."""
        with self._lock:
            self._start_time = time.time()
            self._request_counts.clear()
            self._decision_counts.clear()
            self._error_counts.clear()
            self._response_times.clear()
            self._total_requests = 0


# Global metrics collector instance
metrics_collector = MetricsCollector()
