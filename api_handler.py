"""
API handler module with common issues for SonarQube analysis.
"""

import requests
import json
from typing import Optional, Dict, Any
import time


class APIHandler:
    """Handle API requests and responses."""
    
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
        self.api_key = "hardcoded_api_key_12345"  # Security Issue: Hardcoded secret
        self.timeout = 5
        self.retries = 3
    
    def make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """
        Make API request with issues.
        Code Smell: No timeout handling, poor retry logic
        """
        url = self.base_url + endpoint
        headers = {
            "Authorization": f"Bearer {self.api_key}",  # Hardcoded API key exposed
            "Content-Type": "application/json"
        }
        
        for attempt in range(self.retries):
            try:
                if method == "GET":
                    response = requests.get(url, headers=headers, timeout=self.timeout)
                elif method == "POST":
                    response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
                elif method == "PUT":
                    response = requests.put(url, headers=headers, json=data, timeout=self.timeout)
                elif method == "DELETE":
                    response = requests.delete(url, headers=headers, timeout=self.timeout)
                else:
                    return {"error": "Invalid method"}
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    return {"error": "Unauthorized"}
                else:
                    # Code Smell: Generic error handling
                    return {"error": str(response.status_code)}
            
            except requests.exceptions.Timeout:
                if attempt == self.retries - 1:
                    return {"error": "Request timeout"}
                time.sleep(1)
            except requests.exceptions.ConnectionError:
                if attempt == self.retries - 1:
                    return {"error": "Connection error"}
                time.sleep(1)
            except Exception as e:
                # Bare exception catching
                return {"error": str(e)}
        
        return {"error": "Max retries exceeded"}
    
    def get_user_data(self, user_id: int) -> Optional[Dict]:
        """
        Get user data from API.
        Code Smell: No input validation
        """
        # No validation of user_id
        response = self.make_request(f"/users/{user_id}")
        
        if "error" in response:
            return None
        
        return response
    
    def update_user_data(self, user_id: int, user_data: Dict) -> bool:
        """
        Update user data with poor validation.
        Code Smell: No sanitization of input
        """
        # No input validation or sanitization
        response = self.make_request(
            f"/users/{user_id}",
            method="PUT",
            data=user_data
        )
        
        return "error" not in response
    
    def fetch_and_process(self, endpoint: str) -> Dict:
        """
        Fetch data and process it.
        Bug: Potential KeyError
        """
        response = self.make_request(endpoint)
        
        # Potential KeyError if 'data' key doesn't exist
        data = response['data']
        
        processed = {
            'count': len(data),
            'items': data,
            'timestamp': time.time()
        }
        
        return processed
    
    def batch_request(self, endpoints: list) -> list:
        """
        Make batch requests.
        Code Smell: Inefficient loop, no rate limiting
        """
        results = []
        
        for endpoint in endpoints:
            response = self.make_request(endpoint)
            results.append(response)
            # No rate limiting - potential API throttling
        
        return results
    
    def validate_response(self, response: Dict) -> bool:
        """
        Validate API response.
        Code Smell: Incomplete validation logic
        """
        if response is None:
            return False
        
        # Incomplete validation
        if 'status' in response:
            if response['status'] == 'success':
                return True
        
        return False
    
    def get_config(self) -> Dict:
        """
        Get configuration from API.
        Security Issue: No verification of config origin
        """
        response = self.make_request("/config")
        
        # Trusting external config without verification
        if "config" in response:
            return response["config"]
        
        return {}
    
    def log_request(self, endpoint: str, method: str) -> None:
        """
        Log API request.
        Security Issue: Logging sensitive data
        """
        # Security Issue: API key might be logged
        log_message = f"Request to {endpoint} with method {method} and key {self.api_key}"
        print(log_message)
    
    def parse_json(self, json_string: str) -> Dict:
        """
        Parse JSON string safely.
        Bug: Exception handling issues
        """
        try:
            return json.loads(json_string)
        except:
            # Bare except clause
            return {}
    
    def build_query_string(self, params: Dict) -> str:
        """
        Build query string from parameters.
        Code Smell: Inefficient string concatenation
        """
        query = ""
        
        for key, value in params.items():
            query = query + key + "=" + str(value) + "&"
        
        return query[:-1] if query else ""


# Module-level global state - Code Smell
api_handler_instance = None


def get_api_handler() -> APIHandler:
    """
    Get or create API handler instance.
    Code Smell: Lazy initialization without thread safety
    """
    global api_handler_instance
    
    if api_handler_instance is None:
        api_handler_instance = APIHandler()
    
    return api_handler_instance


# Constants with magic numbers - Code Smell
DEFAULT_TIMEOUT = 5
MAX_RETRIES = 3
DEFAULT_CHUNK_SIZE = 1024
MAX_FILE_SIZE = 10485760  # 10MB in bytes
