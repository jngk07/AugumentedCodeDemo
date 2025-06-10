#!/usr/bin/env python3
"""
Comprehensive test runner for the Remote Trading Agent system.
This script orchestrates all testing activities and generates detailed reports.
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_case_agent import TestCaseAgent
from test_config import config
from test_mock_agents import create_mock_agents

class ComprehensiveTestRunner:
    """Orchestrates comprehensive testing of the remote trading agent system"""
    
    def __init__(self, base_url: str = None, output_dir: str = None):
        self.base_url = base_url or config.BASE_URL
        self.output_dir = Path(output_dir or config.REPORT_OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        
        self.test_agent = TestCaseAgent(self.base_url)
        self.mock_agents = create_mock_agents()
        
        self.start_time = None
        self.end_time = None
        
    def run_all_tests(self, categories: list = None) -> dict:
        """Run all test categories"""
        self.start_time = datetime.now()
        
        print("🚀 Starting Comprehensive Remote Trading Agent Test Suite")
        print("=" * 80)
        print(f"Target URL: {self.base_url}")
        print(f"Output Directory: {self.output_dir}")
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Determine which categories to run
        categories_to_run = categories or config.TEST_CATEGORIES
        
        # Run the main test suite
        print("\n📋 Running main test suite...")
        main_results = self.test_agent.run_all_tests()
        
        # Run additional specialized tests
        additional_results = {}
        
        if "mock_agents" in categories_to_run:
            print("\n🤖 Testing mock agents...")
            additional_results["mock_agents"] = self._test_mock_agents()
        
        if "configuration" in categories_to_run:
            print("\n⚙️  Testing configuration...")
            additional_results["configuration"] = self._test_configuration()
        
        if "environment" in categories_to_run:
            print("\n🌍 Testing environment...")
            additional_results["environment"] = self._test_environment()
        
        # Combine all results
        combined_results = {
            "test_run_info": {
                "start_time": self.start_time.isoformat(),
                "base_url": self.base_url,
                "categories_run": categories_to_run,
                "test_runner_version": "1.0.0"
            },
            "main_tests": main_results,
            "additional_tests": additional_results
        }
        
        self.end_time = datetime.now()
        combined_results["test_run_info"]["end_time"] = self.end_time.isoformat()
        combined_results["test_run_info"]["duration_seconds"] = (
            self.end_time - self.start_time
        ).total_seconds()
        
        return combined_results
    
    def _test_mock_agents(self) -> dict:
        """Test the mock agents functionality"""
        results = {}
        
        try:
            # Test news agent
            news_agent = self.mock_agents["news"]
            news = news_agent.get_news("TestCompany")
            results["news_agent"] = {
                "passed": isinstance(news, list) and len(news) > 0,
                "articles_count": len(news),
                "sample_article": news[0] if news else None
            }
        except Exception as e:
            results["news_agent"] = {"passed": False, "error": str(e)}
        
        try:
            # Test sentiment agent
            sentiment_agent = self.mock_agents["sentiment"]
            decision, score = sentiment_agent.analyze_news(["Positive news about company"])
            results["sentiment_agent"] = {
                "passed": decision in ["BUY", "SELL", "HOLD"] and isinstance(score, (int, float)),
                "decision": decision,
                "score": score
            }
        except Exception as e:
            results["sentiment_agent"] = {"passed": False, "error": str(e)}
        
        try:
            # Test price predictor agent
            predictor_agent = self.mock_agents["predictor"]
            price = predictor_agent.predict_price("AAPL", 30)
            results["predictor_agent"] = {
                "passed": isinstance(price, (int, float)) and price > 0,
                "predicted_price": price
            }
        except Exception as e:
            results["predictor_agent"] = {"passed": False, "error": str(e)}
        
        try:
            # Test trading agent (should fail)
            trading_agent = self.mock_agents["trader"]
            trading_agent.execute_trade("AAPL", "buy", 10, "test", "test")
            results["trading_agent"] = {"passed": False, "error": "Trading should be disabled"}
        except Exception as e:
            results["trading_agent"] = {"passed": True, "error": str(e)}
        
        return results
    
    def _test_configuration(self) -> dict:
        """Test configuration validity"""
        results = {}
        
        # Test config validation
        config_issues = config.validate_config()
        results["config_validation"] = {
            "passed": len(config_issues) == 0,
            "issues": config_issues
        }
        
        # Test environment variables
        env_vars = [
            "TEST_BASE_URL", "SERVER_START_TIMEOUT", "REQUEST_TIMEOUT",
            "ENABLE_PERFORMANCE_TESTS", "ENABLE_LOAD_TESTS"
        ]
        
        env_results = {}
        for var in env_vars:
            env_results[var] = {
                "set": var in os.environ,
                "value": os.environ.get(var, "Not set")
            }
        
        results["environment_variables"] = env_results
        
        # Test test data validity
        results["test_data"] = {
            "companies_count": len(config.TEST_COMPANIES),
            "symbols_count": len(config.TEST_SYMBOLS),
            "news_articles_count": len(config.TEST_NEWS_ARTICLES),
            "endpoints_count": len(config.get_test_endpoints())
        }
        
        return results
    
    def _test_environment(self) -> dict:
        """Test the runtime environment"""
        results = {}
        
        # Test Python version
        results["python_version"] = {
            "version": sys.version,
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "compatible": sys.version_info >= (3, 7)
        }
        
        # Test required modules
        required_modules = [
            "requests", "flask", "json", "threading", "subprocess",
            "unittest", "logging", "pathlib"
        ]
        
        module_results = {}
        for module in required_modules:
            try:
                __import__(module)
                module_results[module] = {"available": True}
            except ImportError as e:
                module_results[module] = {"available": False, "error": str(e)}
        
        results["required_modules"] = module_results
        
        # Test file system permissions
        try:
            test_file = self.output_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            results["file_system"] = {"writable": True}
        except Exception as e:
            results["file_system"] = {"writable": False, "error": str(e)}
        
        return results
    
    def generate_reports(self, results: dict):
        """Generate comprehensive test reports"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate JSON report
        json_file = self.output_dir / f"test_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"📄 JSON report saved: {json_file}")
        
        # Generate text report
        text_file = self.output_dir / f"test_report_{timestamp}.txt"
        text_report = self._generate_text_report(results)
        with open(text_file, 'w') as f:
            f.write(text_report)
        print(f"📄 Text report saved: {text_file}")
        
        # Generate HTML report if enabled
        if config.GENERATE_HTML_REPORT:
            html_file = self.output_dir / f"test_report_{timestamp}.html"
            html_report = self._generate_html_report(results)
            with open(html_file, 'w') as f:
                f.write(html_report)
            print(f"📄 HTML report saved: {html_file}")
        
        return {
            "json_report": str(json_file),
            "text_report": str(text_file),
            "html_report": str(html_file) if config.GENERATE_HTML_REPORT else None
        }
    
    def _generate_text_report(self, results: dict) -> str:
        """Generate a detailed text report"""
        lines = []
        lines.append("COMPREHENSIVE REMOTE TRADING AGENT TEST REPORT")
        lines.append("=" * 80)
        
        # Test run info
        info = results.get("test_run_info", {})
        lines.append(f"Start Time: {info.get('start_time', 'Unknown')}")
        lines.append(f"End Time: {info.get('end_time', 'Unknown')}")
        lines.append(f"Duration: {info.get('duration_seconds', 0):.2f} seconds")
        lines.append(f"Base URL: {info.get('base_url', 'Unknown')}")
        lines.append(f"Categories: {', '.join(info.get('categories_run', []))}")
        lines.append("")
        
        # Main test results
        main_tests = results.get("main_tests", {})
        if "summary" in main_tests:
            summary = main_tests["summary"]
            lines.append("MAIN TEST SUMMARY:")
            lines.append(f"  Total Tests: {summary.get('total_tests', 0)}")
            lines.append(f"  Passed: {summary.get('passed_tests', 0)}")
            lines.append(f"  Failed: {summary.get('failed_tests', 0)}")
            lines.append(f"  Success Rate: {summary.get('success_rate', 0):.2%}")
            lines.append(f"  Status: {summary.get('overall_status', 'UNKNOWN')}")
            lines.append("")
        
        # Additional test results
        additional = results.get("additional_tests", {})
        if additional:
            lines.append("ADDITIONAL TEST RESULTS:")
            for category, category_results in additional.items():
                lines.append(f"  {category.upper()}:")
                self._format_results_recursive(category_results, lines, "    ")
            lines.append("")
        
        lines.append("=" * 80)
        return "\n".join(lines)
    
    def _format_results_recursive(self, data, lines, indent):
        """Recursively format test results"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and "passed" in value:
                    status = "PASS" if value["passed"] else "FAIL"
                    lines.append(f"{indent}{key}: {status}")
                    if not value["passed"] and "error" in value:
                        lines.append(f"{indent}  Error: {value['error']}")
                else:
                    lines.append(f"{indent}{key}:")
                    self._format_results_recursive(value, lines, indent + "  ")
    
    def _generate_html_report(self, results: dict) -> str:
        """Generate an HTML report"""
        # Basic HTML template - could be enhanced with CSS/JS
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Remote Trading Agent Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; }}
                .pass {{ color: green; }}
                .fail {{ color: red; }}
                .section {{ margin: 20px 0; }}
                pre {{ background-color: #f5f5f5; padding: 10px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Remote Trading Agent Test Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>Test Results</h2>
                <pre>{json.dumps(results, indent=2, default=str)}</pre>
            </div>
        </body>
        </html>
        """
        return html


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Comprehensive Remote Trading Agent Test Runner")
    parser.add_argument("--url", default=config.BASE_URL, help="Base URL of the API")
    parser.add_argument("--output-dir", default=config.REPORT_OUTPUT_DIR, help="Output directory for reports")
    parser.add_argument("--categories", nargs="+", choices=config.TEST_CATEGORIES + ["mock_agents", "configuration", "environment"],
                       help="Test categories to run")
    parser.add_argument("--no-reports", action="store_true", help="Skip generating reports")
    
    args = parser.parse_args()
    
    # Create test runner
    runner = ComprehensiveTestRunner(args.url, args.output_dir)
    
    # Run tests
    results = runner.run_all_tests(args.categories)
    
    # Generate reports
    if not args.no_reports:
        print("\n📊 Generating reports...")
        report_files = runner.generate_reports(results)
        print("✅ Reports generated successfully!")
    
    # Print summary
    main_summary = results.get("main_tests", {}).get("summary", {})
    print(f"\n🎯 FINAL RESULT: {main_summary.get('overall_status', 'UNKNOWN')}")
    print(f"   Tests: {main_summary.get('passed_tests', 0)}/{main_summary.get('total_tests', 0)} passed")
    print(f"   Success Rate: {main_summary.get('success_rate', 0):.2%}")
    
    # Exit with appropriate code
    exit_code = 0 if main_summary.get('overall_status') == 'PASS' else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
