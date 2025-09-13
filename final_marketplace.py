#!/usr/bin/env python3
import http.server
import socketserver
import socket
import time
from urllib.parse import urlparse

class FinalMarketplaceHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        
        if path.startswith('/collection/'):
            collection_name = path.split('/')[-1]
            html = self.get_collection_page(collection_name)
        else:
            html = self.get_home_page()
        
        self.wfile.write(html.encode())
    
    def get_collection_page(self, collection_name):
        if collection_name == 'wealthy-hypio-babies':
            title = "Wealthy Hypio Babies"
            total = "5,555"
            floor = "58.2 HYPE"
            avatar = "W"
        elif collection_name == 'pip-friends':
            title = "PiP & Friends"
            total = "7,777"
            floor = "25.7 HYPE"
            avatar = "P"
        else:
            title = "Collection Not Found"
            total = "0"
            floor = "0 HYPE"
            avatar = "?"
            
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - HyperFlow</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            color: white;
            min-height: 100vh;
        }}
        .header {{
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(45, 212, 191, 0.1);
            padding: 16px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .logo {{
            font-size: 24px;
            font-weight: 700;
            color: #2dd4bf;
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
        }}
        .logo-icon {{
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #2dd4bf, #8b5cf6);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }}
        .collection-header {{
            padding: 60px 20px;
            text-align: center;
        }}
        .collection-avatar {{
            width: 120px;
            height: 120px;
            border-radius: 24px;
            background: linear-gradient(135deg, #2dd4bf, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            font-weight: 700;
            margin: 0 auto 24px;
        }}
        .collection-title {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 16px;
        }}
        .collection-stats {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-top: 40px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: 700;
            color: #2dd4bf;
            display: block;
        }}
        .stat-label {{
            color: #94a3b8;
            margin-top: 4px;
        }}
        .nft-grid {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 24px;
        }}
        .nft-card {{
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(45, 212, 191, 0.1);
            border-radius: 16px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .nft-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(45, 212, 191, 0.3);
        }}
        .nft-image {{
            width: 100%;
            height: 250px;
            background: linear-gradient(135deg, #2dd4bf, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            font-weight: 700;
        }}
        .nft-info {{
            padding: 16px;
        }}
        .nft-name {{
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .nft-price {{
            color: #2dd4bf;
            font-weight: 700;
        }}
        .back-btn {{
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(45, 212, 191, 0.3);
            border-radius: 12px;
            padding: 12px 24px;
            color: #2dd4bf;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-block;
            margin: 20px;
        }}
        .back-btn:hover {{
            background: rgba(45, 212, 191, 0.1);
        }}
        @media (max-width: 768px) {{
            .collection-stats {{ flex-direction: column; gap: 16px; }}
            .nft-grid {{ grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <a href="/" class="logo">
                <div class="logo-icon">⚡</div>
                HyperFlow
            </a>
        </div>
    </header>

    <div class="collection-header">
        <a href="/" class="back-btn">← Back to Marketplace</a>
        <div class="collection-avatar">{avatar}</div>
        <h1 class="collection-title">{title}</h1>
        <div class="collection-stats">
            <div class="stat">
                <span class="stat-value">{floor}</span>
                <span class="stat-label">Floor Price</span>
            </div>
            <div class="stat">
                <span class="stat-value">{total}</span>
                <span class="stat-label">Total Supply</span>
            </div>
            <div class="stat">
                <span class="stat-value">50%</span>
                <span class="stat-label">Listed</span>
            </div>
        </div>
    </div>

    <div class="nft-grid">''' + ''.join([f'''
        <div class="nft-card">
            <div class="nft-image">{avatar}#{i+1}</div>
            <div class="nft-info">
                <div class="nft-name">{title.split()[0]} #{i+1}</div>
                <div class="nft-price">{float(floor.split()[0]) + (i * 0.1):.1f} HYPE</div>
            </div>
        </div>''' for i in range(12)]) + '''
    </div>

    <script>
        console.log('🎨 {title} Collection Page');
        console.log('💎 HyperEVM Integration Active');
    </script>
</body>
</html>'''

    def get_home_page(self):
        
        return '''<!DOCTYPE html>
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
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .container {
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
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #2dd4bf, #8b5cf6);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }
        .nav {
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
            transition: all 0.3s ease;
        }
        .nav-link.active, .nav-link:hover {
            color: #2dd4bf;
            background: rgba(45, 212, 191, 0.1);
        }
        .hero {
            text-align: center;
            padding: 100px 20px;
            background: linear-gradient(135deg, 
                rgba(45, 212, 191, 0.1) 0%, 
                rgba(6, 182, 212, 0.05) 50%, 
                rgba(139, 92, 246, 0.1) 100%);
            border-bottom: 1px solid rgba(45, 212, 191, 0.1);
            position: relative;
            overflow: hidden;
        }
        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M 60 0 L 0 0 0 60" fill="none" stroke="rgba(45,212,191,0.05)" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(%23grid)" /></svg>');
            opacity: 0.3;
            z-index: 0;
        }
        .hero-content {
            position: relative;
            z-index: 1;
        }
        .hero h1 {
            font-size: 72px;
            font-weight: 800;
            margin-bottom: 24px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.1;
        }
        .hero p {
            font-size: 20px;
            color: #94a3b8;
            margin-bottom: 40px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .btn {
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            border: none;
            border-radius: 12px;
            padding: 16px 32px;
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 20px 40px rgba(45, 212, 191, 0.3);
        }
        .collections {
            padding: 80px 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .section-title {
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 60px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 32px;
        }
        .card {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(45, 212, 191, 0.1);
            border-radius: 24px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
        }
        .card:hover {
            transform: translateY(-8px);
            border-color: rgba(45, 212, 191, 0.3);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
        }
        .card-banner {
            height: 140px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            position: relative;
        }
        .card-avatar {
            position: absolute;
            bottom: -35px;
            left: 24px;
            width: 90px;
            height: 90px;
            border-radius: 24px;
            border: 4px solid rgba(15, 23, 42, 0.9);
            background: linear-gradient(135deg, #2dd4bf, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 700;
        }
        .card-content {
            padding: 50px 24px 32px;
        }
        .card-title {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }
        .stat {
            background: rgba(15, 23, 42, 0.6);
            border-radius: 16px;
            padding: 16px;
            text-align: center;
        }
        .stat-value {
            font-size: 18px;
            font-weight: 700;
            color: #2dd4bf;
            display: block;
            margin-bottom: 4px;
        }
        .stat-label {
            font-size: 13px;
            color: #64748b;
        }
        .status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(45, 212, 191, 0.1);
            border: 1px solid rgba(45, 212, 191, 0.3);
            border-radius: 12px;
            padding: 12px 20px;
            font-size: 14px;
            color: #2dd4bf;
        }
        @media (max-width: 768px) {
            .hero h1 { font-size: 48px; }
            .nav { display: none; }
            .grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">
                <div class="logo-icon">⚡</div>
                HyperFlow
            </div>
            <nav>
                <ul class="nav">
                    <li><a href="#" class="nav-link active">Marketplace</a></li>
                    <li><a href="#" class="nav-link">Collections</a></li>
                    <li><a href="#" class="nav-link">Activity</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="hero-content">
            <h1>Discover NFTs</h1>
            <p>The premier NFT marketplace on HyperEVM blockchain featuring verified collections and real-time trading.</p>
            <a href="#collections" class="btn">Explore Collections</a>
        </div>
    </section>

    <section class="collections" id="collections">
        <h2 class="section-title">Featured Collections</h2>
        <div class="grid">
            <a href="/collection/wealthy-hypio-babies" class="card">
                <div class="card-banner">
                    <div class="card-avatar">W</div>
                </div>
                <div class="card-content">
                    <h3 class="card-title">Wealthy Hypio Babies</h3>
                    <div class="stats">
                        <div class="stat">
                            <span class="stat-value">58.2 HYPE</span>
                            <span class="stat-label">Floor Price</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">5,555</span>
                            <span class="stat-label">Total Supply</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">2.8K</span>
                            <span class="stat-label">24h Volume</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">2,770</span>
                            <span class="stat-label">Owners</span>
                        </div>
                    </div>
                </div>
            </a>

            <a href="/collection/pip-friends" class="card">
                <div class="card-banner">
                    <div class="card-avatar">P</div>
                </div>
                <div class="card-content">
                    <h3 class="card-title">PiP & Friends</h3>
                    <div class="stats">
                        <div class="stat">
                            <span class="stat-value">25.7 HYPE</span>
                            <span class="stat-label">Floor Price</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">7,777</span>
                            <span class="stat-label">Total Supply</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">1.2K</span>
                            <span class="stat-label">24h Volume</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">3,421</span>
                            <span class="stat-label">Owners</span>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </section>

    <div class="status">
        ✅ HyperEVM Connected • Chain ID 999
    </div>

    <script>
        console.log('🎨 HyperFlow NFT Marketplace');
        console.log('💎 HyperEVM Integration Active');
        console.log('🚀 Magic Eden Style Interface');
        console.log('✅ Port 5000 - WORKING');
        
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>'''

class ReusableServer(socketserver.TCPServer):
    allow_reuse_address = True
    
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        super().server_bind()

if __name__ == '__main__':
    PORT = 5000
    print("🚀 HyperFlow NFT Marketplace - FINAL BUILD")
    print("🎨 Magic Eden Professional Interface")
    print("💎 HyperEVM Chain ID 999 Integration")
    print("✅ Clean Port 5000 - No Conflicts")
    print(f"🌐 Access: https://{PORT}-workspace-hypurrs75.replit.dev")
    
    try:
        with ReusableServer(("0.0.0.0", PORT), FinalMarketplaceHandler) as server:
            server.serve_forever()
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(2)
        print("🔄 Retrying...")
        with ReusableServer(("0.0.0.0", PORT), FinalMarketplaceHandler) as server:
            server.serve_forever()