#!/usr/bin/env python3
"""
Examples and usage demonstrations for the Test Case Agent
"""

import sys
import os
import time

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_case_agent import TestCaseAgent
from test_mock_agents import create_mock_agents
from test_config import config
from run_comprehensive_tests import ComprehensiveTestRunner

def example_basic_testing():
    """Example: Basic testing with the test case agent"""
    print("🔍 Example 1: Basic Testing")
    print("-" * 50)
    
    # Create test agent
    agent = TestCaseAgent("http://localhost:5000")
    
    # Run a quick health check test
    print("Testing server health...")
    if agent._is_server_running():
        print("✅ Server is running")
        
        # Run a simple API test
        health_result = agent._test_health_endpoint()
        if health_result["passed"]:
            print("✅ Health endpoint test passed")
        else:
            print(f"❌ Health endpoint test failed: {health_result.get('error', 'Unknown error')}")
    else:
        print("❌ Server is not running")
    
    print()

def example_mock_agent_testing():
    """Example: Testing with mock agents"""
    print("🤖 Example 2: Mock Agent Testing")
    print("-" * 50)
    
    # Create mock agents
    mock_agents = create_mock_agents()
    
    # Test news agent
    print("Testing mock news agent...")
    news = mock_agents["news"].get_news("Tesla")
    print(f"✅ Retrieved {len(news)} news articles")
    print(f"   Sample: {news[0][:60]}..." if news else "   No news")
    
    # Test sentiment agent
    print("Testing mock sentiment agent...")
    decision, score = mock_agents["sentiment"].analyze_news(news[:3])
    print(f"✅ Sentiment analysis: {decision} (score: {score:.3f})")
    
    # Test price predictor
    print("Testing mock price predictor...")
    price = mock_agents["predictor"].predict_price("TSLA", 30)
    print(f"✅ Price prediction: ${price}")
    
    print()

def example_comprehensive_testing():
    """Example: Comprehensive testing"""
    print("🚀 Example 3: Comprehensive Testing")
    print("-" * 50)
    
    # Create comprehensive test runner
    runner = ComprehensiveTestRunner()
    
    print("Running comprehensive test suite...")
    print("(This may take a few minutes)")
    
    # Run specific test categories
    categories = ["mock_agents", "configuration", "environment"]
    results = runner.run_all_tests(categories)
    
    # Print summary
    if "main_tests" in results and "summary" in results["main_tests"]:
        summary = results["main_tests"]["summary"]
        print(f"✅ Test Summary:")
        print(f"   Total: {summary.get('total_tests', 0)}")
        print(f"   Passed: {summary.get('passed_tests', 0)}")
        print(f"   Failed: {summary.get('failed_tests', 0)}")
        print(f"   Success Rate: {summary.get('success_rate', 0):.2%}")
    
    print()

def example_performance_testing():
    """Example: Performance testing"""
    print("⚡ Example 4: Performance Testing")
    print("-" * 50)
    
    agent = TestCaseAgent("http://localhost:5000")
    
    if not agent._is_server_running():
        print("❌ Server not running - starting test server...")
        if not agent.setup_test_environment():
            print("❌ Failed to start server")
            return
    
    try:
        print("Running performance tests...")
        
        # Test response times
        perf_results = agent._test_response_times()
        if perf_results["passed"]:
            print("✅ Performance tests passed")
            times = perf_results["response_times"]
            for endpoint, time_taken in times.items():
                print(f"   {endpoint}: {time_taken:.3f}s")
        else:
            print(f"❌ Performance tests failed: {perf_results.get('error', 'Unknown error')}")
        
        # Test load handling
        load_results = agent._test_load_handling()
        if load_results["passed"]:
            print("✅ Load tests passed")
            print(f"   Success rate: {load_results['success_rate']:.2%}")
        else:
            print(f"❌ Load tests failed: {load_results.get('error', 'Unknown error')}")
    
    finally:
        agent.teardown_test_environment()
    
    print()

def example_error_testing():
    """Example: Error scenario testing"""
    print("🚨 Example 5: Error Scenario Testing")
    print("-" * 50)
    
    agent = TestCaseAgent("http://localhost:5000")
    
    if not agent._is_server_running():
        print("❌ Server not running - cannot test error scenarios")
        return
    
    print("Testing error scenarios...")
    
    # Test error propagation
    error_results = agent._test_error_propagation()
    
    for test_name, result in error_results.items():
        if result["passed"]:
            print(f"✅ {test_name}: Handled correctly")
        else:
            print(f"❌ {test_name}: {result.get('error', 'Failed')}")
    
    print()

def example_configuration_testing():
    """Example: Configuration testing"""
    print("⚙️ Example 6: Configuration Testing")
    print("-" * 50)
    
    print("Testing configuration...")
    
    # Validate configuration
    issues = config.validate_config()
    if not issues:
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration issues found:")
        for issue in issues:
            print(f"   - {issue}")
    
    # Show configuration details
    print(f"📋 Configuration details:")
    print(f"   Base URL: {config.BASE_URL}")
    print(f"   Max Response Time: {config.MAX_RESPONSE_TIME}s")
    print(f"   Min Success Rate: {config.MIN_SUCCESS_RATE}")
    print(f"   Test Companies: {len(config.TEST_COMPANIES)}")
    print(f"   Test Endpoints: {len(config.get_test_endpoints())}")
    
    print()

def run_all_examples():
    """Run all examples"""
    print("🎯 Running All Test Case Agent Examples")
    print("=" * 80)
    
    examples = [
        example_basic_testing,
        example_mock_agent_testing,
        example_comprehensive_testing,
        example_performance_testing,
        example_error_testing,
        example_configuration_testing
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"❌ Example {i} failed: {e}")
        
        if i < len(examples):
            print("⏳ Waiting 2 seconds before next example...")
            time.sleep(2)
    
    print("🎉 All examples completed!")

def show_usage():
    """Show usage information"""
    print("📚 Test Case Agent Usage Examples")
    print("=" * 80)
    print()
    print("1. Basic Usage:")
    print("   python test_case_agent.py")
    print("   python test_case_agent.py --url http://localhost:5000")
    print()
    print("2. Comprehensive Testing:")
    print("   python run_comprehensive_tests.py")
    print("   python run_comprehensive_tests.py --categories api client performance")
    print()
    print("3. Mock Agent Testing:")
    print("   python test_mock_agents.py")
    print()
    print("4. Configuration Testing:")
    print("   python test_config.py")
    print()
    print("5. Run Examples:")
    print("   python test_examples.py")
    print("   python test_examples.py --example basic")
    print("   python test_examples.py --example all")
    print()
    print("Environment Variables:")
    print("   TEST_BASE_URL=http://localhost:5000")
    print("   ENABLE_PERFORMANCE_TESTS=true")
    print("   ENABLE_LOAD_TESTS=true")
    print("   MAX_RESPONSE_TIME=30.0")
    print("   MIN_SUCCESS_RATE=0.8")
    print()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Case Agent Examples")
    parser.add_argument("--example", choices=["basic", "mock", "comprehensive", "performance", "error", "config", "all"],
                       default="all", help="Which example to run")
    parser.add_argument("--usage", action="store_true", help="Show usage information")
    
    args = parser.parse_args()
    
    if args.usage:
        show_usage()
        return
    
    example_map = {
        "basic": example_basic_testing,
        "mock": example_mock_agent_testing,
        "comprehensive": example_comprehensive_testing,
        "performance": example_performance_testing,
        "error": example_error_testing,
        "config": example_configuration_testing,
        "all": run_all_examples
    }
    
    example_func = example_map.get(args.example, run_all_examples)
    example_func()

if __name__ == "__main__":
    main()
