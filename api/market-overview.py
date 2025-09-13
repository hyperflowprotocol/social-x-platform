from http.server import BaseHTTPRequestHandler
import json
import random
import time

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Dynamic market overview - aggregate all 3 accounts
        base_time = time.time()
        
        # Calculate dynamic market caps for all 3 accounts (matching trending-accounts.py)
        # @diero_hl: ~$0.12 * 100,000 = ~$12,000
        diero_price = round(0.12 + random.uniform(-0.006, 0.006), 4)
        diero_market_cap = round(diero_price * 100000)
        
        # @jeromeliquid: ~$0.15 * 80,000 = ~$12,000  
        jerome_price = round(0.15 + random.uniform(-0.008, 0.012), 4)
        jerome_market_cap = round(jerome_price * 80000)
        
        # @jeffrey_hl: ~$0.18 * 60,000 = ~$10,800
        jeffrey_price = round(0.18 + random.uniform(-0.009, 0.015), 4)
        jeffrey_market_cap = round(jeffrey_price * 60000)
        
        # Total market cap from all 3 accounts
        total_market_cap = diero_market_cap + jerome_market_cap + jeffrey_market_cap
        
        # Combined volume from all accounts
        diero_volume = random.randint(1500, 4000)
        jerome_volume = random.randint(2000, 6000)  
        jeffrey_volume = random.randint(3000, 8000)
        total_volume_24h = diero_volume + jerome_volume + jeffrey_volume
        
        # Active traders - keep it small and realistic
        active_traders = 20
        
        # Overall market trending change
        trending_change_val = round(random.uniform(-5.0, 35.0), 1)
        trending_change = f"{'+' if trending_change_val >= 0 else ''}{trending_change_val}%"
        
        response = {
            "total_market_cap": total_market_cap,
            "total_volume_24h": total_volume_24h,
            "active_accounts": 3,  # We have 3 trending accounts
            "active_traders": active_traders,
            "total_tokens_launched": 3,  # All 3 tokens launched
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