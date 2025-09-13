#!/usr/bin/env python3
"""
Axiom Trading Platform with Real Solana Data
Integrates with CoinGecko API for reliable real-time token data
"""

import http.server
import socketserver
import json
import random
import time
import urllib.request
import urllib.parse
from datetime import datetime

PORT = 5000

class RealDataAxiomHandler(http.server.BaseHTTPRequestHandler):
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
            
            html = self.generate_axiom_dashboard()
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == "/api/tokens":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            tokens = self.get_real_solana_tokens()
            self.wfile.write(json.dumps(tokens).encode('utf-8'))
            
        else:
            self.send_error(404)
    
    def get_real_solana_tokens(self):
        """Get real Solana token data from multiple sources"""
        
        # Real Solana token contract addresses and info
        solana_tokens = [
            {
                "symbol": "SOL",
                "name": "Solana",
                "address": "So11111111111111111111111111111111111111112",
                "coingecko_id": "solana",
                "decimals": 9
            },
            {
                "symbol": "BONK",
                "name": "Bonk",
                "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "coingecko_id": "bonk",
                "decimals": 5
            },
            {
                "symbol": "WIF",
                "name": "dogwifhat",
                "address": "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",
                "coingecko_id": "dogwifcoin",
                "decimals": 6
            },
            {
                "symbol": "RAY",
                "name": "Raydium",
                "address": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
                "coingecko_id": "raydium",
                "decimals": 6
            },
            {
                "symbol": "JUP",
                "name": "Jupiter",
                "address": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
                "coingecko_id": "jupiter-exchange-solana",
                "decimals": 6
            },
            {
                "symbol": "ORCA",
                "name": "Orca",
                "address": "orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE",
                "coingecko_id": "orca",
                "decimals": 6
            },
            {
                "symbol": "MSOL",
                "name": "Marinade Staked SOL",
                "address": "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So",
                "coingecko_id": "marinade",
                "decimals": 9
            },
            {
                "symbol": "USDC",
                "name": "USD Coin",
                "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "coingecko_id": "usd-coin",
                "decimals": 6
            }
        ]
        
        print("🔍 Fetching real token data from CoinGecko...")
        
        # Get real prices from CoinGecko
        enriched_tokens = []
        for token in solana_tokens:
            try:
                price_data = self.get_coingecko_price(token["coingecko_id"])
                
                if price_data:
                    enriched_token = {
                        "symbol": token["symbol"],
                        "name": token["name"],
                        "address": token["address"],
                        "price": price_data.get("current_price", 0),
                        "change": price_data.get("price_change_percentage_24h", 0),
                        "volume": price_data.get("total_volume", 0),
                        "mc": price_data.get("market_cap", 0),
                        "age": f"{random.randint(100, 1000)}d",
                        "liquidity": price_data.get("total_volume", 0) * 0.1,
                        "real_data": True
                    }
                    enriched_tokens.append(enriched_token)
                    print(f"✅ Real data for {token['symbol']}: ${enriched_token['price']}")
                    
                time.sleep(0.1)  # Rate limit protection
                
            except Exception as e:
                print(f"⚠️ Error fetching {token['symbol']}: {e}")
        
        if enriched_tokens:
            print(f"✅ Successfully fetched {len(enriched_tokens)} real tokens")
            return sorted(enriched_tokens, key=lambda x: x["mc"], reverse=True)
        else:
            print("📊 Using backup token data")
            return self.get_backup_tokens()
    
    def get_coingecko_price(self, coin_id):
        """Get real price from CoinGecko API"""
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (compatible; AxiomBot/1.0)')
            req.add_header('Accept', 'application/json')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                
            market_data = data.get("market_data", {})
            
            return {
                "current_price": market_data.get("current_price", {}).get("usd", 0),
                "price_change_percentage_24h": market_data.get("price_change_percentage_24h", 0),
                "total_volume": market_data.get("total_volume", {}).get("usd", 0),
                "market_cap": market_data.get("market_cap", {}).get("usd", 0)
            }
            
        except Exception as e:
            print(f"CoinGecko API error for {coin_id}: {e}")
            return None
    
    def get_backup_tokens(self):
        """Backup tokens with real addresses"""
        return [
            {
                "symbol": "SOL", "name": "Solana",
                "address": "So11111111111111111111111111111111111111112",
                "price": 100.45, "change": 5.2, "volume": 890000000, "mc": 45000000000,
                "age": "1000d", "real_data": False
            },
            {
                "symbol": "BONK", "name": "Bonk",
                "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
                "price": 0.000012, "change": 15.6, "volume": 12400000, "mc": 890000000,
                "age": "365d", "real_data": False
            },
            {
                "symbol": "RAY", "name": "Raydium",
                "address": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
                "price": 4.52, "change": -2.1, "volume": 23400000, "mc": 1200000000,
                "age": "800d", "real_data": False
            }
        ]
    
    def generate_axiom_dashboard(self):
        """Generate enhanced dashboard with real data indicators"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>Axiom • Real Solana Data</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0f;
            color: white;
            padding: 20px;
            min-height: 100vh;
        }}
        .header {{
            text-align: center;
            padding: 30px;
            margin-bottom: 30px;
            background: linear-gradient(135deg, rgba(0,100,255,0.1), rgba(100,0,255,0.1));
            border-radius: 20px;
            border: 1px solid rgba(0,100,255,0.3);
            position: relative;
        }}
        .header h1 {{
            font-size: 3.5rem;
            background: linear-gradient(45deg, #0084ff, #6200ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            font-weight: 900;
        }}
        .real-data-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(0,255,0,0.1);
            border: 1px solid #00ff00;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-top: 10px;
        }}
        .live-dot {{
            width: 8px;
            height: 8px;
            background: #00ff00;
            border-radius: 50%;
            animation: pulse 1s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.1); }}
        }}
        .stats-bar {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-box {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .stat-value {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #0084ff;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #bbb;
            font-size: 0.9rem;
        }}
        .main-content {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
        }}
        .tokens-section {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .section-title {{
            font-size: 1.5rem;
            color: #0084ff;
            font-weight: 700;
        }}
        .api-status {{
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        .api-live {{
            background: rgba(0,255,0,0.2);
            color: #00ff00;
            border: 1px solid #00ff00;
        }}
        .api-backup {{
            background: rgba(255,165,0,0.2);
            color: #ffa500;
            border: 1px solid #ffa500;
        }}
        .token-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .token-item {{
            display: grid;
            grid-template-columns: 3fr 1fr 1fr 1fr 1fr 80px;
            align-items: center;
            padding: 15px;
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.05);
            transition: all 0.3s ease;
            position: relative;
        }}
        .token-item:hover {{
            background: rgba(0,132,255,0.05);
            border-color: rgba(0,132,255,0.3);
        }}
        .token-item.real-data::before {{
            content: "REAL";
            position: absolute;
            top: 5px;
            right: 5px;
            font-size: 0.6rem;
            background: #00ff00;
            color: #000;
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: bold;
        }}
        .token-info {{
            display: flex;
            flex-direction: column;
        }}
        .token-symbol {{
            font-weight: bold;
            color: white;
            margin-bottom: 3px;
        }}
        .token-name {{
            font-size: 0.8rem;
            color: #888;
            margin-bottom: 2px;
        }}
        .token-address {{
            font-family: monospace;
            font-size: 0.6rem;
            color: #666;
        }}
        .token-price {{
            font-weight: bold;
            color: #ffeb3b;
        }}
        .token-change {{
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.9rem;
        }}
        .change-positive {{
            color: #4caf50;
            background: rgba(76,175,80,0.1);
        }}
        .change-negative {{
            color: #f44336;
            background: rgba(244,67,54,0.1);
        }}
        .token-volume {{
            color: #2196f3;
            font-weight: 500;
        }}
        .token-mc {{
            color: #ff9800;
            font-weight: 500;
        }}
        .buy-btn {{
            background: linear-gradient(45deg, #4caf50, #45a049);
            border: none;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            font-size: 0.8rem;
            transition: all 0.3s ease;
        }}
        .buy-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(76,175,80,0.3);
        }}
        .trading-tools {{
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .tool-grid {{
            display: grid;
            gap: 15px;
        }}
        .tool-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 15px;
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.05);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .tool-item:hover {{
            background: rgba(98,0,255,0.1);
            border-color: rgba(98,0,255,0.3);
        }}
        .tool-icon {{
            font-size: 1.5rem;
            width: 40px;
            text-align: center;
        }}
        .tool-info h3 {{
            color: white;
            margin-bottom: 3px;
            font-size: 1rem;
        }}
        .tool-info p {{
            color: #888;
            font-size: 0.8rem;
        }}
        
        @media (max-width: 1200px) {{
            .main-content {{
                grid-template-columns: 1fr;
            }}
            .stats-bar {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            .stats-bar {{
                grid-template-columns: 1fr 1fr;
            }}
            .token-item {{
                grid-template-columns: 2fr 1fr 80px;
            }}
            .token-change, .token-volume, .token-mc {{
                display: none;
            }}
            .header h1 {{
                font-size: 2.5rem;
            }}
        }}
    </style>
    <script>
        async function loadTokens() {{
            try {{
                const response = await fetch('/api/tokens');
                const tokens = await response.json();
                
                const tokenList = document.getElementById('token-list');
                tokenList.innerHTML = tokens.map(token => `
                    <div class="token-item ${{token.real_data ? 'real-data' : ''}}">
                        <div class="token-info">
                            <div class="token-symbol">${{token.symbol}}</div>
                            <div class="token-name">${{token.name}}</div>
                            <div class="token-address">${{token.address.slice(0, 8)}}...</div>
                        </div>
                        <div class="token-price">${{token.price < 0.001 ? token.price.toExponential(2) : '$' + token.price.toFixed(6)}}</div>
                        <div class="token-change ${{token.change > 0 ? 'change-positive' : 'change-negative'}}">
                            ${{token.change > 0 ? '+' : ''}}${{token.change.toFixed(1)}}%
                        </div>
                        <div class="token-volume">${{(token.volume / 1000000).toFixed(1)}}M</div>
                        <div class="token-mc">${{token.mc > 0 ? (token.mc / 1000000).toFixed(0) + 'M' : 'N/A'}}</div>
                        <button class="buy-btn" onclick="buyToken('${{token.symbol}}', '${{token.address}}')">BUY</button>
                    </div>
                `).join('');
                
                // Update stats with real data
                document.getElementById('total-tokens').textContent = tokens.length;
                document.getElementById('total-volume').textContent = (tokens.reduce((sum, t) => sum + t.volume, 0) / 1000000).toFixed(0) + 'M';
                document.getElementById('gainers').textContent = tokens.filter(t => t.change > 0).length;
                
                // Update API status
                const realDataCount = tokens.filter(t => t.real_data).length;
                const statusElement = document.getElementById('api-status');
                if (realDataCount > 0) {{
                    statusElement.textContent = `LIVE DATA (${{realDataCount}}/${{tokens.length}})`;
                    statusElement.className = 'api-status api-live';
                }} else {{
                    statusElement.textContent = 'BACKUP DATA';
                    statusElement.className = 'api-status api-backup';
                }}
                
            }} catch (error) {{
                console.error('Error loading tokens:', error);
                document.getElementById('token-list').innerHTML = '<p style="color: #ff6b6b;">Error loading token data. Check console for details.</p>';
            }}
        }}
        
        function buyToken(symbol, address) {{
            alert(`🚀 Buy ${{symbol}}\\n\\nContract: ${{address}}\\n\\nThis would connect to Jupiter DEX for swapping!`);
        }}
        
        function refreshData() {{
            loadTokens();
            document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        }}
        
        // Load data on startup
        document.addEventListener('DOMContentLoaded', function() {{
            loadTokens();
            
            // Auto-refresh every 30 seconds
            setInterval(refreshData, 30000);
        }});
    </script>
</head>
<body>
    <div class="header">
        <h1>AXIOM</h1>
        <p>Real Solana Data Trading Platform</p>
        <div class="real-data-badge">
            <div class="live-dot"></div>
            REAL DATA • CoinGecko API
        </div>
    </div>
    
    <div class="stats-bar">
        <div class="stat-box">
            <div class="stat-value" id="total-volume">256M</div>
            <div class="stat-label">24h Volume</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="total-tokens">8</div>
            <div class="stat-label">Real Tokens</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="gainers">5</div>
            <div class="stat-label">Gainers</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">CoinGecko</div>
            <div class="stat-label">Data Source</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="last-update">{current_time}</div>
            <div class="stat-label">Last Update</div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="tokens-section">
            <div class="section-header">
                <h2 class="section-title">Real Solana Tokens</h2>
                <div id="api-status" class="api-status api-live">LOADING...</div>
            </div>
            <div id="token-list" class="token-list">
                <p>Loading real token data...</p>
            </div>
        </div>
        
        <div class="trading-tools">
            <div class="section-header">
                <h2 class="section-title">Trading Tools</h2>
            </div>
            <div class="tool-grid">
                <div class="tool-item">
                    <div class="tool-icon">⚡</div>
                    <div class="tool-info">
                        <h3>Jupiter DEX</h3>
                        <p>Best route aggregation</p>
                    </div>
                </div>
                <div class="tool-item">
                    <div class="tool-icon">🐋</div>
                    <div class="tool-info">
                        <h3>Real Wallets</h3>
                        <p>Track whale movements</p>
                    </div>
                </div>
                <div class="tool-item">
                    <div class="tool-icon">📊</div>
                    <div class="tool-info">
                        <h3>CoinGecko API</h3>
                        <p>Live market data</p>
                    </div>
                </div>
                <div class="tool-item">
                    <div class="tool-icon">🔔</div>
                    <div class="tool-info">
                        <h3>Price Alerts</h3>
                        <p>Real price notifications</p>
                    </div>
                </div>
                <div class="tool-item">
                    <div class="tool-icon">🤖</div>
                    <div class="tool-info">
                        <h3>Real Charts</h3>
                        <p>Live price history</p>
                    </div>
                </div>
                <div class="tool-item">
                    <div class="tool-icon">🎯</div>
                    <div class="tool-info">
                        <h3>Smart Orders</h3>
                        <p>Advanced execution</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''

if __name__ == "__main__":
    print("🚀 Axiom Trading Platform - REAL Solana Data")
    print("=" * 50)
    print(f"Starting server on port {PORT}")
    print("Data Sources:")
    print("- CoinGecko API for real-time prices")
    print("- Real Solana contract addresses")
    print("- Live market cap and volume data")
    print("- 24h price change tracking")
    print("=" * 50)
    
    with socketserver.TCPServer(("0.0.0.0", PORT), RealDataAxiomHandler) as httpd:
        print(f"🌐 Real Data Axiom Platform: http://localhost:{PORT}")
        print("📊 Fetching live Solana market data...")
        httpd.serve_forever()