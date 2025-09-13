from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timedelta
import random

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        trades = []
        base_time = datetime.now()
        trade_types = ["buy", "sell"]
        
        # Generate trades for @diero_hl
        for i in range(3):
            time = base_time - timedelta(minutes=random.randint(1, 120))
            shares = random.randint(50, 300)
            base_price = 0.12  # Base diero_hl price
            price = round(base_price + random.uniform(-0.006, 0.006), 4)  # Dynamic ±5%
            trades.append({
                "id": f"diero_trade_{i+1}",
                "timestamp": time.isoformat(),
                "type": random.choice(trade_types),
                "shares": shares,
                "account": "diero_hl",
                "price": price,
                "total_value": round(shares * price, 2)
            })
        
        # Generate trades for @jeromeliquid
        for i in range(3):
            time = base_time - timedelta(minutes=random.randint(1, 180))
            shares = random.randint(75, 400)  # Higher volumes for Jerome
            base_price = 0.15  # Base jerome price
            price = round(base_price + random.uniform(-0.008, 0.012), 4)  # Dynamic ±6%
            trades.append({
                "id": f"jerome_trade_{i+1}",
                "timestamp": time.isoformat(),
                "type": random.choice(trade_types),
                "shares": shares,
                "account": "jeromeliquid",
                "price": price,
                "total_value": round(shares * price, 2)
            })
        
        # Generate trades for @jeffrey_hl
        for i in range(2):
            time = base_time - timedelta(minutes=random.randint(1, 200))
            shares = random.randint(100, 600)  # Premium volumes for Jeffrey
            base_price = 0.18  # Base jeffrey price (highest)
            price = round(base_price + random.uniform(-0.009, 0.015), 4)  # Dynamic ±7%
            trades.append({
                "id": f"jeffrey_trade_{i+1}",
                "timestamp": time.isoformat(),
                "type": random.choice(trade_types),
                "shares": shares,
                "account": "jeffrey_hl",
                "price": price,
                "total_value": round(shares * price, 2)
            })
        
        sorted_trades = sorted(trades, key=lambda x: x['timestamp'], reverse=True)
        response = {"trades": sorted_trades}
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return