from http.server import BaseHTTPRequestHandler
import json
import random
import time

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Generate dynamic, live-changing data for @diero_hl
        base_time = time.time()
        
        # Price fluctuates around $0.12 (±5%)
        price_variance = random.uniform(-0.006, 0.006)  # ±5% of 0.12
        current_price = round(0.12 + price_variance, 4)
        
        # Market cap changes with price (100,000 total supply assumed)
        total_supply = 100000
        current_market_cap = round(current_price * total_supply)
        
        # Daily change varies between -10% to +50%  
        daily_change = round(random.uniform(-10.0, 50.0), 1)
        
        # Volume and holders fluctuate
        volume_24h = random.randint(1500, 4000)
        holders = random.randint(120, 180)
        
        accounts = [{
            "name": "diero_hl", 
            "handle": "diero_hl", 
            "avatar": "https://amethyst-defensive-marsupial-68.mypinata.cloud/ipfs/bafkreiglj7znabpnwgf6uo4vol3twduhhlcj6fl4r7s3jvdsjt7akfyhiu",
            "price_per_token": current_price, 
            "market_cap": current_market_cap, 
            "daily_change": daily_change,
            "holders": holders,
            "volume_24h": volume_24h
        }]
        
        response = {"accounts": accounts}
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return