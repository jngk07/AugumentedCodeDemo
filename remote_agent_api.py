from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the agent modules with error handling
try:
    from agent1_news_reader import get_news
    NEWS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: News functionality not available: {e}")
    NEWS_AVAILABLE = False
    def get_news(*args, **kwargs):
        return ["Sample news: Market shows positive trends", "Sample news: Economic indicators improving"]

try:
    from agent2_sentiment_signal import analyze_news
    SENTIMENT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Sentiment analysis not available: {e}")
    SENTIMENT_AVAILABLE = False
    def analyze_news(news_articles):
        return "HOLD", 0.0

try:
    from agent4_price_predictor import predict_price
    PREDICTION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Price prediction not available: {e}")
    PREDICTION_AVAILABLE = False
    def predict_price(*args, **kwargs):
        return None

# Trading functionality (optional)
TRADER_AVAILABLE = False
def execute_trade(*args, **kwargs):
    raise Exception("Trading functionality disabled for safety")

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "message": "Remote Trading Agent API is running",
        "services": {
            "news": NEWS_AVAILABLE,
            "sentiment": SENTIMENT_AVAILABLE,
            "prediction": PREDICTION_AVAILABLE,
            "trader": TRADER_AVAILABLE
        }
    })

@app.route('/api/news', methods=['POST'])
def get_news_api():
    """Get news for a company"""
    try:
        data = request.get_json()
        company = data.get('company', 'Tesla')
        api_key = data.get('api_key')
        
        news = get_news(company, api_key)
        return jsonify({
            "success": True,
            "company": company,
            "news": news,
            "service_available": NEWS_AVAILABLE
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment_api():
    """Analyze sentiment of news articles"""
    try:
        data = request.get_json()
        news_articles = data.get('news_articles', [])
        
        if not news_articles:
            return jsonify({
                "success": False,
                "error": "No news articles provided"
            }), 400
        
        decision, score = analyze_news(news_articles)
        return jsonify({
            "success": True,
            "decision": decision,
            "sentiment_score": score,
            "articles_analyzed": len(news_articles),
            "service_available": SENTIMENT_AVAILABLE
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict_price_api():
    """Predict stock price"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'AAPL')
        days = data.get('days', 60)
        
        if not PREDICTION_AVAILABLE:
            return jsonify({
                "success": False,
                "error": "Price prediction service not available",
                "service_available": False
            }), 503
        
        predicted_price = predict_price(symbol, days)
        
        if predicted_price is None:
            return jsonify({
                "success": False,
                "error": f"Could not predict price for symbol {symbol}"
            }), 400
        
        return jsonify({
            "success": True,
            "symbol": symbol,
            "predicted_price": predicted_price,
            "prediction_days": days,
            "service_available": PREDICTION_AVAILABLE
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/trade', methods=['POST'])
def execute_trade_api():
    """Execute a trade"""
    try:
        return jsonify({
            "success": False,
            "error": "Trading functionality disabled for safety",
            "service_available": TRADER_AVAILABLE
        }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/full-analysis', methods=['POST'])
def full_analysis_api():
    """Complete trading analysis pipeline"""
    try:
        data = request.get_json()
        company = data.get('company', 'Tesla')
        symbol = data.get('symbol', 'TSLA')
        news_api_key = data.get('news_api_key')
        enable_prediction = data.get('enable_prediction', False)
        
        # Step 1: Get news
        news = get_news(company, news_api_key)
        
        # Step 2: Analyze sentiment
        decision, sentiment_score = analyze_news(news)
        
        result = {
            "success": True,
            "company": company,
            "symbol": symbol,
            "news": news,
            "sentiment_analysis": {
                "decision": decision,
                "score": sentiment_score
            },
            "services": {
                "news": NEWS_AVAILABLE,
                "sentiment": SENTIMENT_AVAILABLE,
                "prediction": PREDICTION_AVAILABLE,
                "trader": TRADER_AVAILABLE
            }
        }
        
        # Step 3: Price prediction (optional)
        if enable_prediction and PREDICTION_AVAILABLE:
            try:
                predicted_price = predict_price(symbol)
                result["price_prediction"] = {
                    "predicted_price": predicted_price,
                    "prediction_available": predicted_price is not None
                }
            except Exception as pred_error:
                result["price_prediction"] = {
                    "predicted_price": None,
                    "prediction_available": False,
                    "error": str(pred_error)
                }
        else:
            result["price_prediction"] = {
                "predicted_price": None,
                "prediction_available": False,
                "reason": "Prediction disabled or service unavailable"
            }
        
        # Trading is disabled for safety
        result["trade_execution"] = {
            "executed": False,
            "reason": "Trading functionality disabled for safety"
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/endpoints', methods=['GET'])
def list_endpoints():
    """List all available API endpoints"""
    endpoints = {
        "health": {
            "method": "GET",
            "url": "/health",
            "description": "Health check endpoint"
        },
        "news": {
            "method": "POST",
            "url": "/api/news",
            "description": "Get news for a company",
            "parameters": ["company", "api_key (optional)"],
            "available": NEWS_AVAILABLE
        },
        "sentiment": {
            "method": "POST",
            "url": "/api/sentiment",
            "description": "Analyze sentiment of news articles",
            "parameters": ["news_articles"],
            "available": SENTIMENT_AVAILABLE
        },
        "predict": {
            "method": "POST",
            "url": "/api/predict",
            "description": "Predict stock price",
            "parameters": ["symbol", "days (optional)"],
            "available": PREDICTION_AVAILABLE
        },
        "trade": {
            "method": "POST",
            "url": "/api/trade",
            "description": "Execute a trade (disabled for safety)",
            "parameters": ["symbol", "action", "qty", "api_key", "secret_key"],
            "available": False
        },
        "full_analysis": {
            "method": "POST",
            "url": "/api/full-analysis",
            "description": "Complete trading analysis pipeline",
            "parameters": ["company", "symbol", "news_api_key", "enable_prediction"]
        }
    }
    return jsonify(endpoints)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
