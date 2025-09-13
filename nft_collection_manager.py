#!/usr/bin/env python3

import http.server
import socketserver
import os
import json
import time
from urllib.parse import urlparse, parse_qs

PORT = 5002

class NFTCollectionManager(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_homepage()
        elif self.path.startswith('/mint/'):
            # Individual collection mint page
            collection_slug = self.path.split('/mint/')[1]
            self.send_mint_page(collection_slug)
        elif self.path.startswith('/admin/'):
            # Admin management for collections
            collection_slug = self.path.split('/admin/')[1]
            self.send_admin_page(collection_slug)
        elif self.path.startswith('/api/collections'):
            self.send_collections_api()
        else:
            super().do_GET()

    def send_homepage(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow Collection Manager</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        
        .hero {
            text-align: center;
            padding: 60px 0;
            background: rgba(30, 41, 59, 0.3);
        }
        
        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            padding: 60px 0;
        }
        
        .feature-card {
            background: rgba(30, 41, 59, 0.4);
            padding: 30px;
            border-radius: 16px;
            border: 1px solid rgba(45, 212, 191, 0.2);
        }
        
        .feature-card h3 {
            color: #2dd4bf;
            margin-bottom: 15px;
            font-size: 20px;
        }
        
        .feature-card p {
            color: #94a3b8;
            line-height: 1.6;
        }
        
        .btn {
            display: inline-block;
            padding: 16px 32px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            transition: transform 0.2s;
            border: none;
            cursor: pointer;
        }
        
        .btn:hover { transform: translateY(-2px); }
        
        .collection-list {
            background: rgba(30, 41, 59, 0.3);
            border-radius: 16px;
            padding: 30px;
            margin: 30px 0;
        }
        
        .collection-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 12px;
            margin-bottom: 15px;
            border: 1px solid rgba(45, 212, 191, 0.1);
        }
        
        .collection-status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .status-active { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
        .status-soldout { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
        .status-upcoming { background: rgba(251, 191, 36, 0.2); color: #fbbf24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>🚀 NFT Collection Manager</h1>
            <p style="font-size: 18px; color: #94a3b8; margin-bottom: 30px;">Manage all your NFT collections with advanced features</p>
            <button class="btn" onclick="window.open('http://localhost:5000', '_blank')">+ Create New Collection</button>
        </div>

        <div class="features">
            <div class="feature-card">
                <h3>📦 Individual Collection Pages</h3>
                <p>Each collection gets its own unique mint page with custom branding and dedicated URL.</p>
            </div>
            
            <div class="feature-card">
                <h3>⏰ Phase Extension Management</h3>
                <p>Extend mint times, modify phases, and update pricing even after launch.</p>
            </div>
            
            <div class="feature-card">
                <h3>🎨 Unrevealed Mint Support</h3>
                <p>Start with placeholder metadata and reveal artwork later with IPFS updates.</p>
            </div>
            
            <div class="feature-card">
                <h3>🛍️ Auto-Marketplace Integration</h3>
                <p>Sold-out collections automatically list on marketplace for secondary trading.</p>
            </div>
        </div>

        <div class="collection-list">
            <h2 style="color: #2dd4bf; margin-bottom: 25px;">Active Collections</h2>
            
            <div class="collection-item">
                <div>
                    <h4 style="color: white; margin-bottom: 5px;">HyperFlow Genesis</h4>
                    <p style="color: #94a3b8; font-size: 14px;">4,250 / 10,000 minted • $80 HYPE</p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span class="collection-status status-active">ACTIVE</span>
                    <button class="btn" style="padding: 8px 16px; font-size: 14px;" onclick="openMintPage('hyperflow-genesis')">View Mint</button>
                    <button class="btn" style="padding: 8px 16px; font-size: 14px; background: rgba(75, 85, 99, 0.8);" onclick="openAdminPage('hyperflow-genesis')">Manage</button>
                </div>
            </div>
            
            <div class="collection-item">
                <div>
                    <h4 style="color: white; margin-bottom: 5px;">Cyber Punks Elite</h4>
                    <p style="color: #94a3b8; font-size: 14px;">5,000 / 5,000 minted • Sold Out</p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span class="collection-status status-soldout">SOLD OUT</span>
                    <button class="btn" style="padding: 8px 16px; font-size: 14px;" onclick="openMarketplace('cyber-punks')">View Marketplace</button>
                    <button class="btn" style="padding: 8px 16px; font-size: 14px; background: rgba(75, 85, 99, 0.8);" onclick="openAdminPage('cyber-punks')">Manage</button>
                </div>
            </div>
            
            <div class="collection-item">
                <div>
                    <h4 style="color: white; margin-bottom: 5px;">Digital Warriors</h4>
                    <p style="color: #94a3b8; font-size: 14px;">Mint starts in 2 days • $120 HYPE</p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span class="collection-status status-upcoming">UPCOMING</span>
                    <button class="btn" style="padding: 8px 16px; font-size: 14px; background: rgba(75, 85, 99, 0.8);" onclick="openAdminPage('digital-warriors')">Manage</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        function openMintPage(slug) {
            window.open(`/mint/${slug}`, '_blank');
        }
        
        function openAdminPage(slug) {
            window.open(`/admin/${slug}`, '_blank');
        }
        
        function openMarketplace(slug) {
            window.open(`http://localhost:5000/#collection-${slug}`, '_blank');
        }
        
        console.log('✅ Collection Manager Ready');
    </script>
</body>
</html>
        """
        
        self.wfile.write(html.encode())

    def send_mint_page(self, collection_slug):
        """Individual collection mint page with unique URL"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Mock collection data (in real app, load from database)
        collections = {
            'hyperflow-genesis': {
                'name': 'HyperFlow Genesis',
                'symbol': 'HFGEN',
                'price': 80,
                'minted': 4250,
                'total': 10000,
                'status': 'active',
                'banner': '/attached_assets/hyperflow-banner.png',
                'logo': '/attached_assets/hyperflow-logo.png'
            }
        }
        
        collection = collections.get(collection_slug, {
            'name': 'Unknown Collection',
            'symbol': 'UNK',
            'price': 0,
            'minted': 0,
            'total': 0,
            'status': 'unknown'
        })
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{collection['name']} - Official Mint</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
        }}
        
        .mint-container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 40px 20px;
            text-align: center;
        }}
        
        .collection-header {{
            margin-bottom: 40px;
        }}
        
        .collection-logo {{
            width: 120px;
            height: 120px;
            border-radius: 20px;
            margin: 0 auto 20px auto;
            background: rgba(45, 212, 191, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
        }}
        
        .mint-card {{
            background: rgba(30, 41, 59, 0.4);
            border-radius: 20px;
            padding: 40px;
            border: 1px solid rgba(45, 212, 191, 0.2);
        }}
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: rgba(15, 23, 42, 0.6);
            border-radius: 10px;
            overflow: hidden;
            margin: 20px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            width: {(collection['minted'] / collection['total']) * 100 if collection['total'] > 0 else 0}%;
            transition: width 0.3s ease;
        }}
        
        .mint-controls {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
        }}
        
        .quantity-btn {{
            width: 40px;
            height: 40px;
            border-radius: 8px;
            border: 2px solid rgba(45, 212, 191, 0.3);
            background: rgba(15, 23, 42, 0.6);
            color: white;
            font-size: 18px;
            cursor: pointer;
        }}
        
        .quantity-input {{
            width: 80px;
            height: 40px;
            text-align: center;
            background: rgba(15, 23, 42, 0.6);
            border: 2px solid rgba(45, 212, 191, 0.3);
            border-radius: 8px;
            color: white;
            font-size: 18px;
        }}
        
        .mint-btn {{
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            border: none;
            border-radius: 12px;
            color: white;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        .mint-btn:hover {{ transform: translateY(-2px); }}
        
        .mint-btn:disabled {{
            background: rgba(75, 85, 99, 0.5);
            cursor: not-allowed;
            transform: none;
        }}
    </style>
</head>
<body>
    <div class="mint-container">
        <div class="collection-header">
            <div class="collection-logo">🚀</div>
            <h1 style="font-size: 36px; margin-bottom: 10px;">{collection['name']}</h1>
            <p style="color: #94a3b8; font-size: 18px;">Official Mint Page</p>
        </div>
        
        <div class="mint-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                <div>
                    <div style="color: #94a3b8; font-size: 14px;">Price</div>
                    <div style="color: white; font-size: 24px; font-weight: 600;">{collection['price']} HYPE</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 14px;">Minted</div>
                    <div style="color: white; font-size: 24px; font-weight: 600;">{collection['minted']:,} / {collection['total']:,}</div>
                </div>
            </div>
            
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
            
            <div style="color: #94a3b8; font-size: 14px; margin-bottom: 30px;">
                {((collection['total'] - collection['minted']) / collection['total'] * 100):.1f}% remaining
            </div>
            
            <div class="mint-controls">
                <button class="quantity-btn" onclick="changeQuantity(-1)">-</button>
                <input type="number" class="quantity-input" value="1" min="1" max="10" id="mint-quantity">
                <button class="quantity-btn" onclick="changeQuantity(1)">+</button>
            </div>
            
            <div style="margin-bottom: 20px;">
                <div style="color: #94a3b8; font-size: 14px;">Total Cost</div>
                <div style="color: white; font-size: 28px; font-weight: 600;" id="total-cost">{collection['price']} HYPE</div>
            </div>
            
            <button class="mint-btn" onclick="mintNFT()">🚀 Mint NFT</button>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(45, 212, 191, 0.1);">
                <p style="color: #94a3b8; font-size: 14px;">
                    🔗 Collection Contract: 0x{collection_slug[:8]}...{collection_slug[-8:]}
                </p>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 8px;">
                    🌐 Network: HyperEVM (Chain ID: 999)
                </p>
            </div>
        </div>
    </div>

    <script>
        const price = {collection['price']};
        
        function changeQuantity(change) {{
            const input = document.getElementById('mint-quantity');
            let newValue = parseInt(input.value) + change;
            newValue = Math.max(1, Math.min(10, newValue));
            input.value = newValue;
            updateTotalCost();
        }}
        
        function updateTotalCost() {{
            const quantity = parseInt(document.getElementById('mint-quantity').value);
            const total = quantity * price;
            document.getElementById('total-cost').textContent = total + ' HYPE';
        }}
        
        function mintNFT() {{
            const quantity = parseInt(document.getElementById('mint-quantity').value);
            alert(`Minting ${{quantity}} NFT(s) for ${{quantity * price}} HYPE tokens!\\n\\nTransaction will be processed on HyperEVM network.`);
        }}
        
        document.getElementById('mint-quantity').addEventListener('input', updateTotalCost);
        
        console.log('✅ {collection["name"]} Mint Page Ready');
    </script>
</body>
</html>
        """
        
        self.wfile.write(html.encode())

    def send_admin_page(self, collection_slug):
        """Admin management page for collections"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin - {collection_slug}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .admin-container {{ max-width: 1000px; margin: 0 auto; }}
        
        .admin-card {{
            background: rgba(30, 41, 59, 0.4);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(45, 212, 191, 0.2);
        }}
        
        .admin-card h2 {{
            color: #2dd4bf;
            margin-bottom: 20px;
            font-size: 24px;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            color: white;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        
        .form-group input, .form-group textarea {{
            width: 100%;
            padding: 12px;
            background: rgba(15, 23, 42, 0.6);
            border: 2px solid rgba(45, 212, 191, 0.2);
            border-radius: 8px;
            color: white;
            font-size: 16px;
        }}
        
        .btn {{
            padding: 12px 24px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            margin-right: 10px;
            margin-bottom: 10px;
        }}
        
        .btn-danger {{
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }}
        
        .btn-secondary {{
            background: rgba(75, 85, 99, 0.8);
        }}
        
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .status-indicator {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 15px;
        }}
        
        .status-active {{ background: rgba(34, 197, 94, 0.2); color: #22c55e; }}
    </style>
</head>
<body>
    <div class="admin-container">
        <h1 style="font-size: 36px; margin-bottom: 10px; color: white;">🛠️ Collection Admin</h1>
        <p style="color: #94a3b8; margin-bottom: 30px;">Managing: {collection_slug}</p>
        <span class="status-indicator status-active">ACTIVE MINT</span>
        
        <!-- Phase Management -->
        <div class="admin-card">
            <h2>⏰ Phase Management</h2>
            <p style="color: #94a3b8; margin-bottom: 25px;">Extend or modify mint phases even after launch</p>
            
            <div class="form-group">
                <label>Current Phase: Whitelist Mint</label>
                <div class="grid-2">
                    <div>
                        <label>End Time</label>
                        <input type="datetime-local" value="2025-08-25T23:59">
                    </div>
                    <div>
                        <label>Price (HYPE)</label>
                        <input type="number" value="50" step="0.1">
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <button class="btn" onclick="extendPhase()">📅 Extend Phase by 24h</button>
                <button class="btn" onclick="updatePrice()">💰 Update Price</button>
                <button class="btn btn-secondary" onclick="addNewPhase()">➕ Add New Phase</button>
            </div>
            
            <div style="background: rgba(251, 191, 36, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #fbbf24;">
                <div style="color: #fbbf24; font-size: 14px; font-weight: 600;">⚠️ Phase Extension Notice</div>
                <div style="color: #94a3b8; font-size: 14px; margin-top: 5px;">
                    Changes will take effect immediately. Notify your community about any phase extensions.
                </div>
            </div>
        </div>
        
        <!-- IPFS Management -->
        <div class="admin-card">
            <h2>🎨 IPFS & Reveal Management</h2>
            <p style="color: #94a3b8; margin-bottom: 25px;">Update metadata URI for artwork reveal</p>
            
            <div class="form-group">
                <label>Current Base URI (Unrevealed)</label>
                <input type="text" value="ipfs://QmPlaceholder123/" id="current-uri">
                <div style="color: #94a3b8; font-size: 12px; margin-top: 5px;">
                    Currently showing placeholder images to minters
                </div>
            </div>
            
            <div class="form-group">
                <label>New Base URI (For Reveal)</label>
                <input type="text" placeholder="ipfs://QmNewRealArt456/" id="new-uri">
                <div style="color: #94a3b8; font-size: 12px; margin-top: 5px;">
                    Enter the IPFS URI with your final artwork metadata
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <button class="btn" onclick="revealArtwork()">🎭 Reveal Artwork</button>
                <button class="btn btn-secondary" onclick="previewMetadata()">👁️ Preview Metadata</button>
            </div>
            
            <div style="background: rgba(45, 212, 191, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #2dd4bf;">
                <div style="color: #2dd4bf; font-size: 14px; font-weight: 600;">💡 Reveal Strategy</div>
                <div style="color: #94a3b8; font-size: 14px; margin-top: 5px;">
                    Most projects reveal artwork 24-48 hours after mint completion to build excitement.
                </div>
            </div>
        </div>
        
        <!-- Collection Status -->
        <div class="admin-card">
            <h2>📊 Collection Status & Actions</h2>
            
            <div class="grid-2" style="margin-bottom: 25px;">
                <div>
                    <div style="color: #94a3b8; font-size: 14px;">Total Minted</div>
                    <div style="color: white; font-size: 24px; font-weight: 600;">4,250 / 10,000</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 14px;">Revenue Generated</div>
                    <div style="color: white; font-size: 24px; font-weight: 600;">340,000 HYPE</div>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button class="btn" onclick="pauseMint()">⏸️ Pause Mint</button>
                <button class="btn" onclick="enableMarketplace()">🛍️ Enable Marketplace</button>
                <button class="btn btn-secondary" onclick="viewAnalytics()">📈 View Analytics</button>
                <button class="btn btn-danger" onclick="emergencyStop()">🛑 Emergency Stop</button>
            </div>
        </div>
    </div>

    <script>
        function extendPhase() {{
            alert('✅ Phase extended by 24 hours!\\n\\nNew end time: ' + new Date(Date.now() + 24*60*60*1000).toLocaleString());
        }}
        
        function updatePrice() {{
            alert('💰 Price updated successfully!\\n\\nChanges are live immediately.');
        }}
        
        function addNewPhase() {{
            alert('➕ New phase added!\\n\\nConfigure the new phase parameters.');
        }}
        
        function revealArtwork() {{
            const newUri = document.getElementById('new-uri').value;
            if (!newUri) {{
                alert('Please enter a new IPFS URI first.');
                return;
            }}
            alert('🎭 Artwork revealed!\\n\\nBase URI updated to: ' + newUri + '\\n\\nAll NFT metadata now shows final artwork.');
        }}
        
        function previewMetadata() {{
            alert('👁️ Opening metadata preview...\\n\\nCheck how your NFTs will look after reveal.');
        }}
        
        function pauseMint() {{
            alert('⏸️ Mint paused!\\n\\nNo new NFTs can be minted until resumed.');
        }}
        
        function enableMarketplace() {{
            alert('🛍️ Marketplace enabled!\\n\\nNFTs are now available for secondary trading.');
        }}
        
        function viewAnalytics() {{
            alert('📈 Opening analytics dashboard...');
        }}
        
        function emergencyStop() {{
            if (confirm('🛑 Are you sure you want to emergency stop?\\n\\nThis will immediately halt all minting and cannot be undone.')) {{
                alert('🛑 Emergency stop activated!\\n\\nAll collection activities have been halted.');
            }}
        }}
        
        console.log('✅ Admin Panel Ready for {collection_slug}');
    </script>
</body>
</html>
        """
        
        self.wfile.write(html.encode())

    def send_collections_api(self):
        """API endpoint for collection data"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        collections = {
            "collections": [
                {
                    "slug": "hyperflow-genesis",
                    "name": "HyperFlow Genesis",
                    "symbol": "HFGEN",
                    "price": 80,
                    "minted": 4250,
                    "total": 10000,
                    "status": "active",
                    "mintUrl": "/mint/hyperflow-genesis",
                    "adminUrl": "/admin/hyperflow-genesis"
                }
            ]
        }
        
        self.wfile.write(json.dumps(collections).encode())

if __name__ == "__main__":
    httpd = socketserver.TCPServer(("", PORT), NFTCollectionManager)
    httpd.allow_reuse_address = True
    print(f"🚀 NFT Collection Manager")
    print(f"✅ Running at http://localhost:{PORT}")
    print(f"🌐 External access: https://{PORT}-workspace-hypurrs75.replit.dev")
    print(f"✅ Collection management system ready")
    httpd.serve_forever()