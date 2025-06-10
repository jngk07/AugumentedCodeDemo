#!/usr/bin/env python3
"""
Usage examples for the Remote Trading Agent
"""
from remote_agent_client import RemoteTradingAgentClient
import json

def main():
    # Initialize client
    client = RemoteTradingAgentClient("http://localhost:5000")
    
    print("=== Remote Trading Agent Usage Examples ===\n")
    
    # 1. Health Check
    print("1. Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    print()
    
    # 2. Get News
    print("2. Get News for Tesla:")
    news_result = client.get_news("Tesla")
    print(json.dumps(news_result, indent=2))
    print()
    
    # 3. Analyze Sentiment
    print("3. Analyze Sentiment:")
    sample_news = [
        "Tesla reports record quarterly earnings, stock soars",
        "Electric vehicle market shows strong growth potential",
        "Tesla announces new factory expansion plans"
    ]
    sentiment_result = client.analyze_sentiment(sample_news)
    print(json.dumps(sentiment_result, indent=2))
    print()
    
    # 4. Full Analysis
    print("4. Full Analysis:")
    full_result = client.full_analysis("Tesla", "TSLA", enable_prediction=False)
    print(json.dumps(full_result, indent=2))
    print()
    
    # 5. List Endpoints
    print("5. Available Endpoints:")
    endpoints = client.list_endpoints()
    print(json.dumps(endpoints, indent=2))

if __name__ == "__main__":
    main()
