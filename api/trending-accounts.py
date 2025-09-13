from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # @diero_hl profile data
        accounts = [{
            "name": "diero_hl", 
            "handle": "diero_hl", 
            "avatar": "/avatar-diero.png",
            "price_per_token": 0.12, 
            "market_cap": 12000, 
            "daily_change": 25.8,
            "holders": 145,
            "volume_24h": 2500
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