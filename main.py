#!/usr/bin/env python3
"""
HyperFlow Protocol - Main Entry Point
Optimized for Replit external access
"""
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse

class HyperFlowServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        # Set CORS headers for all responses
        self.send_response(200)
        self.send_header('Content-Type', 'application/json' if path.startswith('/api') else 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            if path == '/':
                self.wfile.write(self.get_main_page().encode())
            elif path == '/api/nft-stats':
                self.wfile.write(json.dumps({
                    'name': 'Wealthy Hypio Babies',
                    'floor_price': 61.799,
                    'floor_price_symbol': 'HYPE',
                    'total_supply': 5555,
                    'unique_owners': 2770,
                    'total_volume': '543514'
                }).encode())
            elif path == '/api/live-data':
                self.wfile.write(json.dumps({
                    'tvl': '2.1B',
                    'volume_24h': '145.7M',
                    'active_vaults': 12,
                    'total_users': 15420
                }).encode())
            elif path.startswith('/api/nfts'):
                nfts = []
                for i in range(1, 13):
                    nfts.append({
                        'id': i,
                        'name': f'Hypio Baby #{i}',
                        'image': f'https://images.weserv.nl/?url=https://gateway.pinata.cloud/ipfs/QmYjKpP8jEzTNyUPBRKWJSqGowFsVDBLJ7Z7GnkYRV9a5s/{i}.png&w=400&h=400',
                        'price': 61.799 + (i % 20)
                    })
                self.wfile.write(json.dumps(nfts).encode())
            else:
                self.send_error(404)
        except Exception as e:
            print(f"Error handling request: {e}")
            self.send_error(500)
    
    def get_main_page(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow Protocol - DeFi Infrastructure</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; overflow-x: hidden;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 15px; }
        .hero { text-align: center; padding: 30px 15px; }
        .hero h1 { font-size: 2.2em; margin-bottom: 15px; }
        .hero p { font-size: 1.1em; opacity: 0.9; }
        .menu { 
            display: flex; justify-content: center; gap: 15px; margin: 25px 0;
            flex-wrap: wrap; padding: 0 10px;
        }
        .menu-btn { 
            background: rgba(255,255,255,0.2); 
            padding: 10px 18px; border-radius: 20px; 
            border: none; color: white; cursor: pointer;
            transition: all 0.3s; font-size: 0.9em;
        }
        .menu-btn:hover, .menu-btn.active { 
            background: rgba(255,255,255,0.4); 
            transform: translateY(-2px);
        }
        .section { margin: 25px 0; }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); 
            gap: 12px; margin: 20px 0; 
        }
        .stat-card { 
            background: rgba(255,255,255,0.15); 
            padding: 18px; border-radius: 12px; text-align: center; 
            backdrop-filter: blur(10px);
        }
        .stat-value { font-size: 1.8em; font-weight: bold; color: #00ff88; }
        .stat-label { margin-top: 6px; opacity: 0.85; font-size: 0.85em; }
        .nft-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); 
            gap: 12px; 
        }
        .nft-card { 
            background: rgba(255,255,255,0.15); 
            border-radius: 10px; overflow: hidden; 
            transition: transform 0.3s;
        }
        .nft-card:hover { transform: translateY(-3px); }
        .nft-image { width: 100%; height: 160px; object-fit: cover; }
        .nft-info { padding: 10px; }
        .nft-name { font-weight: 600; margin-bottom: 4px; font-size: 0.85em; }
        .nft-price { color: #00ff88; font-size: 0.9em; }
        .loading { text-align: center; padding: 30px; opacity: 0.7; }
        .status { 
            position: fixed; top: 15px; right: 15px; 
            background: rgba(0,255,136,0.2); 
            padding: 8px 12px; border-radius: 15px; 
            font-size: 0.8em; z-index: 1000;
        }
        @media (max-width: 768px) {
            .hero h1 { font-size: 1.8em; }
            .hero p { font-size: 1em; }
            .stats-grid { grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); }
            .nft-grid { grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); }
            .menu { gap: 10px; }
            .menu-btn { padding: 8px 14px; font-size: 0.8em; }
        }
    </style>
</head>
<body>
    <div class="status">🟢 Live</div>
    
    <div class="container">
        <div class="hero">
            <h1>🌊 HyperFlow Protocol</h1>
            <p>Next-Generation DeFi Infrastructure on HyperEVM</p>
        </div>
        
        <nav class="menu">
            <button class="menu-btn active" onclick="showSection('dashboard')">📊 Dashboard</button>
            <button class="menu-btn" onclick="showSection('vaults')">🏦 Vaults</button>  
            <button class="menu-btn" onclick="showSection('bridge')">🌉 Bridge</button>
            <button class="menu-btn" onclick="showSection('nfts')">🎨 NFT Collection</button>
        </nav>
        
        <div id="dashboard" class="section">
            <div class="stats-grid" id="stats-container">
                <div class="loading">Loading protocol stats...</div>
            </div>
        </div>
        
        <div id="nfts" class="section" style="display:none;">
            <h2 style="text-align: center; margin-bottom: 20px;">🎨 Wealthy Hypio Babies Collection</h2>
            <div class="stats-grid" id="nft-stats-container">
                <div class="loading">Loading collection stats...</div>
            </div>
            <div class="nft-grid" id="nft-container">
                <div class="loading">Loading NFTs...</div>
            </div>
        </div>
        
        <div id="vaults" class="section" style="display:none;">
            <h2 style="text-align: center; margin-bottom: 20px;">🏦 Smart Vaults</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">12.5%</div>
                    <div class="stat-label">Delta Neutral Vault APY</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">15.2%</div>
                    <div class="stat-label">Yield Optimizer APY</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">18.5%</div>
                    <div class="stat-label">FLOW Staking APY</div>
                </div>
            </div>
        </div>
        
        <div id="bridge" class="section" style="display:none;">
            <h2 style="text-align: center; margin-bottom: 20px;">🌉 Cross-Chain Bridge</h2>
            <div class="stat-card">
                <div class="stat-value">⚡</div>
                <div class="stat-label">Instant transfers between HyperEVM and Base networks</div>
            </div>
        </div>
    </div>
    
    <script>
        function showSection(sectionName) {
            document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
            document.querySelectorAll('.menu-btn').forEach(m => m.classList.remove('active'));
            
            document.getElementById(sectionName).style.display = 'block';
            event.target.classList.add('active');
            
            if (sectionName === 'nfts') loadNFTData();
            else if (sectionName === 'dashboard') loadDashboardData();
        }
        
        function loadData(url, containerId, renderer) {
            fetch(url)
                .then(r => r.json())
                .then(renderer)
                .catch(() => document.getElementById(containerId).innerHTML = '<div class="loading">Data unavailable</div>');
        }
        
        function loadDashboardData() {
            loadData('/api/live-data', 'stats-container', data => {
                document.getElementById('stats-container').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-value">$${data.tvl}</div>
                        <div class="stat-label">Total Value Locked</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">$${data.volume_24h}</div>
                        <div class="stat-label">24h Volume</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${data.active_vaults}</div>
                        <div class="stat-label">Active Vaults</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${data.total_users.toLocaleString()}</div>
                        <div class="stat-label">Total Users</div>
                    </div>
                `;
            });
        }
        
        function loadNFTData() {
            loadData('/api/nft-stats', 'nft-stats-container', data => {
                document.getElementById('nft-stats-container').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-value">${data.floor_price} ${data.floor_price_symbol}</div>
                        <div class="stat-label">Floor Price</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${data.total_supply.toLocaleString()}</div>
                        <div class="stat-label">Total Supply</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${data.unique_owners.toLocaleString()}</div>
                        <div class="stat-label">Unique Owners</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${parseFloat(data.total_volume).toLocaleString()} ${data.floor_price_symbol}</div>
                        <div class="stat-label">Total Volume</div>
                    </div>
                `;
            });
            
            loadData('/api/nfts/random', 'nft-container', nfts => {
                document.getElementById('nft-container').innerHTML = nfts.map(nft => `
                    <div class="nft-card">
                        <img src="${nft.image}" alt="${nft.name}" class="nft-image" 
                             onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjNjY3ZWVhIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iI2ZmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPiMke25mdC5pZH08L3RleHQ+PC9zdmc+'">
                        <div class="nft-info">
                            <div class="nft-name">${nft.name}</div>
                            <div class="nft-price">${nft.price} HYPE</div>
                        </div>
                    </div>
                `).join('');
            });
        }
        
        // Initialize
        loadDashboardData();
    </script>
</body>
</html>"""

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    
    print(f"🚀 HyperFlow Protocol starting on port {PORT}")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), HyperFlowServer) as httpd:
            httpd.allow_reuse_address = True
            print(f"✅ Server running on http://0.0.0.0:{PORT}")
            print("🌐 External access configured")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Server error: {e}")