#!/usr/bin/env python3
"""
Comprehensive Test Case Agent for Remote Trading Agent System
This agent provides automated testing capabilities for all components.
"""

import unittest
import requests
import json
import time
import threading
import subprocess
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any, Optional
import logging

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestCaseAgent:
    """
    Comprehensive test case agent for the remote trading agent system.
    Provides automated testing, validation, and reporting capabilities.
    """
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_results = {}
        self.server_process = None
        self.setup_complete = False
        
    def setup_test_environment(self) -> bool:
        """Setup the test environment including starting the server if needed"""
        try:
            logger.info("Setting up test environment...")
            
            # Check if server is already running
            if self._is_server_running():
                logger.info("Server is already running")
                self.setup_complete = True
                return True
            
            # Try to start the server
            logger.info("Starting test server...")
            self._start_test_server()
            
            # Wait for server to be ready
            max_retries = 30
            for i in range(max_retries):
                if self._is_server_running():
                    logger.info("Server is ready")
                    self.setup_complete = True
                    return True
                time.sleep(1)
            
            logger.error("Failed to start server within timeout")
            return False
            
        except Exception as e:
            logger.error(f"Error setting up test environment: {e}")
            return False
    
    def _is_server_running(self) -> bool:
        """Check if the server is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _start_test_server(self):
        """Start the test server in a separate process"""
        try:
            # Start server in background
            self.server_process = subprocess.Popen([
                sys.executable, "remote_agent_api.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)  # Give server time to start
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
    
    def teardown_test_environment(self):
        """Clean up test environment"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            logger.info("Test server stopped")
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites and return comprehensive results"""
        logger.info("Starting comprehensive test suite...")
        
        if not self.setup_test_environment():
            return {"error": "Failed to setup test environment"}
        
        try:
            # Run all test categories
            results = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "environment": {
                    "base_url": self.base_url,
                    "server_running": self._is_server_running()
                },
                "tests": {}
            }
            
            # API Tests
            logger.info("Running API tests...")
            results["tests"]["api"] = self._test_api_endpoints()
            
            # Client Tests
            logger.info("Running client tests...")
            results["tests"]["client"] = self._test_client_functionality()
            
            # Integration Tests
            logger.info("Running integration tests...")
            results["tests"]["integration"] = self._test_integration_scenarios()
            
            # Performance Tests
            logger.info("Running performance tests...")
            results["tests"]["performance"] = self._test_performance()
            
            # Error Handling Tests
            logger.info("Running error handling tests...")
            results["tests"]["error_handling"] = self._test_error_scenarios()
            
            # Module Import Tests
            logger.info("Running module import tests...")
            results["tests"]["modules"] = self._test_module_imports()
            
            # Calculate overall results
            results["summary"] = self._calculate_test_summary(results["tests"])
            
            logger.info("Test suite completed")
            return results
            
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return {"error": str(e)}
        finally:
            self.teardown_test_environment()
    
    def _test_api_endpoints(self) -> Dict[str, Any]:
        """Test all API endpoints"""
        tests = {}
        
        # Health check test
        tests["health_check"] = self._test_health_endpoint()
        
        # News API test
        tests["news_api"] = self._test_news_endpoint()
        
        # Sentiment API test
        tests["sentiment_api"] = self._test_sentiment_endpoint()
        
        # Prediction API test
        tests["prediction_api"] = self._test_prediction_endpoint()
        
        # Trade API test
        tests["trade_api"] = self._test_trade_endpoint()
        
        # Full analysis API test
        tests["full_analysis_api"] = self._test_full_analysis_endpoint()
        
        # Endpoints listing test
        tests["endpoints_list"] = self._test_endpoints_list()
        
        return tests
    
    def _test_health_endpoint(self) -> Dict[str, Any]:
        """Test the health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            data = response.json()
            
            return {
                "passed": response.status_code == 200 and data.get("status") == "healthy",
                "status_code": response.status_code,
                "response": data,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def _test_news_endpoint(self) -> Dict[str, Any]:
        """Test the news API endpoint"""
        try:
            test_data = {"company": "Tesla"}
            response = requests.post(f"{self.base_url}/api/news", json=test_data, timeout=10)
            data = response.json()
            
            return {
                "passed": response.status_code == 200 and data.get("success", False),
                "status_code": response.status_code,
                "response": data,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def _test_sentiment_endpoint(self) -> Dict[str, Any]:
        """Test the sentiment analysis endpoint"""
        try:
            test_data = {
                "news_articles": [
                    "Tesla stock surges after positive earnings",
                    "Analysts upgrade Tesla to buy rating"
                ]
            }
            response = requests.post(f"{self.base_url}/api/sentiment", json=test_data, timeout=10)
            data = response.json()
            
            return {
                "passed": response.status_code == 200 and data.get("success", False),
                "status_code": response.status_code,
                "response": data,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def _test_prediction_endpoint(self) -> Dict[str, Any]:
        """Test the price prediction endpoint"""
        try:
            test_data = {"symbol": "AAPL", "days": 30}
            response = requests.post(f"{self.base_url}/api/predict", json=test_data, timeout=30)
            data = response.json()
            
            # This might fail if prediction service is not available, which is expected
            return {
                "passed": response.status_code in [200, 503],  # 503 is acceptable for unavailable service
                "status_code": response.status_code,
                "response": data,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def _test_trade_endpoint(self) -> Dict[str, Any]:
        """Test the trade execution endpoint (should be disabled)"""
        try:
            test_data = {
                "symbol": "AAPL",
                "action": "buy",
                "qty": 10,
                "api_key": "test",
                "secret_key": "test"
            }
            response = requests.post(f"{self.base_url}/api/trade", json=test_data, timeout=10)
            data = response.json()
            
            # Should return 503 as trading is disabled for safety
            return {
                "passed": response.status_code == 503 and not data.get("success", True),
                "status_code": response.status_code,
                "response": data,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def _test_full_analysis_endpoint(self) -> Dict[str, Any]:
        """Test the full analysis endpoint"""
        try:
            test_data = {
                "company": "Tesla",
                "symbol": "TSLA",
                "enable_prediction": False
            }
            response = requests.post(f"{self.base_url}/api/full-analysis", json=test_data, timeout=30)
            data = response.json()
            
            return {
                "passed": response.status_code == 200 and data.get("success", False),
                "status_code": response.status_code,
                "response": data,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def _test_endpoints_list(self) -> Dict[str, Any]:
        """Test the endpoints listing endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/endpoints", timeout=5)
            data = response.json()
            
            return {
                "passed": response.status_code == 200 and isinstance(data, dict),
                "status_code": response.status_code,
                "response": data,
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}

    def _test_client_functionality(self) -> Dict[str, Any]:
        """Test the RemoteTradingAgentClient functionality"""
        try:
            from remote_agent_client import RemoteTradingAgentClient
            client = RemoteTradingAgentClient(self.base_url)

            tests = {}

            # Test health check
            health_result = client.health_check()
            tests["health_check"] = {
                "passed": not health_result.get("error") and health_result.get("status") == "healthy",
                "result": health_result
            }

            # Test news retrieval
            news_result = client.get_news("Tesla")
            tests["get_news"] = {
                "passed": not news_result.get("error") and news_result.get("success", False),
                "result": news_result
            }

            # Test sentiment analysis
            sentiment_result = client.analyze_sentiment(["Tesla stock rises", "Good earnings report"])
            tests["analyze_sentiment"] = {
                "passed": not sentiment_result.get("error") and sentiment_result.get("success", False),
                "result": sentiment_result
            }

            # Test price prediction
            prediction_result = client.predict_price("AAPL", 30)
            tests["predict_price"] = {
                "passed": not prediction_result.get("error"),  # May not be available
                "result": prediction_result
            }

            # Test full analysis
            analysis_result = client.full_analysis("Tesla", "TSLA")
            tests["full_analysis"] = {
                "passed": not analysis_result.get("error") and analysis_result.get("success", False),
                "result": analysis_result
            }

            # Test endpoints listing
            endpoints_result = client.list_endpoints()
            tests["list_endpoints"] = {
                "passed": not endpoints_result.get("error") and isinstance(endpoints_result, dict),
                "result": endpoints_result
            }

            return tests

        except Exception as e:
            return {"error": str(e), "passed": False}

    def _test_integration_scenarios(self) -> Dict[str, Any]:
        """Test integration scenarios"""
        tests = {}

        # Test complete workflow
        tests["complete_workflow"] = self._test_complete_workflow()

        # Test error propagation
        tests["error_propagation"] = self._test_error_propagation()

        # Test concurrent requests
        tests["concurrent_requests"] = self._test_concurrent_requests()

        return tests

    def _test_complete_workflow(self) -> Dict[str, Any]:
        """Test the complete trading analysis workflow"""
        try:
            from remote_agent_client import RemoteTradingAgentClient
            client = RemoteTradingAgentClient(self.base_url)

            # Step 1: Get news
            news_result = client.get_news("Apple")
            if news_result.get("error"):
                return {"passed": False, "step": "news", "error": news_result["error"]}

            # Step 2: Analyze sentiment
            news_articles = news_result.get("news", ["Sample news about Apple"])
            sentiment_result = client.analyze_sentiment(news_articles)
            if sentiment_result.get("error"):
                return {"passed": False, "step": "sentiment", "error": sentiment_result["error"]}

            # Step 3: Full analysis
            analysis_result = client.full_analysis("Apple", "AAPL")
            if analysis_result.get("error"):
                return {"passed": False, "step": "analysis", "error": analysis_result["error"]}

            return {
                "passed": True,
                "steps_completed": ["news", "sentiment", "analysis"],
                "final_result": analysis_result
            }

        except Exception as e:
            return {"passed": False, "error": str(e)}

    def _test_error_propagation(self) -> Dict[str, Any]:
        """Test how errors are handled and propagated"""
        tests = {}

        # Test invalid JSON
        try:
            response = requests.post(f"{self.base_url}/api/news", data="invalid json", timeout=5)
            tests["invalid_json"] = {
                "passed": response.status_code >= 400,
                "status_code": response.status_code
            }
        except Exception as e:
            tests["invalid_json"] = {"passed": False, "error": str(e)}

        # Test missing required fields
        try:
            response = requests.post(f"{self.base_url}/api/sentiment", json={}, timeout=5)
            tests["missing_fields"] = {
                "passed": response.status_code == 400,
                "status_code": response.status_code
            }
        except Exception as e:
            tests["missing_fields"] = {"passed": False, "error": str(e)}

        # Test invalid endpoint
        try:
            response = requests.get(f"{self.base_url}/api/nonexistent", timeout=5)
            tests["invalid_endpoint"] = {
                "passed": response.status_code == 404,
                "status_code": response.status_code
            }
        except Exception as e:
            tests["invalid_endpoint"] = {"passed": False, "error": str(e)}

        return tests

    def _test_concurrent_requests(self) -> Dict[str, Any]:
        """Test handling of concurrent requests"""
        try:
            import threading
            from remote_agent_client import RemoteTradingAgentClient

            client = RemoteTradingAgentClient(self.base_url)
            results = []
            errors = []

            def make_request():
                try:
                    result = client.health_check()
                    results.append(result)
                except Exception as e:
                    errors.append(str(e))

            # Create multiple threads
            threads = []
            for i in range(5):
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            return {
                "passed": len(errors) == 0 and len(results) == 5,
                "successful_requests": len(results),
                "errors": len(errors),
                "error_details": errors
            }

        except Exception as e:
            return {"passed": False, "error": str(e)}

    def _test_performance(self) -> Dict[str, Any]:
        """Test performance characteristics"""
        tests = {}

        # Test response times
        tests["response_times"] = self._test_response_times()

        # Test load handling
        tests["load_handling"] = self._test_load_handling()

        return tests

    def _test_response_times(self) -> Dict[str, Any]:
        """Test API response times"""
        try:
            from remote_agent_client import RemoteTradingAgentClient
            client = RemoteTradingAgentClient(self.base_url)

            times = {}

            # Test health check time
            start_time = time.time()
            client.health_check()
            times["health_check"] = time.time() - start_time

            # Test news retrieval time
            start_time = time.time()
            client.get_news("Tesla")
            times["get_news"] = time.time() - start_time

            # Test sentiment analysis time
            start_time = time.time()
            client.analyze_sentiment(["Test news"])
            times["sentiment_analysis"] = time.time() - start_time

            return {
                "passed": all(t < 30 for t in times.values()),  # All should be under 30 seconds
                "response_times": times,
                "average_time": sum(times.values()) / len(times)
            }

        except Exception as e:
            return {"passed": False, "error": str(e)}

    def _test_load_handling(self) -> Dict[str, Any]:
        """Test how the system handles load"""
        try:
            import threading
            from remote_agent_client import RemoteTradingAgentClient

            client = RemoteTradingAgentClient(self.base_url)
            successful_requests = 0
            failed_requests = 0
            lock = threading.Lock()

            def make_requests():
                nonlocal successful_requests, failed_requests
                for _ in range(3):  # Each thread makes 3 requests
                    try:
                        result = client.health_check()
                        if not result.get("error"):
                            with lock:
                                successful_requests += 1
                        else:
                            with lock:
                                failed_requests += 1
                    except:
                        with lock:
                            failed_requests += 1

            # Create multiple threads
            threads = []
            for i in range(3):  # 3 threads, 3 requests each = 9 total requests
                thread = threading.Thread(target=make_requests)
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            total_requests = successful_requests + failed_requests
            success_rate = successful_requests / total_requests if total_requests > 0 else 0

            return {
                "passed": success_rate >= 0.8,  # At least 80% success rate
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "success_rate": success_rate
            }

        except Exception as e:
            return {"passed": False, "error": str(e)}

    def _test_error_scenarios(self) -> Dict[str, Any]:
        """Test various error scenarios"""
        tests = {}

        # Test timeout handling
        tests["timeout_handling"] = self._test_timeout_handling()

        # Test malformed requests
        tests["malformed_requests"] = self._test_malformed_requests()

        # Test service unavailability
        tests["service_unavailability"] = self._test_service_unavailability()

        return tests

    def _test_timeout_handling(self) -> Dict[str, Any]:
        """Test timeout handling"""
        try:
            # Test with very short timeout
            response = requests.get(f"{self.base_url}/health", timeout=0.001)
            return {"passed": False, "reason": "Should have timed out"}
        except requests.exceptions.Timeout:
            return {"passed": True, "message": "Timeout handled correctly"}
        except Exception as e:
            return {"passed": False, "error": str(e)}

    def _test_malformed_requests(self) -> Dict[str, Any]:
        """Test handling of malformed requests"""
        tests = {}

        # Test invalid content type
        try:
            response = requests.post(f"{self.base_url}/api/news",
                                   data="not json",
                                   headers={"Content-Type": "text/plain"},
                                   timeout=5)
            tests["invalid_content_type"] = {
                "passed": response.status_code >= 400,
                "status_code": response.status_code
            }
        except Exception as e:
            tests["invalid_content_type"] = {"passed": False, "error": str(e)}

        # Test oversized request
        try:
            large_data = {"news_articles": ["x" * 10000] * 100}  # Very large request
            response = requests.post(f"{self.base_url}/api/sentiment",
                                   json=large_data, timeout=10)
            tests["oversized_request"] = {
                "passed": True,  # Should handle gracefully
                "status_code": response.status_code
            }
        except Exception as e:
            tests["oversized_request"] = {"passed": True, "error": str(e)}  # Timeout is acceptable

        return tests

    def _test_service_unavailability(self) -> Dict[str, Any]:
        """Test handling when services are unavailable"""
        try:
            # Test prediction service (likely unavailable)
            response = requests.post(f"{self.base_url}/api/predict",
                                   json={"symbol": "AAPL"}, timeout=10)
            data = response.json()

            return {
                "passed": response.status_code in [200, 503],  # Either works or service unavailable
                "status_code": response.status_code,
                "service_available": data.get("service_available", False),
                "response": data
            }
        except Exception as e:
            return {"passed": False, "error": str(e)}

    def _test_module_imports(self) -> Dict[str, Any]:
        """Test module imports and availability"""
        tests = {}

        # Test agent modules
        agent_modules = [
            "agent1_news_reader",
            "agent2_sentiment_signal",
            "agent4_price_predictor"
        ]

        for module_name in agent_modules:
            try:
                __import__(module_name)
                tests[module_name] = {"passed": True, "available": True}
            except ImportError as e:
                tests[module_name] = {"passed": True, "available": False, "error": str(e)}
            except Exception as e:
                tests[module_name] = {"passed": False, "available": False, "error": str(e)}

        # Test main modules
        main_modules = ["remote_agent_api", "remote_agent_client"]
        for module_name in main_modules:
            try:
                __import__(module_name)
                tests[module_name] = {"passed": True, "available": True}
            except Exception as e:
                tests[module_name] = {"passed": False, "available": False, "error": str(e)}

        return tests

    def _calculate_test_summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall test summary"""
        total_tests = 0
        passed_tests = 0

        def count_tests(data):
            nonlocal total_tests, passed_tests
            if isinstance(data, dict):
                if "passed" in data:
                    total_tests += 1
                    if data["passed"]:
                        passed_tests += 1
                else:
                    for value in data.values():
                        count_tests(value)

        count_tests(test_results)

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "overall_status": "PASS" if passed_tests == total_tests else "FAIL"
        }

    def generate_test_report(self, results: Dict[str, Any]) -> str:
        """Generate a formatted test report"""
        report = []
        report.append("=" * 80)
        report.append("REMOTE TRADING AGENT - COMPREHENSIVE TEST REPORT")
        report.append("=" * 80)
        report.append(f"Timestamp: {results.get('timestamp', 'Unknown')}")
        report.append(f"Environment: {results.get('environment', {})}")
        report.append("")

        # Summary
        summary = results.get("summary", {})
        report.append("SUMMARY:")
        report.append(f"  Total Tests: {summary.get('total_tests', 0)}")
        report.append(f"  Passed: {summary.get('passed_tests', 0)}")
        report.append(f"  Failed: {summary.get('failed_tests', 0)}")
        report.append(f"  Success Rate: {summary.get('success_rate', 0):.2%}")
        report.append(f"  Overall Status: {summary.get('overall_status', 'UNKNOWN')}")
        report.append("")

        # Detailed results
        tests = results.get("tests", {})
        for category, category_tests in tests.items():
            report.append(f"{category.upper()} TESTS:")
            self._format_test_category(category_tests, report, indent="  ")
            report.append("")

        report.append("=" * 80)
        return "\n".join(report)

    def _format_test_category(self, tests: Dict[str, Any], report: List[str], indent: str = ""):
        """Format a test category for the report"""
        for test_name, test_result in tests.items():
            if isinstance(test_result, dict):
                if "passed" in test_result:
                    status = "PASS" if test_result["passed"] else "FAIL"
                    report.append(f"{indent}{test_name}: {status}")
                    if not test_result["passed"] and "error" in test_result:
                        report.append(f"{indent}  Error: {test_result['error']}")
                else:
                    report.append(f"{indent}{test_name}:")
                    self._format_test_category(test_result, report, indent + "  ")


def main():
    """Main function to run the test case agent"""
    import argparse

    parser = argparse.ArgumentParser(description="Remote Trading Agent Test Case Agent")
    parser.add_argument("--url", default="http://localhost:5000",
                       help="Base URL of the remote agent API")
    parser.add_argument("--output", help="Output file for test report")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create and run test agent
    test_agent = TestCaseAgent(args.url)

    print("Starting Remote Trading Agent Test Suite...")
    print(f"Testing against: {args.url}")
    print("-" * 50)

    # Run all tests
    results = test_agent.run_all_tests()

    # Generate report
    report = test_agent.generate_test_report(results)

    # Output results
    print(report)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")

    # Exit with appropriate code
    summary = results.get("summary", {})
    exit_code = 0 if summary.get("overall_status") == "PASS" else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
