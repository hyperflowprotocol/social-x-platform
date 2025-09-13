from http.server import BaseHTTPRequestHandler
import json
import random
import time

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Dynamic market overview that changes over time
        base_time = time.time()
        
        # Market cap fluctuates around 12K
        market_cap_variance = random.uniform(-1000, 3000)
        total_market_cap = max(8000, round(12000 + market_cap_variance))
        
        # Volume changes
        total_volume_24h = random.randint(1500, 4500)
        
        # Trader count varies
        active_traders = random.randint(120, 200)
        
        # Trending change percentage
        trending_change_val = round(random.uniform(-8.0, 45.0), 1)
        trending_change = f"{'+' if trending_change_val >= 0 else ''}{trending_change_val}%"
        
        response = {
            "total_market_cap": total_market_cap,
            "total_volume_24h": total_volume_24h,
            "active_accounts": 1,
            "active_traders": active_traders,
            "total_tokens_launched": 1,
            "trending_change": trending_change
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return