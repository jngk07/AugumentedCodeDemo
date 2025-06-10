#!/usr/bin/env python3
"""
Test configuration for the Remote Trading Agent Test Suite
"""

import os
from typing import Dict, Any, List

class TestConfig:
    """Configuration class for test settings"""
    
    def __init__(self):
        # Server configuration
        self.BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:5000")
        self.SERVER_START_TIMEOUT = int(os.getenv("SERVER_START_TIMEOUT", "30"))
        self.REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
        
        # Test configuration
        self.ENABLE_PERFORMANCE_TESTS = os.getenv("ENABLE_PERFORMANCE_TESTS", "true").lower() == "true"
        self.ENABLE_LOAD_TESTS = os.getenv("ENABLE_LOAD_TESTS", "true").lower() == "true"
        self.ENABLE_INTEGRATION_TESTS = os.getenv("ENABLE_INTEGRATION_TESTS", "true").lower() == "true"
        
        # Performance test settings
        self.MAX_RESPONSE_TIME = float(os.getenv("MAX_RESPONSE_TIME", "30.0"))
        self.MIN_SUCCESS_RATE = float(os.getenv("MIN_SUCCESS_RATE", "0.8"))
        self.CONCURRENT_THREADS = int(os.getenv("CONCURRENT_THREADS", "5"))
        self.REQUESTS_PER_THREAD = int(os.getenv("REQUESTS_PER_THREAD", "3"))
        
        # Test data
        self.TEST_COMPANIES = [
            "Tesla", "Apple", "Microsoft", "Google", "Amazon", "Meta", "NVIDIA"
        ]
        self.TEST_SYMBOLS = [
            "TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"
        ]
        self.TEST_NEWS_ARTICLES = [
            "Company reports strong quarterly earnings",
            "Stock price surges after positive analyst upgrade",
            "New product launch receives market approval",
            "CEO announces strategic partnership deal",
            "Market volatility affects trading volume"
        ]
        
        # Expected service availability
        self.EXPECTED_SERVICES = {
            "news": True,  # Should be available with mock data
            "sentiment": True,  # Should be available with mock analysis
            "prediction": False,  # May not be available
            "trader": False  # Should be disabled for safety
        }
        
        # Test categories to run
        self.TEST_CATEGORIES = [
            "api",
            "client", 
            "integration",
            "performance",
            "error_handling",
            "modules"
        ]
        
        # Logging configuration
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", "test_results.log")
        
        # Report configuration
        self.GENERATE_HTML_REPORT = os.getenv("GENERATE_HTML_REPORT", "false").lower() == "true"
        self.REPORT_OUTPUT_DIR = os.getenv("REPORT_OUTPUT_DIR", "test_reports")
        
    def get_test_endpoints(self) -> List[Dict[str, Any]]:
        """Get list of endpoints to test"""
        return [
            {
                "name": "health",
                "method": "GET",
                "path": "/health",
                "expected_status": 200,
                "required_fields": ["status", "message"]
            },
            {
                "name": "news",
                "method": "POST", 
                "path": "/api/news",
                "expected_status": 200,
                "test_data": {"company": "Tesla"},
                "required_fields": ["success", "company", "news"]
            },
            {
                "name": "sentiment",
                "method": "POST",
                "path": "/api/sentiment", 
                "expected_status": 200,
                "test_data": {"news_articles": self.TEST_NEWS_ARTICLES[:2]},
                "required_fields": ["success", "decision", "sentiment_score"]
            },
            {
                "name": "predict",
                "method": "POST",
                "path": "/api/predict",
                "expected_status": [200, 503],  # May not be available
                "test_data": {"symbol": "AAPL", "days": 30},
                "required_fields": ["success"]
            },
            {
                "name": "trade",
                "method": "POST",
                "path": "/api/trade",
                "expected_status": 503,  # Should be disabled
                "test_data": {
                    "symbol": "AAPL",
                    "action": "buy", 
                    "qty": 10,
                    "api_key": "test",
                    "secret_key": "test"
                },
                "required_fields": ["success"]
            },
            {
                "name": "full_analysis",
                "method": "POST",
                "path": "/api/full-analysis",
                "expected_status": 200,
                "test_data": {
                    "company": "Tesla",
                    "symbol": "TSLA",
                    "enable_prediction": False
                },
                "required_fields": ["success", "company", "symbol"]
            },
            {
                "name": "endpoints",
                "method": "GET",
                "path": "/api/endpoints",
                "expected_status": 200,
                "required_fields": []
            }
        ]
    
    def get_error_test_scenarios(self) -> List[Dict[str, Any]]:
        """Get error test scenarios"""
        return [
            {
                "name": "invalid_json",
                "endpoint": "/api/news",
                "method": "POST",
                "data": "invalid json",
                "content_type": "text/plain",
                "expected_status": 400
            },
            {
                "name": "missing_required_field",
                "endpoint": "/api/sentiment",
                "method": "POST", 
                "data": {},
                "expected_status": 400
            },
            {
                "name": "invalid_endpoint",
                "endpoint": "/api/nonexistent",
                "method": "GET",
                "expected_status": 404
            },
            {
                "name": "invalid_method",
                "endpoint": "/health",
                "method": "POST",
                "expected_status": 405
            }
        ]
    
    def get_performance_test_scenarios(self) -> List[Dict[str, Any]]:
        """Get performance test scenarios"""
        return [
            {
                "name": "health_check_performance",
                "endpoint": "/health",
                "method": "GET",
                "max_time": 1.0,
                "iterations": 10
            },
            {
                "name": "news_api_performance", 
                "endpoint": "/api/news",
                "method": "POST",
                "data": {"company": "Tesla"},
                "max_time": 10.0,
                "iterations": 5
            },
            {
                "name": "sentiment_api_performance",
                "endpoint": "/api/sentiment",
                "method": "POST", 
                "data": {"news_articles": self.TEST_NEWS_ARTICLES[:3]},
                "max_time": 5.0,
                "iterations": 5
            }
        ]
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues"""
        issues = []
        
        if self.MAX_RESPONSE_TIME <= 0:
            issues.append("MAX_RESPONSE_TIME must be positive")
        
        if not (0 <= self.MIN_SUCCESS_RATE <= 1):
            issues.append("MIN_SUCCESS_RATE must be between 0 and 1")
        
        if self.CONCURRENT_THREADS <= 0:
            issues.append("CONCURRENT_THREADS must be positive")
        
        if self.REQUESTS_PER_THREAD <= 0:
            issues.append("REQUESTS_PER_THREAD must be positive")
        
        if not self.TEST_COMPANIES:
            issues.append("TEST_COMPANIES cannot be empty")
        
        if not self.TEST_SYMBOLS:
            issues.append("TEST_SYMBOLS cannot be empty")
        
        return issues

# Global configuration instance
config = TestConfig()

# Validate configuration on import
config_issues = config.validate_config()
if config_issues:
    print("Configuration issues found:")
    for issue in config_issues:
        print(f"  - {issue}")
    print("Please fix these issues before running tests.")

if __name__ == "__main__":
    print("Test Configuration:")
    print(f"  Base URL: {config.BASE_URL}")
    print(f"  Performance Tests: {config.ENABLE_PERFORMANCE_TESTS}")
    print(f"  Load Tests: {config.ENABLE_LOAD_TESTS}")
    print(f"  Integration Tests: {config.ENABLE_INTEGRATION_TESTS}")
    print(f"  Max Response Time: {config.MAX_RESPONSE_TIME}s")
    print(f"  Min Success Rate: {config.MIN_SUCCESS_RATE}")
    print(f"  Test Categories: {', '.join(config.TEST_CATEGORIES)}")
    
    print(f"\nEndpoints to test: {len(config.get_test_endpoints())}")
    print(f"Error scenarios: {len(config.get_error_test_scenarios())}")
    print(f"Performance scenarios: {len(config.get_performance_test_scenarios())}")
    
    if config_issues:
        print(f"\nConfiguration issues: {len(config_issues)}")
    else:
        print("\nConfiguration is valid!")
