from typing import Dict, Optional
import time
from datetime import datetime, timedelta

class LLMConnector:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.api_key = api_key
        self.last_request_time = None
        self.request_count = 0
        self.rate_limit = {
            "requests_per_min": 60,
            "tokens_per_min": 90000
        }
    
    def validate_connection(self) -> bool:
        """Validate the connection and API key."""
        try:
            # Implement actual validation logic here
            return True
        except Exception as e:
            return False
    
    def check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        current_time = datetime.now()
        
        if self.last_request_time:
            time_diff = current_time - self.last_request_time
            if time_diff < timedelta(minutes=1):
                if self.request_count >= self.rate_limit["requests_per_min"]:
                    return False
        else:
            self.request_count = 0
            
        self.last_request_time = current_time
        self.request_count += 1
        return True
    
    def get_rate_limits(self) -> Dict[str, int]:
        """Get current rate limits."""
        return self.rate_limit
    
    def set_rate_limits(self, requests_per_min: int, tokens_per_min: int):
        """Update rate limits."""
        self.rate_limit = {
            "requests_per_min": requests_per_min,
            "tokens_per_min": tokens_per_min
        }
