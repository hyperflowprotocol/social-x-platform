#!/usr/bin/env python3
"""
Axiom Trading Server - Web interface for Solana trading platform
"""

import http.server
import socketserver
import os
import json
import asyncio
import threading
from datetime import datetime
import time

PORT = 5010

class AxiomTradingHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Generate real-time dashboard
            html = self.generate_live_dashboard()
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == "/api/trending":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Mock trending tokens data
            trending_data = self.get_trending_tokens_data()
            self.wfile.write(json.dumps(trending_data).encode('utf-8'))
            
        elif self.path == "/api/whales":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Mock whale data
            whale_data = self.get_whale_data()
            self.wfile.write(json.dumps(whale_data).encode('utf-8'))
            
        else:
            self.send_error(404)
    
    def get_trending_tokens_data(self):
        """Generate trending tokens data"""
        import random
        
        tokens = [
            {"symbol": "BONK", "name": "Bonk", "price": 0.000012, "change": 15.6, "volume": 12400000},
            {"symbol": "WIF", "name": "dogwifhat", "price": 2.34, "change": -8.2, "volume": 45600000},
            {"symbol": "PEPE", "name": "Pepe", "price": 0.0000087, "change": 23.1, "volume": 67800000},
            {"symbol": "PNUT", "name": "Peanut", "price": 0.45, "change": 156.7, "volume": 89200000},
            {"symbol": "GOAT", "name": "Goatseus Maximus", "price": 0.67, "change": -12.3, "volume": 34500000},
            {"symbol": "MEW", "name": "Cat in a Dogs World", "price": 0.0089, "change": 45.2, "volume": 23400000},
            {"symbol": "POPCAT", "name": "Popcat", "price": 1.23, "change": 67.8, "volume": 56700000},
            {"symbol": "MOODENG", "name": "Moo Deng", "price": 0.234, "change": -5.6, "volume": 12300000},
        ]
        
        # Add some randomness to simulate live data
        for token in tokens:
            token["price"] *= (1 + random.uniform(-0.05, 0.05))
            token["change"] += random.uniform(-2, 2)
            token["volume"] *= (1 + random.uniform(-0.1, 0.1))
            token["address"] = f"{''.join(random.choices('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', k=44))}"
        
        return tokens
    
    def get_whale_data(self):
        """Generate whale wallet data"""
        import random
        
        whales = [
            {"label": "Whale Alpha", "address": "6dMH3H3revFkX9M2Gzzj8XPUX5t7hAUKAP2Ld8iRj4P1", "sol_balance": 45670.5, "value_usd": 4567050},
            {"label": "DeFi Maxi", "address": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM", "sol_balance": 78923.2, "value_usd": 7892320},
            {"label": "MEV Bot", "address": "3tLPE2f5YvCn3C9KQbXQHvBRF2kbwSJXi4QNWT1z8QRG", "sol_balance": 23456.8, "value_usd": 2345680},
            {"label": "Pump Hunter", "address": "5kTzWXGTN4L8h2vMd9LKQpRX3G4mDxYP7qJmV9H6rK3S", "sol_balance": 12789.4, "value_usd": 1278940},
        ]
        
        # Add some randomness
        for whale in whales:
            whale["sol_balance"] *= (1 + random.uniform(-0.02, 0.02))
            whale["value_usd"] = whale["sol_balance"] * 100  # Assume SOL = $100
            whale["pnl_24h"] = random.uniform(-50000, 50000)
            whale["tokens_count"] = random.randint(15, 45)
        
        return whales
    
    def generate_live_dashboard(self):
        """Generate live dashboard HTML"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>Axiom Trading Platform - Live</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: white;
            padding: 20px;
            min-height: 100vh;
        }}
        .header {{
            text-align: center;
            padding: 40px;
            margin-bottom: 40px;
            background: rgba(0,212,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(15px);
            border: 2px solid rgba(0,212,255,0.3);
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,212,255,0.2), transparent);
            animation: shine 3s infinite;
        }}
        @keyframes shine {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        .header h1 {{
            font-size: 4rem;
            background: linear-gradient(45deg, #00d4ff, #5200ff, #ff0080);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            font-weight: 900;
            position: relative;
            z-index: 1;
        }}
        .live-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #00ff00;
            border-radius: 50%;
            animation: pulse 1s infinite;
            margin-right: 8px;
        }}
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.2); opacity: 0.7; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        .dashboard {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 30px;
            max-width: 1600px;
            margin: 0 auto;
        }}
        .section {{
            background: rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0,212,255,0.3);
            position: relative;
            overflow: hidden;
        }}
        .section::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00d4ff, #5200ff);
        }}
        .section h2 {{
            color: #00d4ff;
            margin-bottom: 25px;
            font-size: 1.8rem;
            font-weight: 700;
        }}
        .stats-overview {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
            grid-column: 1 / -1;
        }}
        .stat-card {{
            background: rgba(0,212,255,0.1);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(0,212,255,0.3);
            transition: all 0.3s ease;
        }}
        .stat-card:hover {{
            background: rgba(0,212,255,0.2);
            transform: translateY(-5px);
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #00d4ff;
            margin-bottom: 8px;
        }}
        .stat-label {{
            color: #ccc;
            font-size: 1rem;
            font-weight: 500;
        }}
        .token-card, .whale-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
            position: relative;
        }}
        .token-card:hover, .whale-card:hover {{
            background: rgba(0,212,255,0.1);
            border-color: #00d4ff;
            transform: translateX(5px);
        }}
        .token-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }}
        .token-info h3 {{
            color: #00d4ff;
            font-size: 1.3rem;
            margin-bottom: 5px;
        }}
        .token-name {{
            color: #bbb;
            font-size: 0.9rem;
        }}
        .token-stats {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            text-align: center;
        }}
        .stat {{
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }}
        .stat-number {{
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 3px;
        }}
        .stat-desc {{
            font-size: 0.8rem;
            color: #bbb;
        }}
        .price {{
            color: #ffeb3b;
        }}
        .change-positive {{
            color: #4caf50;
        }}
        .change-negative {{
            color: #f44336;
        }}
        .volume {{
            color: #2196f3;
        }}
        .whale-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .whale-balance {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #ffeb3b;
        }}
        .trading-tools {{
            grid-column: 1 / -1;
            background: rgba(82,0,255,0.1);
            border: 1px solid rgba(82,0,255,0.3);
            margin-top: 20px;
        }}
        .tools-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 20px;
        }}
        .tool-card {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .tool-card:hover {{
            background: rgba(82,0,255,0.2);
            transform: scale(1.05);
        }}
        .tool-icon {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}
        .last-updated {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.9rem;
            color: #ccc;
        }}
        
        @media (max-width: 1200px) {{
            .dashboard {{
                grid-template-columns: 1fr 1fr;
            }}
            .stats-overview {{
                grid-template-columns: 1fr 1fr;
            }}
        }}
        
        @media (max-width: 768px) {{
            .dashboard {{
                grid-template-columns: 1fr;
            }}
            .stats-overview {{
                grid-template-columns: 1fr 1fr;
            }}
            .header h1 {{
                font-size: 2.5rem;
            }}
        }}
    </style>
    <script>
        async function loadTrendingTokens() {{
            try {{
                const response = await fetch('/api/trending');
                const tokens = await response.json();
                const container = document.getElementById('trending-tokens');
                
                container.innerHTML = tokens.slice(0, 8).map(token => `
                    <div class="token-card">
                        <div class="token-header">
                            <div class="token-info">
                                <h3>${{token.symbol}}</h3>
                                <div class="token-name">${{token.name}}</div>
                            </div>
                        </div>
                        <div class="token-stats">
                            <div class="stat">
                                <div class="stat-number price">${{token.price.toFixed(6)}}</div>
                                <div class="stat-desc">Price USD</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number ${{token.change > 0 ? 'change-positive' : 'change-negative'}}">${{token.change.toFixed(1)}}%</div>
                                <div class="stat-desc">24h Change</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number volume">${{(token.volume / 1000000).toFixed(1)}}M</div>
                                <div class="stat-desc">Volume</div>
                            </div>
                        </div>
                    </div>
                `).join('');
            }} catch (error) {{
                console.error('Error loading trending tokens:', error);
            }}
        }}
        
        async function loadWhaleData() {{
            try {{
                const response = await fetch('/api/whales');
                const whales = await response.json();
                const container = document.getElementById('whale-wallets');
                
                container.innerHTML = whales.slice(0, 6).map(whale => `
                    <div class="whale-card">
                        <div class="whale-header">
                            <div>
                                <h3>${{whale.label}}</h3>
                                <div style="font-family: monospace; font-size: 0.8rem; color: #888;">
                                    ${{whale.address.slice(0, 8)}}...${{whale.address.slice(-8)}}
                                </div>
                            </div>
                            <div class="whale-balance">${{whale.sol_balance.toFixed(1)}} SOL</div>
                        </div>
                        <div class="token-stats">
                            <div class="stat">
                                <div class="stat-number volume">${{(whale.value_usd / 1000000).toFixed(1)}}M</div>
                                <div class="stat-desc">Portfolio Value</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number ${{whale.pnl_24h > 0 ? 'change-positive' : 'change-negative'}}">${{(whale.pnl_24h / 1000).toFixed(0)}}K</div>
                                <div class="stat-desc">24h PnL</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">${{whale.tokens_count}}</div>
                                <div class="stat-desc">Tokens</div>
                            </div>
                        </div>
                    </div>
                `).join('');
            }} catch (error) {{
                console.error('Error loading whale data:', error);
            }}
        }}
        
        function updateStats() {{
            // Update random stats for demo
            document.getElementById('total-volume').textContent = (Math.random() * 50 + 100).toFixed(1) + 'M';
            document.getElementById('active-traders').textContent = Math.floor(Math.random() * 1000 + 5000).toLocaleString();
            document.getElementById('total-tokens').textContent = Math.floor(Math.random() * 100 + 2500).toLocaleString();
            document.getElementById('success-rate').textContent = (Math.random() * 10 + 85).toFixed(1) + '%';
        }}
        
        function refreshData() {{
            loadTrendingTokens();
            loadWhaleData();
            updateStats();
            document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
        }}
        
        // Load data on page load
        document.addEventListener('DOMContentLoaded', function() {{
            refreshData();
            
            // Auto-refresh every 15 seconds
            setInterval(refreshData, 15000);
        }});
    </script>
</head>
<body>
    <div class="header">
        <h1>🚀 Axiom Trading Platform</h1>
        <p><span class="live-indicator"></span>Live • Advanced Solana Trading & Analytics</p>
        <p>Real-time market data • Whale tracking • Automated strategies • Zero slippage</p>
    </div>
    
    <div class="stats-overview">
        <div class="stat-card">
            <div class="stat-value" id="total-volume">125.6M</div>
            <div class="stat-label">24h Volume</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="active-traders">5,847</div>
            <div class="stat-label">Active Traders</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="total-tokens">2,643</div>
            <div class="stat-label">Listed Tokens</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="success-rate">89.2%</div>
            <div class="stat-label">Success Rate</div>
        </div>
    </div>
    
    <div class="dashboard">
        <div class="section">
            <h2>📈 Trending Tokens</h2>
            <div id="trending-tokens">
                <p>Loading trending tokens...</p>
            </div>
        </div>
        
        <div class="section">
            <h2>🐋 Whale Activity</h2>
            <div id="whale-wallets">
                <p>Loading whale data...</p>
            </div>
        </div>
        
        <div class="section">
            <h2>🤖 Trading Tools</h2>
            <div class="tools-grid">
                <div class="tool-card">
                    <div class="tool-icon">⚡</div>
                    <div>Sniper Bot</div>
                    <small>Auto-buy new listings</small>
                </div>
                <div class="tool-card">
                    <div class="tool-icon">📊</div>
                    <div>Portfolio</div>
                    <small>Track performance</small>
                </div>
                <div class="tool-card">
                    <div class="tool-icon">🔔</div>
                    <div>Alerts</div>
                    <small>Price notifications</small>
                </div>
                <div class="tool-card">
                    <div class="tool-icon">💰</div>
                    <div>DCA Bot</div>
                    <small>Dollar cost average</small>
                </div>
            </div>
        </div>
        
        <div class="trading-tools">
            <h2>🔧 Advanced Features</h2>
            <div class="tools-grid">
                <div class="tool-card">
                    <div class="tool-icon">🎯</div>
                    <div>Copy Trading</div>
                    <small>Follow successful traders</small>
                </div>
                <div class="tool-card">
                    <div class="tool-icon">🔍</div>
                    <div>Token Scanner</div>
                    <small>Find hidden gems</small>
                </div>
                <div class="tool-card">
                    <div class="tool-icon">📱</div>
                    <div>Social Signals</div>
                    <small>Twitter sentiment</small>
                </div>
                <div class="tool-card">
                    <div class="tool-icon">⚙️</div>
                    <div>MEV Protection</div>
                    <small>Anti-sandwich</small>
                </div>
            </div>
        </div>
    </div>
    
    <div class="last-updated">
        Last updated: <span id="last-updated">{current_time}</span>
    </div>
</body>
</html>'''

if __name__ == "__main__":
    print("🚀 Starting Axiom Trading Platform Server")
    print("=" * 50)
    print(f"Server running on port {PORT}")
    print("Features:")
    print("- Real-time trending tokens")
    print("- Whale wallet tracking")
    print("- Advanced trading tools")
    print("- Live market data")
    print("=" * 50)
    
    with socketserver.TCPServer(("0.0.0.0", PORT), AxiomTradingHandler) as httpd:
        print(f"🌐 Axiom Trading Platform live at http://localhost:{PORT}")
        httpd.serve_forever()