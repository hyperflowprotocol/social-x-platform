#!/usr/bin/env python3
import http.server
import socketserver
import json
import threading
import time

PORT = 5000

class HyperFlowHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_html()
        elif self.path == '/api/nft-stats':
            self.serve_json({
                'name': 'Wealthy Hypio Babies',
                'floor_price': 61.799,
                'floor_price_symbol': 'HYPE',
                'total_supply': 5555,
                'unique_owners': 2770,
                'total_volume': '543514'
            })
        elif self.path == '/api/live-data':
            self.serve_json({
                'tvl': '2.1B',
                'volume_24h': '145.7M', 
                'active_vaults': 12,
                'total_users': 15420
            })
        elif self.path.startswith('/api/nfts'):
            nfts = []
            for i in range(1, 13):
                nfts.append({
                    'id': i,
                    'name': f'Hypio Baby #{i}',
                    'image': f'https://images.weserv.nl/?url=https://gateway.pinata.cloud/ipfs/QmYjKpP8jEzTNyUPBRKWJSqGowFsVDBLJ7Z7GnkYRV9a5s/{i}.png&w=400&h=400',
                    'price': 61.799 + (i % 20)
                })
            self.serve_json(nfts)
        else:
            self.send_error(404)
    
    def serve_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def serve_html(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html>
<head>
    <title>HyperFlow Protocol - DeFi Infrastructure</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .hero { text-align: center; padding: 40px 20px; }
        .hero h1 { font-size: 2.5em; margin-bottom: 15px; }
        .hero p { font-size: 1.2em; opacity: 0.9; }
        .menu { 
            display: flex; justify-content: center; gap: 20px; margin: 30px 0;
            flex-wrap: wrap;
        }
        .menu-item { 
            background: rgba(255,255,255,0.2); 
            padding: 12px 20px; border-radius: 20px; 
            text-decoration: none; color: white;
            transition: all 0.3s; cursor: pointer; border: none;
        }
        .menu-item:hover, .menu-item.active { 
            background: rgba(255,255,255,0.4); 
        }
        .section { margin: 30px 0; }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; margin: 30px 0; 
        }
        .stat-card { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; border-radius: 12px; text-align: center; 
        }
        .stat-value { font-size: 2em; font-weight: bold; color: #00ff88; }
        .stat-label { margin-top: 8px; opacity: 0.8; font-size: 0.9em; }
        .nft-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); 
            gap: 15px; 
        }
        .nft-card { 
            background: rgba(255,255,255,0.1); 
            border-radius: 12px; overflow: hidden; 
            transition: transform 0.3s;
        }
        .nft-card:hover { transform: translateY(-3px); }
        .nft-image { width: 100%; height: 180px; object-fit: cover; }
        .nft-info { padding: 12px; }
        .nft-name { font-weight: bold; margin-bottom: 4px; font-size: 0.9em; }
        .nft-price { color: #00ff88; font-size: 1em; }
        .loading { text-align: center; padding: 30px; opacity: 0.7; }
        @media (max-width: 768px) {
            .hero h1 { font-size: 2em; }
            .stats-grid { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }
            .nft-grid { grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>🌊 HyperFlow Protocol</h1>
            <p>Next-Generation DeFi Infrastructure on HyperEVM</p>
        </div>
        
        <nav class="menu">
            <button class="menu-item active" onclick="showSection('dashboard')">📊 Dashboard</button>
            <button class="menu-item" onclick="showSection('vaults')">🏦 Vaults</button>  
            <button class="menu-item" onclick="showSection('bridge')">🌉 Bridge</button>
            <button class="menu-item" onclick="showSection('nfts')">🎨 NFT Collection</button>
        </nav>
        
        <div id="dashboard" class="section">
            <div class="stats-grid" id="stats-container">
                <div class="loading">Loading protocol stats...</div>
            </div>
        </div>
        
        <div id="nfts" class="section" style="display:none;">
            <h2 style="text-align: center; margin-bottom: 25px;">🎨 Wealthy Hypio Babies Collection</h2>
            <div class="stats-grid" id="nft-stats-container">
                <div class="loading">Loading collection stats...</div>
            </div>
            <div class="nft-grid" id="nft-container">
                <div class="loading">Loading NFTs...</div>
            </div>
        </div>
        
        <div id="vaults" class="section" style="display:none;">
            <h2 style="text-align: center; margin-bottom: 25px;">🏦 Smart Vaults</h2>
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
            <h2 style="text-align: center; margin-bottom: 25px;">🌉 Cross-Chain Bridge</h2>
            <div class="stat-card">
                <div class="stat-value">⚡</div>
                <div class="stat-label">Instant transfers between HyperEVM and Base networks</div>
            </div>
        </div>
    </div>
    
    <script>
        function showSection(sectionName) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
            // Remove active class from all menu items
            document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
            
            // Show selected section and activate menu item
            document.getElementById(sectionName).style.display = 'block';
            event.target.classList.add('active');
            
            // Load data for specific sections
            if (sectionName === 'nfts') {
                loadNFTData();
            } else if (sectionName === 'dashboard') {
                loadDashboardData();
            }
        }
        
        function loadDashboardData() {
            fetch('/api/live-data')
                .then(r => r.json())
                .then(data => {
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
                })
                .catch(() => {
                    document.getElementById('stats-container').innerHTML = '<div class="loading">Unable to load data</div>';
                });
        }
        
        function loadNFTData() {
            // Load collection stats
            fetch('/api/nft-stats')
                .then(r => r.json())
                .then(data => {
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
            
            // Load NFT grid
            fetch('/api/nfts/random')
                .then(r => r.json())
                .then(nfts => {
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
        
        // Initialize dashboard
        loadDashboardData();
    </script>
</body>
</html>"""
        self.wfile.write(html.encode())

def start_server():
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), HyperFlowHandler) as server:
            server.allow_reuse_address = True
            print(f"🚀 HyperFlow Protocol running on port {PORT}")
            print("🌐 External access should work via Replit URL")
            server.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")
        time.sleep(5)
        start_server()  # Restart on error

if __name__ == "__main__":
    start_server()