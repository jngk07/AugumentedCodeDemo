#!/usr/bin/env python3
"""
Mock agents for testing the remote trading agent system.
These provide predictable responses for testing purposes.
"""

import random
import time
from typing import List, Tuple, Optional, Any

class MockNewsAgent:
    """Mock news agent that provides sample news data"""
    
    def __init__(self):
        self.sample_news = [
            "Company reports strong quarterly earnings with 15% growth",
            "New product launch receives positive market reception",
            "CEO announces strategic partnership with major tech firm",
            "Analysts upgrade stock rating to 'Buy' with higher price target",
            "Company expands operations to new international markets",
            "Innovative technology patent approved, boosting competitive advantage",
            "Strong demand drives revenue growth in key business segments",
            "Company announces dividend increase and share buyback program",
            "Market volatility affects stock price despite strong fundamentals",
            "Regulatory approval received for new product line"
        ]
    
    def get_news(self, company: str, api_key: Optional[str] = None) -> List[str]:
        """Get mock news for a company"""
        # Simulate API delay
        time.sleep(random.uniform(0.1, 0.5))
        
        # Return random selection of news
        num_articles = random.randint(3, 7)
        selected_news = random.sample(self.sample_news, min(num_articles, len(self.sample_news)))
        
        # Customize news for the company
        customized_news = []
        for news in selected_news:
            customized_news.append(f"{company}: {news}")
        
        return customized_news

class MockSentimentAgent:
    """Mock sentiment analysis agent"""
    
    def __init__(self):
        self.positive_keywords = [
            "strong", "growth", "positive", "upgrade", "buy", "increase", 
            "expansion", "innovative", "approved", "boost", "higher"
        ]
        self.negative_keywords = [
            "weak", "decline", "negative", "downgrade", "sell", "decrease",
            "contraction", "concerns", "rejected", "drop", "lower"
        ]
    
    def analyze_news(self, news_articles: List[str]) -> Tuple[str, float]:
        """Analyze sentiment of news articles"""
        # Simulate processing delay
        time.sleep(random.uniform(0.2, 0.8))
        
        if not news_articles:
            return "HOLD", 0.0
        
        total_score = 0.0
        
        for article in news_articles:
            article_lower = article.lower()
            
            # Count positive and negative keywords
            positive_count = sum(1 for keyword in self.positive_keywords if keyword in article_lower)
            negative_count = sum(1 for keyword in self.negative_keywords if keyword in article_lower)
            
            # Calculate article score
            article_score = (positive_count - negative_count) / max(len(article.split()), 1)
            total_score += article_score
        
        # Average score across all articles
        avg_score = total_score / len(news_articles)
        
        # Determine decision based on score
        if avg_score > 0.1:
            decision = "BUY"
        elif avg_score < -0.1:
            decision = "SELL"
        else:
            decision = "HOLD"
        
        # Normalize score to [-1, 1] range
        normalized_score = max(-1.0, min(1.0, avg_score * 10))
        
        return decision, normalized_score

class MockPricePredictorAgent:
    """Mock price prediction agent"""
    
    def __init__(self):
        self.base_prices = {
            "AAPL": 150.0,
            "TSLA": 200.0,
            "GOOGL": 120.0,
            "MSFT": 300.0,
            "AMZN": 100.0,
            "META": 250.0,
            "NVDA": 400.0
        }
    
    def predict_price(self, symbol: str, days: int = 60) -> Optional[float]:
        """Predict stock price"""
        # Simulate model processing delay
        time.sleep(random.uniform(1.0, 3.0))
        
        # Get base price or use default
        base_price = self.base_prices.get(symbol.upper(), 100.0)
        
        # Simulate prediction with some randomness
        # Longer prediction periods have more uncertainty
        uncertainty_factor = 1 + (days / 365) * 0.5  # More uncertainty for longer periods
        
        # Random walk with slight upward bias
        price_change = random.gauss(0.05, 0.2 * uncertainty_factor)  # 5% average growth with volatility
        predicted_price = base_price * (1 + price_change)
        
        # Ensure price is positive
        predicted_price = max(predicted_price, 1.0)
        
        return round(predicted_price, 2)

class MockTradingAgent:
    """Mock trading agent (always disabled for safety)"""
    
    def execute_trade(self, symbol: str, action: str, qty: int, 
                     api_key: str, secret_key: str) -> dict:
        """Execute a trade (always raises exception for safety)"""
        raise Exception("Trading functionality disabled for safety")

# Factory function to create mock agents
def create_mock_agents():
    """Create all mock agents"""
    return {
        "news": MockNewsAgent(),
        "sentiment": MockSentimentAgent(),
        "predictor": MockPricePredictorAgent(),
        "trader": MockTradingAgent()
    }

# Test the mock agents
if __name__ == "__main__":
    print("Testing Mock Agents...")
    
    agents = create_mock_agents()
    
    # Test news agent
    print("\n1. Testing News Agent:")
    news = agents["news"].get_news("Tesla")
    print(f"Retrieved {len(news)} news articles:")
    for i, article in enumerate(news[:3], 1):
        print(f"  {i}. {article}")
    
    # Test sentiment agent
    print("\n2. Testing Sentiment Agent:")
    decision, score = agents["sentiment"].analyze_news(news)
    print(f"Sentiment Analysis: {decision} (Score: {score:.3f})")
    
    # Test price predictor
    print("\n3. Testing Price Predictor:")
    predicted_price = agents["predictor"].predict_price("TSLA", 30)
    print(f"Predicted TSLA price in 30 days: ${predicted_price}")
    
    # Test trading agent
    print("\n4. Testing Trading Agent:")
    try:
        agents["trader"].execute_trade("TSLA", "buy", 10, "test", "test")
    except Exception as e:
        print(f"Trading correctly disabled: {e}")
    
    print("\nAll mock agents tested successfully!")
