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
        
        # Jerome.hl data - separate dynamic values
        jerome_price_variance = random.uniform(-0.008, 0.012)  # ±6% of 0.15
        jerome_current_price = round(0.15 + jerome_price_variance, 4)
        jerome_total_supply = 80000
        jerome_market_cap = round(jerome_current_price * jerome_total_supply)
        jerome_daily_change = round(random.uniform(-15.0, 60.0), 1)
        jerome_volume_24h = random.randint(2000, 6000)
        jerome_holders = random.randint(200, 300)
        
        # Jeffrey.hl data - premium tier dynamics
        jeffrey_price_variance = random.uniform(-0.009, 0.015)  # ±7% of 0.18
        jeffrey_current_price = round(0.18 + jeffrey_price_variance, 4)
        jeffrey_total_supply = 60000  # Lower supply, higher value
        jeffrey_market_cap = round(jeffrey_current_price * jeffrey_total_supply)
        jeffrey_daily_change = round(random.uniform(-8.0, 75.0), 1)  # Higher potential gains
        jeffrey_volume_24h = random.randint(3000, 8000)  # Highest volume
        jeffrey_holders = random.randint(350, 500)  # Most holders (1.6K followers)
        
        accounts = [{
            "name": "diero_hl", 
            "handle": "diero_hl", 
            "avatar": "https://amethyst-defensive-marsupial-68.mypinata.cloud/ipfs/bafkreiglj7znabpnwgf6uo4vol3twduhhlcj6fl4r7s3jvdsjt7akfyhiu",
            "price_per_token": current_price, 
            "market_cap": current_market_cap, 
            "daily_change": daily_change,
            "holders": holders,
            "volume_24h": volume_24h
        }, {
            "name": "Jerome.hl",
            "handle": "jeromeliquid", 
            "avatar": "https://amethyst-defensive-marsupial-68.mypinata.cloud/ipfs/bafkreieyky45yo4dwuvjg5ffu4lpncrgjlpr5m7ogp65jhir3vv7uw423y",
            "price_per_token": jerome_current_price,
            "market_cap": jerome_market_cap,
            "daily_change": jerome_daily_change,
            "holders": jerome_holders,
            "volume_24h": jerome_volume_24h
        }, {
            "name": "Jeffrey.hl",
            "handle": "jeffrey_hl",
            "avatar": "https://amethyst-defensive-marsupial-68.mypinata.cloud/ipfs/bafkreidt75eg2r6oao2uamqgrhrksvv6o6osqt2cr2uz2tzou3xp3cky6m",
            "price_per_token": jeffrey_current_price,
            "market_cap": jeffrey_market_cap,
            "daily_change": jeffrey_daily_change,
            "holders": jeffrey_holders,
            "volume_24h": jeffrey_volume_24h
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