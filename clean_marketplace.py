#!/usr/bin/env python3
import http.server
import socketserver
import json
import random
import hashlib
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

class CleanMarketplaceHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        try:
            if path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow NFT Marketplace</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            color: white;
            min-height: 100vh;
        }
        .header {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(45, 212, 191, 0.1);
            padding: 16px 0;
        }
        .header-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .logo {
            font-size: 24px;
            font-weight: 700;
            color: #2dd4bf;
        }
        .nav-links {
            display: flex;
            list-style: none;
            gap: 32px;
        }
        .nav-link {
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
        }
        .nav-link.active, .nav-link:hover {
            color: #2dd4bf;
            background: rgba(45, 212, 191, 0.1);
        }
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 60px 20px;
        }
        .hero {
            text-align: center;
            margin-bottom: 80px;
        }
        .hero h1 {
            font-size: 64px;
            font-weight: 800;
            margin-bottom: 24px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero p {
            font-size: 20px;
            color: #94a3b8;
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .btn-primary {
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            border: none;
            border-radius: 12px;
            padding: 16px 32px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(45, 212, 191, 0.3);
        }
        .collections-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 24px;
            margin-top: 40px;
        }
        .collection-card {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(45, 212, 191, 0.1);
            border-radius: 20px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .collection-card:hover {
            transform: translateY(-4px);
            border-color: rgba(45, 212, 191, 0.3);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        .collection-banner {
            height: 120px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            position: relative;
        }
        .collection-avatar {
            position: absolute;
            bottom: -30px;
            left: 24px;
            width: 80px;
            height: 80px;
            border-radius: 20px;
            border: 4px solid rgba(15, 23, 42, 0.9);
            background: linear-gradient(135deg, #2dd4bf, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 700;
        }
        .collection-info {
            padding: 40px 24px 24px;
        }
        .collection-name {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 16px;
        }
        .collection-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }
        .stat-box {
            background: rgba(15, 23, 42, 0.6);
            border-radius: 12px;
            padding: 12px;
            text-align: center;
        }
        .stat-value {
            font-size: 16px;
            font-weight: 700;
            color: #2dd4bf;
            display: block;
        }
        .stat-label {
            font-size: 12px;
            color: #64748b;
            margin-top: 2px;
        }
        @media (max-width: 768px) {
            .hero h1 { font-size: 48px; }
            .nav-links { display: none; }
            .collections-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-container">
            <div class="logo">🎨 HyperFlow NFT</div>
            <nav>
                <ul class="nav-links">
                    <li><a href="#" class="nav-link active">Marketplace</a></li>
                    <li><a href="#" class="nav-link">Collections</a></li>
                    <li><a href="#" class="nav-link">Activity</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="main-content">
        <section class="hero">
            <h1>Discover Extraordinary NFTs</h1>
            <p>The premier NFT marketplace on HyperEVM blockchain. Explore unique digital collectibles from verified collections.</p>
            <button class="btn-primary">Explore Collections</button>
        </section>

        <div class="collections-grid">
            <div class="collection-card">
                <div class="collection-banner">
                    <div class="collection-avatar">W</div>
                </div>
                <div class="collection-info">
                    <div class="collection-name">Wealthy Hypio Babies</div>
                    <div class="collection-stats">
                        <div class="stat-box">
                            <span class="stat-value">58.2 HYPE</span>
                            <span class="stat-label">Floor Price</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-value">5,555</span>
                            <span class="stat-label">Items</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-value">2.8K</span>
                            <span class="stat-label">24h Volume</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-value">2,770</span>
                            <span class="stat-label">Owners</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="collection-card">
                <div class="collection-banner">
                    <div class="collection-avatar">P</div>
                </div>
                <div class="collection-info">
                    <div class="collection-name">PiP & Friends</div>
                    <div class="collection-stats">
                        <div class="stat-box">
                            <span class="stat-value">25.7 HYPE</span>
                            <span class="stat-label">Floor Price</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-value">7,777</span>
                            <span class="stat-label">Items</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-value">1.2K</span>
                            <span class="stat-label">24h Volume</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-value">3,421</span>
                            <span class="stat-label">Owners</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        console.log('✅ HyperFlow NFT Marketplace Loaded Successfully');
        console.log('🌐 Running on Port 5000');
        console.log('💎 HyperEVM Integration Active');
    </script>
</body>
</html>'''
                self.wfile.write(html.encode())
                
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            print(f"❌ Error: {e}")
            self.send_response(500)
            self.end_headers()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    PORT = 5000
    print("🚀 HyperFlow NFT Marketplace - Clean Build")
    print("🎨 Magic Eden Style Interface")
    print("💎 HyperEVM Blockchain Integration")
    print(f"✅ Running on http://localhost:{PORT}")
    print(f"🌐 External: https://{PORT}-workspace-hypurrs75.replit.dev")
    
    with ReusableTCPServer(("0.0.0.0", PORT), CleanMarketplaceHandler) as httpd:
        httpd.serve_forever()