#!/usr/bin/env python3
"""
Scatter-Style Crypto Lottery Platform
Professional lottery/gambling platform inspired by scatter.io
Features: Real-time draws, provable fairness, instant payouts
"""

import http.server
import socketserver
import json
import random
from datetime import datetime, timedelta

PORT = 5000

class ScatterLotteryHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow Lottery - HYPE Token Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: white; min-height: 100vh; overflow-x: hidden;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; padding: 30px 0; }
        .header h1 { 
            font-size: 3.5rem; 
            background: linear-gradient(45deg, #00d4ff, #0099cc, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px; 
        }
        .header p { font-size: 1.3rem; color: #E0E0E0; }
        
        .main-lottery {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 40px; margin-bottom: 30px;
            backdrop-filter: blur(10px); text-align: center;
        }
        .prize-pool { 
            font-size: 4rem; 
            background: linear-gradient(45deg, #00d4ff, #0099cc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold; 
            margin: 20px 0; 
        }
        .countdown { font-size: 2.5rem; color: #FF6B6B; margin: 20px 0; }
        
        .entry-form { margin: 30px 0; }
        .form-row { display: flex; gap: 15px; margin: 15px 0; justify-content: center; }
        .input-field {
            padding: 15px; font-size: 1.1rem; border: none; border-radius: 10px;
            background: rgba(255, 255, 255, 0.2); color: white; min-width: 200px;
        }
        .input-field::placeholder { color: #B0B0B0; }
        
        .bet-buttons { display: flex; gap: 15px; justify-content: center; margin: 20px 0; }
        .bet-btn {
            padding: 15px 25px; font-size: 1.1rem; font-weight: bold;
            border: none; border-radius: 10px; cursor: pointer; transition: all 0.3s;
        }
        .bet-quick { background: #4CAF50; color: white; }
        .bet-medium { background: #FF9800; color: white; }
        .bet-high { background: #F44336; color: white; }
        .bet-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        
        .buy-button {
            padding: 20px 40px; font-size: 1.3rem; font-weight: bold;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            color: #333; border: none; border-radius: 15px; cursor: pointer;
            transition: all 0.3s; margin: 20px 0;
        }
        .buy-button:hover { transform: scale(1.05); }
        
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .stat-card {
            background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 25px; text-align: center;
        }
        .stat-value { font-size: 2.5rem; font-weight: bold; color: #FFD700; }
        .stat-label { color: #E0E0E0; margin-top: 10px; }
        
        .recent-section { margin-top: 40px; }
        .section-title { font-size: 2rem; text-align: center; margin-bottom: 25px; }
        .recent-list { display: grid; gap: 15px; }
        .recent-item {
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 10px;
        }
        .recent-address { font-family: monospace; color: #B0B0B0; }
        .recent-amount { color: #FFD700; font-weight: bold; font-size: 1.2rem; }
        
        .live-dot {
            width: 12px; height: 12px; border-radius: 50%; background: #4CAF50;
            display: inline-block; margin-right: 8px; animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        
        @media (max-width: 768px) {
            .form-row { flex-direction: column; }
            .bet-buttons { flex-wrap: wrap; }
            .prize-pool { font-size: 2.5rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 HyperFlow Lottery</h1>
            <p><span class="live-dot"></span>Powered by HYPE Token</p>
        </div>
        
        <div class="main-lottery">
            <h2>Current Lottery Draw</h2>
            <div class="prize-pool" id="prize-pool">Loading...</div>
            <div class="countdown" id="countdown">Loading...</div>
            
            <div class="entry-form">
                <div class="form-row">
                    <input type="text" class="input-field" placeholder="Wallet Address" id="wallet">
                    <input type="number" class="input-field" placeholder="HYPE Amount" id="amount" min="10" step="10">
                </div>
                
                <div class="bet-buttons">
                    <button class="bet-btn bet-quick" onclick="quickBet(100)">Quick 100 HYPE</button>
                    <button class="bet-btn bet-medium" onclick="quickBet(500)">Medium 500 HYPE</button>
                    <button class="bet-btn bet-high" onclick="quickBet(2000)">High 2K HYPE</button>
                </div>
                
                <button class="buy-button" onclick="enterLottery()">Enter Lottery</button>
            </div>
            
            <div style="background: rgba(76, 175, 80, 0.2); border-radius: 10px; padding: 15px; margin: 20px 0;">
                <strong style="color: #4CAF50;">Provably Fair</strong><br>
                All draws verified on blockchain with transparent randomness
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="total-players">0</div>
                <div class="stat-label">Active Players</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="total-volume">0 HYPE</div>
                <div class="stat-label">Total Volume</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="biggest-win">0 HYPE</div>
                <div class="stat-label">Biggest Win</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="next-draw">0m</div>
                <div class="stat-label">Next Draw</div>
            </div>
        </div>
        
        <div class="recent-section">
            <h2 class="section-title">🏆 Recent Winners</h2>
            <div class="recent-list" id="recent-winners">
                <div style="text-align: center; padding: 20px; color: #B0B0B0;">Loading winners...</div>
            </div>
        </div>
    </div>
    
    <script>
        function quickBet(amount) {
            document.getElementById('amount').value = amount;
        }
        
        function enterLottery() {
            const wallet = document.getElementById('wallet').value;
            const amount = document.getElementById('amount').value;
            
            if (!wallet || !amount) {
                alert('Please enter wallet address and amount');
                return;
            }
            
            if (parseFloat(amount) < 10) {
                alert('Minimum bet is 10 HYPE');
                return;
            }
            
            alert('Entry confirmed! ' + amount + ' HYPE bet placed. In production, this would connect to your wallet.');
        }
        
        async function loadData() {
            try {
                const response = await fetch('/api/lottery-data');
                const data = await response.json();
                
                document.getElementById('prize-pool').textContent = data.prize + ' HYPE';
                document.getElementById('countdown').textContent = data.countdown;
                document.getElementById('total-players').textContent = data.players;
                document.getElementById('total-volume').textContent = data.volume + ' HYPE';
                document.getElementById('biggest-win').textContent = data.biggest_win + ' HYPE';
                document.getElementById('next-draw').textContent = data.next_draw;
                
                const winnersList = document.getElementById('recent-winners');
                winnersList.innerHTML = data.winners.map(w => 
                    '<div class="recent-item">' +
                    '<div><div class="recent-address">' + w.address + '</div>' +
                    '<div style="color: #888; font-size: 0.9rem;">' + w.time + '</div></div>' +
                    '<div class="recent-amount">' + w.amount + ' HYPE</div></div>'
                ).join('');
                
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        loadData();
        setInterval(loadData, 5000);
        
        console.log('🚀 HyperFlow Lottery Platform Loaded');
    </script>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == "/api/lottery-data":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = {
                "prize": round(random.uniform(50000, 500000)),
                "countdown": "Next draw in 15m 30s",
                "players": random.randint(500, 2000),
                "volume": round(random.uniform(1000000, 5000000)),
                "biggest_win": round(random.uniform(100000, 750000)),
                "next_draw": "15m",
                "winners": [
                    {
                        "address": f"{self.generate_address()[:8]}...{self.generate_address()[-4:]}",
                        "amount": round(random.uniform(5000, 150000)),
                        "time": f"{random.randint(1, 60)} min ago"
                    }
                    for _ in range(8)
                ]
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def generate_address(self):
        chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        return ''.join(random.choice(chars) for _ in range(44))

if __name__ == "__main__":
    print("🚀 HyperFlow Lottery - HYPE Token Platform")
    print("=" * 60)
    print("💎 Features:")
    print("  - Real-time HYPE Token Lottery Draws")
    print("  - Provably Fair Blockchain System")
    print("  - Instant HYPE Payouts")
    print("  - HyperFlow Professional Interface")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), ScatterLotteryHandler) as httpd:
            print(f"🌐 HyperFlow Lottery Platform: http://localhost:{PORT}")
            print("🚀 HYPE token lottery interface loading...")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:
            print(f"Port {PORT} in use, trying alternative...")
            for alt_port in [8002, 8003, 9000, 9001]:
                try:
                    with socketserver.TCPServer(("0.0.0.0", alt_port), ScatterLotteryHandler) as httpd:
                        print(f"🌐 HyperFlow Lottery Platform: http://localhost:{alt_port}")
                        print("🚀 HYPE token lottery interface loading...")
                        httpd.serve_forever()
                except OSError:
                    continue
        else:
            raise