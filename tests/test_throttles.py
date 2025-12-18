import pytest
from django.core.cache import cache
from rest_framework.test import APIRequestFactory
from users.throttles import LoginRateThrottle  # ¡CORRECTO ahora!

@pytest.mark.django_db
class TestLoginRateThrottle:
    """Tests for LoginRateThrottle class"""
    
    def test_throttle_allows_requests_below_limit(self):
        """Test that throttle allows requests under the limit"""
        throttle = LoginRateThrottle()
        factory = APIRequestFactory()
        
        # Create a mock request with an IP address
        request = factory.post('/api/login/', {}, REMOTE_ADDR='192.168.1.100')
        
        # Clear cache to start fresh
        cache.clear()
        
        # First request should be allowed
        assert throttle.allow_request(request, None) is True
    
    def test_throttle_blocks_requests_above_limit(self):
        """Test that throttle blocks requests above the limit"""
        throttle = LoginRateThrottle()
        factory = APIRequestFactory()
        
        # Create a mock request with an IP address
        request = factory.post('/api/login/', {}, REMOTE_ADDR='192.168.1.100')
        
        # Clear cache to start fresh
        cache.clear()
        
        # Simulate many requests from the same IP
        # Default rate is usually '5/minute' for SimpleRateThrottle
        allowed_count = 0
        blocked_count = 0
        
        for i in range(10):  # More than the typical limit
            if throttle.allow_request(request, None):
                allowed_count += 1
            else:
                blocked_count += 1
        
        # Should have some allowed and some blocked
        assert allowed_count > 0, "At least some requests should be allowed"
        assert blocked_count > 0, "Some requests should be blocked after limit"
        
        print(f"Requests: {allowed_count} allowed, {blocked_count} blocked")
        
        # Clear cache
        cache.clear()
    
    def test_different_ips_have_separate_limits(self):
        """Test that different IP addresses have separate rate limits"""
        throttle = LoginRateThrottle()
        factory = APIRequestFactory()
        
        # Clear cache
        cache.clear()
        
        # IP 1 makes many requests
        request1 = factory.post('/api/login/', {}, REMOTE_ADDR='192.168.1.100')
        for i in range(10):
            throttle.allow_request(request1, None)
        
        # IP 2 should still be allowed (fresh start)
        request2 = factory.post('/api/login/', {}, REMOTE_ADDR='192.168.1.200')
        assert throttle.allow_request(request2, None) is True
        
        # Clear cache
        cache.clear()
        