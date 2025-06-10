# Remote Trading Agent API Documentation

## Overview
This API provides remote access to the stock trading agent functionality, allowing other projects to integrate trading capabilities safely.

## Features
- ✅ News retrieval for companies
- ✅ Sentiment analysis of news articles
- ✅ Price prediction (when dependencies are available)
- ❌ Trading execution (disabled for safety)
- ✅ Full analysis pipeline
- ✅ Health monitoring

## Base URL
- Development: `http://localhost:5000`
- Production: Configure as needed

## Quick Start

### 1. Start the API Server
```bash
# Development mode
./start_remote_agent.sh

# Production mode
./start_remote_agent_production.sh
```

### 2. Test the API
```bash
# Test modules
python test_remote_agent.py

# Run usage examples
python usage_examples.py
```

### 3. Use in Your Project
```python
from remote_agent_client import RemoteTradingAgentClient

client = RemoteTradingAgentClient("http://localhost:5000")

# Get news and analyze sentiment
news = client.get_news("Tesla")
if news['success']:
    sentiment = client.analyze_sentiment(news['news'])
    print(f"Trading decision: {sentiment['decision']}")

# Full analysis
result = client.full_analysis("Tesla", "TSLA")
print(result)
```

## API Endpoints

### Health Check
- **GET** `/health`
- Returns API status and service availability

### Get News
- **POST** `/api/news`
- Body: `{"company": "Tesla", "api_key": "optional"}`
- Returns news articles for the specified company

### Analyze Sentiment
- **POST** `/api/sentiment`
- Body: `{"news_articles": ["article1", "article2"]}`
- Returns sentiment analysis and trading decision

### Predict Price
- **POST** `/api/predict`
- Body: `{"symbol": "AAPL", "days": 60}`
- Returns predicted stock price (if service available)

### Full Analysis
- **POST** `/api/full-analysis`
- Body: Complete analysis parameters
- Returns comprehensive trading analysis

### List Endpoints
- **GET** `/api/endpoints`
- Returns all available endpoints with descriptions

## Integration Examples

### JavaScript/Node.js
```javascript
const axios = require('axios');

async function getTradingDecision(company, symbol) {
    const client = axios.create({ baseURL: 'http://localhost:5000' });
    
    try {
        const result = await client.post('/api/full-analysis', {
            company: company,
            symbol: symbol
        });
        
        return result.data.sentiment_analysis.decision;
    } catch (error) {
        console.error('Error:', error.message);
        return null;
    }
}

// Usage
getTradingDecision('Tesla', 'TSLA').then(decision => {
    console.log('Trading decision:', decision);
});
```

### Python
```python
import requests

def get_trading_signal(company):
    response = requests.post('http://localhost:5000/api/full-analysis', 
                           json={'company': company})
    
    if response.status_code == 200:
        data = response.json()
        return data['sentiment_analysis']['decision']
    return None

# Usage
signal = get_trading_signal('Apple')
print(f'Trading signal: {signal}')
```

### cURL
```bash
# Health check
curl http://localhost:5000/health

# Get trading analysis
curl -X POST http://localhost:5000/api/full-analysis \
  -H "Content-Type: application/json" \
  -d '{"company": "Tesla", "symbol": "TSLA"}'
```

## Safety Features
- Trading execution is disabled by default
- All operations are read-only except for analysis
- Comprehensive error handling
- Service availability monitoring

## Deployment
- Development: Direct Python execution
- Production: Gunicorn WSGI server
- Containerized: Docker support available
- Scalable: Multiple worker processes

## Error Handling
All endpoints return JSON responses with success/error status:
```json
{
    "success": true,
    "data": "..."
}
```
or
```json
{
    "success": false,
    "error": "Error message"
}
```
