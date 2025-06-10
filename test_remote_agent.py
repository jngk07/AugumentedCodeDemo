#!/usr/bin/env python3
"""
Test suite for the Remote Trading Agent API
"""
import unittest
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test individual modules first
def test_modules():
    """Test if modules can be imported"""
    print("Testing module imports...")
    
    try:
        from agent1_news_reader import get_news
        print("✓ News reader module imported successfully")
        news = get_news("Tesla")
        print(f"✓ News function works: {len(news)} articles")
    except Exception as e:
        print(f"✗ News reader module error: {e}")
    
    try:
        from agent2_sentiment_signal import analyze_news
        print("✓ Sentiment analysis module imported successfully")
        decision, score = analyze_news(["Tesla stock rises"])
        print(f"✓ Sentiment function works: {decision}, {score}")
    except Exception as e:
        print(f"✗ Sentiment analysis module error: {e}")
    
    try:
        from agent4_price_predictor import predict_price
        print("✓ Price predictor module imported successfully")
    except Exception as e:
        print(f"✗ Price predictor module error: {e}")
    
    try:
        import remote_agent_api
        print("✓ Remote agent API module imported successfully")
    except Exception as e:
        print(f"✗ Remote agent API module error: {e}")
    
    try:
        from remote_agent_client import RemoteTradingAgentClient
        client = RemoteTradingAgentClient()
        print("✓ Remote agent client imported and instantiated successfully")
    except Exception as e:
        print(f"✗ Remote agent client error: {e}")

if __name__ == '__main__':
    test_modules()
