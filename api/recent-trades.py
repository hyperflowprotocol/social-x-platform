import json
from datetime import datetime, timedelta
import random

def handler(request):
    """Vercel serverless function for recent trades API"""
    
    trades = []
    base_time = datetime.now()
    trade_types = ["buy", "sell"]
    
    # Generate trades for @diero_hl
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
    
    sorted_trades = sorted(trades, key=lambda x: x['timestamp'], reverse=True)
    response = {"trades": sorted_trades}
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps(response)
    }