#!/bin/bash

# Simple test runner script for the Remote Trading Agent Test Case Agent
# This script provides easy commands to run different types of tests

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
BASE_URL="http://localhost:5000"
OUTPUT_DIR="test_reports"
VERBOSE=false

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if server is running
check_server() {
    print_status "Checking if server is running at $BASE_URL..."
    if curl -s "$BASE_URL/health" > /dev/null 2>&1; then
        print_success "Server is running"
        return 0
    else
        print_warning "Server is not running at $BASE_URL"
        return 1
    fi
}

# Function to start server if needed
start_server() {
    if ! check_server; then
        print_status "Starting test server..."
        python remote_agent_api.py &
        SERVER_PID=$!
        echo $SERVER_PID > .test_server.pid
        
        # Wait for server to start
        for i in {1..30}; do
            if check_server; then
                print_success "Server started successfully"
                return 0
            fi
            sleep 1
        done
        
        print_error "Failed to start server"
        return 1
    fi
}

# Function to stop server
stop_server() {
    if [ -f .test_server.pid ]; then
        PID=$(cat .test_server.pid)
        if kill -0 $PID 2>/dev/null; then
            print_status "Stopping test server (PID: $PID)..."
            kill $PID
            rm .test_server.pid
            print_success "Server stopped"
        fi
    fi
}

# Function to run basic tests
run_basic_tests() {
    print_status "Running basic tests..."
    
    if [ "$VERBOSE" = true ]; then
        python test_case_agent.py --url "$BASE_URL" --verbose
    else
        python test_case_agent.py --url "$BASE_URL"
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Basic tests completed successfully"
    else
        print_error "Basic tests failed"
        return 1
    fi
}

# Function to run comprehensive tests
run_comprehensive_tests() {
    print_status "Running comprehensive tests..."
    
    ARGS="--url $BASE_URL --output-dir $OUTPUT_DIR"
    
    if [ "$#" -gt 0 ]; then
        ARGS="$ARGS --categories $*"
    fi
    
    python run_comprehensive_tests.py $ARGS
    
    if [ $? -eq 0 ]; then
        print_success "Comprehensive tests completed successfully"
    else
        print_error "Comprehensive tests failed"
        return 1
    fi
}

# Function to run mock agent tests
run_mock_tests() {
    print_status "Running mock agent tests..."
    
    python test_mock_agents.py
    
    if [ $? -eq 0 ]; then
        print_success "Mock agent tests completed successfully"
    else
        print_error "Mock agent tests failed"
        return 1
    fi
}

# Function to run examples
run_examples() {
    print_status "Running test examples..."
    
    if [ "$#" -gt 0 ]; then
        python test_examples.py --example "$1"
    else
        python test_examples.py
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Examples completed successfully"
    else
        print_error "Examples failed"
        return 1
    fi
}

# Function to show usage
show_usage() {
    echo "Remote Trading Agent Test Runner"
    echo "================================"
    echo ""
    echo "Usage: $0 [OPTIONS] COMMAND [ARGS]"
    echo ""
    echo "Commands:"
    echo "  basic                    Run basic tests"
    echo "  comprehensive [cats...]  Run comprehensive tests (optionally specify categories)"
    echo "  mock                     Run mock agent tests"
    echo "  examples [example]       Run examples (optionally specify which one)"
    echo "  start-server            Start test server"
    echo "  stop-server             Stop test server"
    echo "  check-server            Check if server is running"
    echo "  all                     Run all tests"
    echo "  help                    Show this help"
    echo ""
    echo "Options:"
    echo "  --url URL               Base URL for testing (default: $BASE_URL)"
    echo "  --output-dir DIR        Output directory for reports (default: $OUTPUT_DIR)"
    echo "  --verbose               Enable verbose output"
    echo "  --auto-server           Automatically start/stop server"
    echo ""
    echo "Examples:"
    echo "  $0 basic"
    echo "  $0 comprehensive api client"
    echo "  $0 --url http://localhost:8080 basic"
    echo "  $0 --auto-server all"
    echo "  $0 examples performance"
    echo ""
    echo "Environment Variables:"
    echo "  TEST_BASE_URL           Override default base URL"
    echo "  ENABLE_PERFORMANCE_TESTS Set to 'false' to skip performance tests"
    echo "  ENABLE_LOAD_TESTS       Set to 'false' to skip load tests"
}

# Parse command line arguments
AUTO_SERVER=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            BASE_URL="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --auto-server)
            AUTO_SERVER=true
            shift
            ;;
        --help|-h)
            show_usage
            exit 0
            ;;
        *)
            break
            ;;
    esac
done

# Override with environment variable if set
if [ -n "$TEST_BASE_URL" ]; then
    BASE_URL="$TEST_BASE_URL"
fi

# Main command handling
COMMAND="$1"
shift || true

case "$COMMAND" in
    basic)
        if [ "$AUTO_SERVER" = true ]; then
            start_server
            trap stop_server EXIT
        fi
        run_basic_tests
        ;;
    comprehensive)
        if [ "$AUTO_SERVER" = true ]; then
            start_server
            trap stop_server EXIT
        fi
        run_comprehensive_tests "$@"
        ;;
    mock)
        run_mock_tests
        ;;
    examples)
        if [ "$AUTO_SERVER" = true ]; then
            start_server
            trap stop_server EXIT
        fi
        run_examples "$@"
        ;;
    start-server)
        start_server
        ;;
    stop-server)
        stop_server
        ;;
    check-server)
        check_server
        ;;
    all)
        if [ "$AUTO_SERVER" = true ]; then
            start_server
            trap stop_server EXIT
        fi
        
        print_status "Running all tests..."
        run_mock_tests && \
        run_basic_tests && \
        run_comprehensive_tests && \
        run_examples
        
        if [ $? -eq 0 ]; then
            print_success "All tests completed successfully!"
        else
            print_error "Some tests failed"
            exit 1
        fi
        ;;
    help|"")
        show_usage
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        show_usage
        exit 1
        ;;
esac
