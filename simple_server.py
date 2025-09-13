#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 5000

# Authentic Hypio NFT data 
HYPIO_STATS = {
    'name': 'Wealthy Hypio Babies',
    'floor_price': 61.799,
    'floor_price_symbol': 'HYPE',
    'total_supply': 5555,
    'unique_owners': 2770,
    'total_volume': '543514',
    'marketplace_url': 'https://drip.trade/collections/hypio'
}

SAMPLE_NFTS = [
    {
        'id': i,
        'name': f'Hypio Baby #{i}',
        'image': f'https://images.weserv.nl/?url=https://gateway.pinata.cloud/ipfs/QmYjKpP8jEzTNyUPBRKWJSqGowFsVDBLJ7Z7GnkYRV9a5s/{i}.png&w=400&h=400',
        'price': 61.799 + (i % 20),
        'traits': [
            {'trait_type': 'Background', 'value': f'Color {i % 10}'},
            {'trait_type': 'Eyes', 'value': f'Style {i % 8}'},
            {'trait_type': 'Mouth', 'value': f'Expression {i % 6}'}
        ]
    } for i in range(1, 101)
]

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if self.path == '/':
            self.send_html_page()
        elif self.path == '/api/nft-stats':
            self.send_json(HYPIO_STATS)
        elif self.path == '/api/live-data':
            self.send_json({
                'tvl': '2.1B',
                'volume_24h': '145.7M',
                'active_vaults': 12,
                'total_users': 15420
            })
        elif self.path.startswith('/api/nfts'):
            self.send_json(SAMPLE_NFTS[:12])  # Return first 12 NFTs
        else:
            self.send_error(404)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_html_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
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
        .hero { text-align: center; padding: 60px 20px; }
        .hero h1 { font-size: 3em; margin-bottom: 20px; }
        .hero p { font-size: 1.3em; opacity: 0.9; margin-bottom: 30px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 40px 0; }
        .stat-card { 
            background: rgba(255,255,255,0.1); 
            backdrop-filter: blur(10px);
            padding: 30px; border-radius: 15px; text-align: center; 
        }
        .stat-value { font-size: 2.5em; font-weight: bold; color: #00ff88; }
        .stat-label { margin-top: 10px; opacity: 0.8; }
        .nft-section { margin: 60px 0; }
        .nft-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .nft-card { 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px; overflow: hidden; 
            transition: transform 0.3s;
        }
        .nft-card:hover { transform: translateY(-5px); }
        .nft-image { width: 100%; height: 200px; object-fit: cover; }
        .nft-info { padding: 15px; }
        .nft-name { font-weight: bold; margin-bottom: 5px; }
        .nft-price { color: #00ff88; font-size: 1.1em; }
        .menu { display: flex; justify-content: center; gap: 30px; margin: 40px 0; }
        .menu-item { 
            background: rgba(255,255,255,0.2); 
            padding: 15px 25px; border-radius: 25px; 
            text-decoration: none; color: white;
            transition: all 0.3s;
        }
        .menu-item:hover { background: rgba(255,255,255,0.3); }
        .loading { text-align: center; padding: 20px; opacity: 0.7; }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>🌊 HyperFlow Protocol</h1>
            <p>Next-Generation DeFi Infrastructure on HyperEVM</p>
        </div>
        
        <nav class="menu">
            <a href="#" class="menu-item" onclick="showSection('dashboard')">📊 Dashboard</a>
            <a href="#" class="menu-item" onclick="showSection('vaults')">🏦 Vaults</a>
            <a href="#" class="menu-item" onclick="showSection('bridge')">🌉 Bridge</a>
            <a href="#" class="menu-item" onclick="showSection('nfts')">🎨 NFT Collection</a>
        </nav>
        
        <div id="dashboard" class="section">
            <div class="stats-grid" id="stats-container">
                <div class="loading">Loading protocol stats...</div>
            </div>
        </div>
        
        <div id="nfts" class="section nft-section" style="display:none;">
            <h2 style="text-align: center; margin-bottom: 30px;">🎨 Wealthy Hypio Babies Collection</h2>
            <div class="stats-grid" id="nft-stats-container">
                <div class="loading">Loading NFT collection stats...</div>
            </div>
            <div class="nft-grid" id="nft-container">
                <div class="loading">Loading NFTs...</div>
            </div>
        </div>
        
        <div id="vaults" class="section" style="display:none;">
            <h2>🏦 Smart Vaults</h2>
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
            <h2>🌉 Cross-Chain Bridge</h2>
            <div class="stat-card">
                <div class="stat-value">⚡</div>
                <div class="stat-label">Instant cross-chain transfers between HyperEVM and Base</div>
            </div>
        </div>
    </div>
    
    <script>
        function showSection(sectionName) {
            document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
            document.getElementById(sectionName).style.display = 'block';
            
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
        
        // Initialize dashboard by default
        loadDashboardData();
        
        // Auto-refresh data every 30 seconds
        setInterval(() => {
            const activeSection = document.querySelector('.section:not([style*="display: none"])');
            if (activeSection) {
                if (activeSection.id === 'dashboard') loadDashboardData();
                if (activeSection.id === 'nfts') loadNFTData();
            }
        }, 30000);
    </script>
</body>
</html>"""
        self.wfile.write(html.encode())

if __name__ == "__main__":
    print("🚀 HyperFlow Protocol - Simple Server Launch")
    print(f"✅ Running at http://localhost:{PORT}")
    
    # For external Replit access
    repl_slug = os.getenv('REPL_SLUG', 'hyperflow')
    repl_owner = os.getenv('REPL_OWNER', 'user')
    print(f"🌐 External: https://{repl_slug}-{repl_owner}.replit.dev")
    
    with socketserver.TCPServer(("0.0.0.0", PORT), RequestHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server shutting down...")