# Test Case Agent for Remote Trading Agent System

A comprehensive testing framework for the Remote Trading Agent system that provides automated testing, validation, and reporting capabilities.

## 🎯 Overview

The Test Case Agent is a sophisticated testing framework designed to thoroughly test all components of the Remote Trading Agent system, including:

- **API Endpoints**: All Flask API routes and their responses
- **Client Functionality**: RemoteTradingAgentClient operations
- **Integration Testing**: End-to-end workflow testing
- **Performance Testing**: Response times and load handling
- **Error Handling**: Various error scenarios and edge cases
- **Mock Agents**: Simulated agent behavior for testing

## 📁 Files Structure

```
├── test_case_agent.py          # Main test case agent
├── test_mock_agents.py         # Mock agents for testing
├── test_config.py              # Test configuration
├── run_comprehensive_tests.py  # Comprehensive test runner
├── test_examples.py            # Usage examples
└── TEST_CASE_AGENT_README.md   # This file
```

## 🚀 Quick Start

### 1. Basic Testing

```bash
# Run the main test case agent
python test_case_agent.py

# Test against a specific URL
python test_case_agent.py --url http://localhost:5000

# Save report to file
python test_case_agent.py --output test_report.txt
```

### 2. Comprehensive Testing

```bash
# Run all test categories
python run_comprehensive_tests.py

# Run specific test categories
python run_comprehensive_tests.py --categories api client performance

# Custom output directory
python run_comprehensive_tests.py --output-dir ./my_test_reports
```

### 3. Mock Agent Testing

```bash
# Test mock agents independently
python test_mock_agents.py

# Use in your own tests
from test_mock_agents import create_mock_agents
mock_agents = create_mock_agents()
```

### 4. Examples and Demonstrations

```bash
# Run all examples
python test_examples.py

# Run specific example
python test_examples.py --example performance

# Show usage information
python test_examples.py --usage
```

## 🧪 Test Categories

### API Tests
- Health check endpoint
- News retrieval API
- Sentiment analysis API
- Price prediction API
- Trade execution API (disabled)
- Full analysis pipeline
- Endpoints listing

### Client Tests
- RemoteTradingAgentClient functionality
- All client methods
- Error handling in client
- Response parsing

### Integration Tests
- Complete workflow testing
- Error propagation
- Concurrent request handling
- Service interaction

### Performance Tests
- Response time measurement
- Load testing with multiple threads
- Timeout handling
- Resource usage

### Error Handling Tests
- Invalid JSON requests
- Missing required fields
- Invalid endpoints
- Malformed requests
- Service unavailability

### Module Tests
- Agent module imports
- Dependency availability
- Configuration validation

## ⚙️ Configuration

### Environment Variables

```bash
# Server configuration
export TEST_BASE_URL="http://localhost:5000"
export SERVER_START_TIMEOUT=30
export REQUEST_TIMEOUT=30

# Test behavior
export ENABLE_PERFORMANCE_TESTS=true
export ENABLE_LOAD_TESTS=true
export ENABLE_INTEGRATION_TESTS=true

# Performance thresholds
export MAX_RESPONSE_TIME=30.0
export MIN_SUCCESS_RATE=0.8
export CONCURRENT_THREADS=5
export REQUESTS_PER_THREAD=3

# Reporting
export GENERATE_HTML_REPORT=true
export REPORT_OUTPUT_DIR="test_reports"
export LOG_LEVEL="INFO"
```

### Configuration File

The `test_config.py` file contains all configuration options:

```python
from test_config import config

# Access configuration
print(config.BASE_URL)
print(config.MAX_RESPONSE_TIME)
print(config.TEST_COMPANIES)
```

## 🤖 Mock Agents

The test framework includes mock agents that simulate real agent behavior:

### MockNewsAgent
- Provides sample news articles
- Simulates API delays
- Customizable for different companies

### MockSentimentAgent
- Analyzes sentiment using keyword matching
- Returns BUY/SELL/HOLD decisions
- Provides sentiment scores

### MockPricePredictorAgent
- Simulates price predictions
- Uses random walk with trends
- Configurable base prices

### MockTradingAgent
- Always disabled for safety
- Raises exceptions when called

## 📊 Test Reports

The test framework generates multiple report formats:

### JSON Report
```json
{
  "timestamp": "2024-01-15 10:30:00",
  "environment": {...},
  "tests": {...},
  "summary": {
    "total_tests": 25,
    "passed_tests": 23,
    "failed_tests": 2,
    "success_rate": 0.92,
    "overall_status": "PASS"
  }
}
```

### Text Report
```
REMOTE TRADING AGENT - COMPREHENSIVE TEST REPORT
===============================================
Total Tests: 25
Passed: 23
Failed: 2
Success Rate: 92.00%
Overall Status: PASS
```

### HTML Report
Interactive HTML report with detailed results and formatting.

## 🔧 Advanced Usage

### Custom Test Scenarios

```python
from test_case_agent import TestCaseAgent

# Create custom test agent
agent = TestCaseAgent("http://localhost:5000")

# Run specific test categories
results = agent._test_api_endpoints()
performance = agent._test_performance()
```

### Extending the Framework

```python
# Add custom test methods
class CustomTestAgent(TestCaseAgent):
    def _test_custom_scenario(self):
        # Your custom test logic
        return {"passed": True, "custom_data": "value"}
```

### Integration with CI/CD

```bash
# In your CI/CD pipeline
python run_comprehensive_tests.py --no-reports
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Tests failed!"
    exit 1
fi
```

## 🐛 Troubleshooting

### Common Issues

1. **Server Not Running**
   ```
   Error: Server is not running
   Solution: Start the remote agent API server first
   ```

2. **Import Errors**
   ```
   Error: Module not found
   Solution: Ensure all dependencies are installed
   ```

3. **Permission Errors**
   ```
   Error: Cannot write to output directory
   Solution: Check file permissions or use different output directory
   ```

### Debug Mode

```bash
# Enable verbose logging
python test_case_agent.py --verbose

# Set log level
export LOG_LEVEL=DEBUG
python run_comprehensive_tests.py
```

## 📈 Performance Benchmarks

Expected performance characteristics:

- **Health Check**: < 1 second
- **News API**: < 10 seconds
- **Sentiment Analysis**: < 5 seconds
- **Price Prediction**: < 30 seconds (if available)
- **Full Analysis**: < 30 seconds

## 🤝 Contributing

To extend the test framework:

1. Add new test methods to `TestCaseAgent`
2. Update configuration in `test_config.py`
3. Add examples in `test_examples.py`
4. Update this README

## 📝 License

This test framework is part of the Remote Trading Agent system and follows the same license terms.

## 🆘 Support

For issues or questions:

1. Check the troubleshooting section
2. Run examples to understand usage
3. Review configuration options
4. Check log files for detailed error information

---

**Happy Testing! 🎉**
