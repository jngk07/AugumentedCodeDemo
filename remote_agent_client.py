import requests
import json

class RemoteTradingAgentClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def health_check(self):
        """Check if the remote agent is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_news(self, company, api_key=None):
        """Get news for a company"""
        try:
            data = {"company": company}
            if api_key:
                data["api_key"] = api_key
            
            response = requests.post(f"{self.base_url}/api/news", json=data, timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_sentiment(self, news_articles):
        """Analyze sentiment of news articles"""
        try:
            data = {"news_articles": news_articles}
            response = requests.post(f"{self.base_url}/api/sentiment", json=data, timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def predict_price(self, symbol, days=60):
        """Predict stock price"""
        try:
            data = {"symbol": symbol, "days": days}
            response = requests.post(f"{self.base_url}/api/predict", json=data, timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def execute_trade(self, symbol, action, qty, api_key, secret_key):
        """Execute a trade (disabled for safety)"""
        try:
            data = {
                "symbol": symbol,
                "action": action,
                "qty": qty,
                "api_key": api_key,
                "secret_key": secret_key
            }
            response = requests.post(f"{self.base_url}/api/trade", json=data, timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def full_analysis(self, company="Tesla", symbol="TSLA", news_api_key=None, 
                     enable_prediction=False):
        """Run complete trading analysis"""
        try:
            data = {
                "company": company,
                "symbol": symbol,
                "news_api_key": news_api_key,
                "enable_prediction": enable_prediction
            }
            response = requests.post(f"{self.base_url}/api/full-analysis", json=data, timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def list_endpoints(self):
        """Get list of all available endpoints"""
        try:
            response = requests.get(f"{self.base_url}/api/endpoints", timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    client = RemoteTradingAgentClient()
    
    # Test health check
    print("Health Check:", client.health_check())
    
    # Test news retrieval
    print("\nNews:", client.get_news("Tesla"))
    
    # Test sentiment analysis
    sample_news = [
        "Tesla stock surges after positive earnings",
        "Analysts upgrade Tesla to buy rating"
    ]
    print("\nSentiment:", client.analyze_sentiment(sample_news))
    
    # Test full analysis
    print("\nFull Analysis:", client.full_analysis("Tesla", "TSLA"))
    
    # List all endpoints
    print("\nAvailable Endpoints:", client.list_endpoints())
