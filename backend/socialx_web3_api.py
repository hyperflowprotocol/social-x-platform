from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Mock data generators
def generate_trending_accounts():
    # Only show @diero_hl profile as requested
    accounts = [
        {
            "name": "diero_hl", 
            "handle": "diero_hl", 
            "avatar": "/avatar-diero.png",
            "price_per_token": 0.12, 
            "market_cap": 12000, 
            "daily_change": 25.8,
            "holders": 145,
            "volume_24h": 2500
        }
    ]
    return accounts

def generate_recent_trades():
    trades = []
    base_time = datetime.now()
    trade_types = ["buy", "sell"]
    
    # Only trades for @diero_hl
    for i in range(6):
        time = base_time - timedelta(minutes=random.randint(1, 120))
        shares = random.randint(50, 300)
        price = 0.12  # Match diero_hl price
        trades.append({
            "id": f"trade_{i+1}",
            "timestamp": time.isoformat(),
            "type": random.choice(trade_types),
            "shares": shares,
            "account": "diero_hl",
            "price": round(price + random.uniform(-0.01, 0.01), 4),
            "total_value": round(shares * price, 2)
        })
    return sorted(trades, key=lambda x: x['timestamp'], reverse=True)

@app.route('/api/trending-accounts', methods=['GET'])
def get_trending_accounts():
    accounts = generate_trending_accounts()
    return jsonify({"accounts": accounts})

@app.route('/api/recent-trades', methods=['GET'])
def get_recent_trades():
    trades = generate_recent_trades()
    return jsonify({"trades": trades})

@app.route('/api/market-overview', methods=['GET'])
def get_market_overview():
    return jsonify({
        "total_market_cap": 12000,
        "total_volume_24h": 2500,
        "active_accounts": 1,
        "active_traders": 145,
        "total_tokens_launched": 1,
        "trending_change": "+25.8%"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)