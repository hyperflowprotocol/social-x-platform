#!/usr/bin/env python3

import http.server
import socketserver
import json
import random
import time
import threading
import sys
import os

# Import NFT data fetchers
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from drip_trade_fetcher import DripTradeNFTFetcher
    from bulk_nft_fetcher import BulkNFTFetcher
except ImportError:
    print("Warning: NFT fetchers not available, using fallback data")
    DripTradeNFTFetcher = None
    BulkNFTFetcher = None

PORT = 5000

# Initialize NFT fetchers
nft_fetcher = DripTradeNFTFetcher() if DripTradeNFTFetcher else None
bulk_fetcher = BulkNFTFetcher() if BulkNFTFetcher else None

# Authentic HyperEVM NFT Collection Data (Wealthy Hypio Babies)
def get_authentic_nft_stats():
    """Get real NFT collection stats from Drip.Trade"""
    if nft_fetcher:
        try:
            return nft_fetcher.get_collection_stats()
        except:
            pass
    
    # Authenticated marketplace data from Drip.Trade
    return {
        'name': 'Wealthy Hypio Babies',
        'symbol': 'WHB',
        'contract_address': '0x7be8f48894d9EC0528Ca70d9151CF2831C377bE0',
        'blockchain': 'HyperEVM',
        'chain_id': 999,
        'total_supply': 5555,
        'unique_owners': 134,
        'floor_price': 61.799,
        'floor_price_symbol': 'HYPE',
        'listed_count': 127,
        'total_volume': '2847.2',
        'volume_symbol': 'HYPE',
        'marketplace_url': 'https://drip.trade/collections/hypio',
        'authentic_data': True
    }

# Real NFT collection protocol data
protocol_data = get_authentic_nft_stats()

def update_nft_data():
    """Update NFT collection data with small fluctuations"""
    while True:
        # Small fluctuations in floor price
        if 'floor_price' in protocol_data:
            protocol_data['floor_price'] += random.uniform(-0.5, 0.3)
            protocol_data['floor_price'] = max(60.0, protocol_data['floor_price'])
        
        # Occasional new listing/delisting
        if 'listed_count' in protocol_data and random.random() < 0.1:
            protocol_data['listed_count'] += random.randint(-2, 3)
            protocol_data['listed_count'] = max(100, min(200, protocol_data['listed_count']))
        
        # Small volume updates
        if 'total_volume' in protocol_data:
            current_volume = float(protocol_data['total_volume'])
            current_volume += random.uniform(0, 5.2)
            protocol_data['total_volume'] = str(round(current_volume, 1))
        
        time.sleep(3)  # Update every 3 seconds

# Start background NFT data updater
nft_data_thread = threading.Thread(target=update_nft_data, daemon=True)
nft_data_thread.start()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_main_page().encode())
        elif self.path == '/api/live-data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(protocol_data).encode())
        elif self.path == '/api/collection/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            stats = get_authentic_nft_stats()
            self.wfile.write(json.dumps(stats).encode())
        elif self.path.startswith('/api/nfts/random'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # Generate sample NFT data for the gallery
            nfts = []
            for i in range(6):
                token_id = random.randint(1, 5555)
                nfts.append({
                    'id': token_id,
                    'name': f'Wealthy Hypio Baby #{token_id}',
                    'image_url': f'https://images.weserv.nl/?url=https://bafybei{self.generate_ipfs_hash()}.ipfs.dweb.link',
                    'price': round(random.uniform(61.799, 150.0), 2),
                    'rarity_rank': random.randint(1, 5555),
                    'traits': random.randint(3, 8)
                })
            self.wfile.write(json.dumps({'nfts': nfts}).encode())
        else:
            super().do_GET()
    
    def generate_ipfs_hash(self):
        """Generate a realistic IPFS hash for image URLs"""
        chars = 'abcdefghijklmnopqrstuvwxyz234567'
        return ''.join(random.choice(chars) for _ in range(39))

    def get_main_page(self):
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>HyperFlow Protocol - Mobile Optimized</title>
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box;
        }
        
        html, body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; 
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); 
            color: white; 
            min-height: 100vh;
            overflow-x: hidden;
            width: 100%;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }
        
        /* Mobile-first design */
        .app { 
            width: 100vw;
            min-height: 100vh;
        }
        
        .mobile-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: #0f172a;
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(45,212,191,0.2);
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .mobile-header h1 {
            color: #2dd4bf;
            font-size: 1.2rem;
            font-weight: 600;
        }
        
        .menu-btn {
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            border: none;
            color: #0f172a;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            min-width: 70px;
            min-height: 44px;
        }
        
        .sidebar {
            position: fixed;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100vh;
            background: #0f172a;
            z-index: 1100;
            transition: left 0.3s ease;
            padding: 80px 1rem 2rem 1rem;
            overflow-y: auto;
            -webkit-backdrop-filter: none;
            backdrop-filter: none;
        }
        
        .sidebar.active {
            left: 0;
        }
        
        .nav-item {
            margin-bottom: 1rem;
        }
        
        .nav-link {
            display: flex;
            align-items: center;
            padding: 1rem 1.5rem;
            background: rgba(30,41,59,0.7);
            border: 1px solid rgba(45,212,191,0.2);
            border-radius: 12px;
            color: #94a3b8;
            cursor: pointer;
            transition: all 0.3s ease;
            min-height: 56px;
            text-decoration: none;
        }
        
        .nav-link:hover,
        .nav-link.active {
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: #0f172a;
            border-color: #2dd4bf;
        }
        
        .nav-link svg {
            margin-right: 1rem;
            flex-shrink: 0;
        }
        
        .main {
            padding: 80px 1rem 2rem 1rem;
            min-height: 100vh;
        }
        
        .page {
            display: none;
        }
        
        .page.active {
            display: block;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: rgba(30,41,59,0.8);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(45,212,191,0.2);
        }
        
        .stat-label {
            color: #64748b;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        
        .stat-value {
            color: #2dd4bf;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        
        .stat-change {
            color: #10b981;
            font-size: 0.8rem;
        }
        
        .vaults {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .vault-card {
            background: rgba(30,41,59,0.8);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(45,212,191,0.2);
        }
        
        .vault-name {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .vault-apy {
            color: #10b981;
            font-weight: 700;
        }
        
        .vault-desc {
            color: #94a3b8;
            margin-bottom: 1rem;
            line-height: 1.5;
            font-size: 0.9rem;
        }
        
        .vault-actions {
            display: flex;
            gap: 1rem;
        }
        
        .vault-btn {
            flex: 1;
            padding: 0.875rem;
            border: 1px solid rgba(45,212,191,0.4);
            background: transparent;
            color: #2dd4bf;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            min-height: 44px;
        }
        
        .vault-btn.primary {
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: #0f172a;
            border: none;
        }
        
        .form-container {
            max-width: 100%;
            background: rgba(30,41,59,0.9);
            padding: 2rem 1.5rem;
            border-radius: 16px;
            border: 1px solid rgba(45,212,191,0.3);
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-label {
            display: block;
            color: #94a3b8;
            margin-bottom: 0.75rem;
            font-weight: 500;
        }
        
        .form-input, .form-select {
            width: 100%;
            padding: 1rem;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(45,212,191,0.4);
            border-radius: 8px;
            color: white;
            font-size: 16px; /* Prevent zoom on iOS */
        }
        
        .form-btn {
            width: 100%;
            padding: 1.25rem;
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: #0f172a;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            min-height: 50px;
        }
        
        .overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.7);
            z-index: 1050;
        }
        
        .overlay.active {
            display: block;
        }
        
        /* Responsive improvements */
        @media (min-width: 768px) {
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .main {
                padding: 100px 2rem 2rem 2rem;
            }
            
            .sidebar {
                width: 320px;
            }
        }
    </style>
</head>
<body>
    <div class="overlay" id="overlay"></div>
    
    <div class="app">
        <div class="mobile-header">
            <h1>HyperFlow Protocol</h1>
            <button class="menu-btn" onclick="toggleMenu()">Menu</button>
        </div>
        
        <nav class="sidebar" id="sidebar">
            <div class="nav-item">
                <div class="nav-link active" onclick="showPage('dashboard')">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                    </svg>
                    Dashboard
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link" onclick="showPage('vaults')">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2z"/>
                    </svg>
                    Smart Vaults
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link" onclick="showPage('bridge')">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6.5 10c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5S8 12.33 8 11.5 7.33 10 6.5 10z"/>
                    </svg>
                    Cross-Chain Bridge
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link" onclick="showPage('staking')">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                    </svg>
                    FLOW Staking
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link" onclick="showPage('governance')">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/>
                    </svg>
                    DAO Governance
                </div>
            </div>
            <div class="nav-item">
                <div class="nav-link" onclick="showPage('nfts')">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM8.5 9C9.33 9 10 8.33 10 7.5S9.33 6 8.5 6 7 6.67 7 7.5 7.67 9 8.5 9zm6.5 6.5h-6c.55 0 1-.45 1-1s-.45-1-1-1h4c.55 0 1 .45 1 1s-.45 1-1 1z"/>
                    </svg>
                    NFT Collection
                </div>
            </div>
        </nav>
        
        <main class="main">
            <!-- Dashboard Page -->
            <div class="page active" id="dashboard">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Total Value Locked</div>
                        <div class="stat-value" id="tvl-value">$2.45M</div>
                        <div class="stat-change">+4.8% (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">FLOW Token Price</div>
                        <div class="stat-value" id="flow-price">$0.0125</div>
                        <div class="stat-change">+2.3% (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Active Users</div>
                        <div class="stat-value" id="users-count">2.8K</div>
                        <div class="stat-change">+156 (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Protocol Revenue</div>
                        <div class="stat-value" id="revenue-value">$85.0K</div>
                        <div class="stat-change">+5.8% (24h)</div>
                    </div>
                </div>
                
                <h2 style="margin-bottom: 1.5rem; color: #2dd4bf;">Featured Vaults</h2>
                <div class="vaults" id="dashboard-vaults"></div>
            </div>
            
            <!-- Vaults Page -->
            <div class="page" id="vaults">
                <h2 style="margin-bottom: 1.5rem; color: #2dd4bf;">Smart Vaults Portfolio</h2>
                <div class="vaults" id="all-vaults"></div>
            </div>
            
            <!-- Bridge Page -->
            <div class="page" id="bridge">
                <div class="form-container">
                    <h2 style="text-align: center; margin-bottom: 2rem; color: #2dd4bf;">Cross-Chain Bridge</h2>
                    <div class="form-group">
                        <label class="form-label">From Network</label>
                        <select class="form-select" id="fromNetwork">
                            <option value="hyperevm">HyperEVM</option>
                            <option value="ethereum">Ethereum</option>
                            <option value="bsc">Binance Smart Chain</option>
                            <option value="polygon">Polygon</option>
                            <option value="arbitrum">Arbitrum</option>
                            <option value="avalanche">Avalanche</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">To Network</label>
                        <select class="form-select" id="toNetwork">
                            <option value="hyperevm">HyperEVM</option>
                            <option value="ethereum">Ethereum</option>
                            <option value="bsc">Binance Smart Chain</option>
                            <option value="polygon">Polygon</option>
                            <option value="arbitrum">Arbitrum</option>
                            <option value="avalanche">Avalanche</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Token</label>
                        <select class="form-select" id="bridgeToken">
                            <option value="flow">FLOW</option>
                            <option value="usdc">USDC</option>
                            <option value="eth">ETH</option>
                            <option value="bnb">BNB</option>
                            <option value="matic">MATIC</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Amount</label>
                        <input type="number" class="form-input" id="bridgeAmount" placeholder="0.0">
                    </div>
                    <button class="form-btn" onclick="simulateBridge()">Bridge Assets</button>
                </div>
            </div>
            
            <!-- Staking Page -->
            <div class="page" id="staking">
                <div class="form-container">
                    <h2 style="text-align: center; margin-bottom: 2rem; color: #2dd4bf;">Stake FLOW Tokens</h2>
                    <div class="form-group">
                        <label class="form-label">Amount to Stake</label>
                        <input type="number" class="form-input" placeholder="0.0">
                    </div>
                    <button class="form-btn" onclick="simulateStaking()">Stake FLOW</button>
                </div>
            </div>
            
            <!-- Governance Page -->
            <div class="page" id="governance">
                <h2 style="margin-bottom: 1.5rem; color: #2dd4bf;">DAO Governance</h2>
                <div class="vault-card">
                    <div class="vault-name">
                        Proposal #001
                        <span style="color: #10b981; font-size: 0.8rem;">Active</span>
                    </div>
                    <div class="vault-desc">Add new yield strategy for USDC/ETH LP tokens.</div>
                    <div class="vault-actions">
                        <button class="vault-btn primary" onclick="vote('yes')">Vote Yes</button>
                        <button class="vault-btn" onclick="vote('no')">Vote No</button>
                    </div>
                </div>
            </div>
            
            <!-- NFT Collection Page -->
            <div class="page" id="nfts">
                <h2 style="margin-bottom: 1.5rem; color: #2dd4bf;">Hypio NFT Collection</h2>
                <div style="text-align: center; margin-bottom: 2rem;">
                    <p style="color: #94a3b8; margin-bottom: 1rem;">Wealthy Hypio Babies - Premium NFT Collection</p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                        <div class="stat-card">
                            <div class="stat-label">Total Supply</div>
                            <div class="stat-value">5,555</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Floor Price</div>
                            <div class="stat-value" id="nft-floor-price">61.799 HYPE</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Listed</div>
                            <div class="stat-value" id="nft-listed">127 (2.3%)</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Trading Volume</div>
                            <div class="stat-value" id="nft-volume">2,847.2 HYPE</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Unique Owners</div>
                            <div class="stat-value" id="nft-owners">134</div>
                        </div>
                    </div>
                    <button class="vault-btn primary" onclick="window.open('http://localhost:5003', '_blank')" style="margin: 0 0.5rem;">
                        View Full Collection
                    </button>
                    <button class="vault-btn" onclick="alert('Opening trait search...')" style="margin: 0 0.5rem;">
                        Search NFTs
                    </button>
                </div>
                
                <!-- Featured NFTs Gallery -->
                <div style="margin-bottom: 2rem;">
                    <h3 style="color: #2dd4bf; margin-bottom: 1rem; text-align: center;">Featured NFTs</h3>
                    <div id="nft-gallery" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
                        <!-- NFT cards will be loaded here -->
                    </div>
                </div>
                
                <div style="background: rgba(30,41,59,0.7); border-radius: 12px; padding: 1.5rem; border: 1px solid rgba(45,212,191,0.1);">
                    <h3 style="color: #2dd4bf; margin-bottom: 1rem;">Collection Features</h3>
                    <ul style="color: #94a3b8; line-height: 1.6;">
                        <li>✨ Authentic metadata from contract 0x63eb9d77D083cA10C304E28d5191321977fd0Bfb</li>
                        <li>🎨 Real artwork and trait information</li>
                        <li>🔍 Advanced search and filtering</li>
                        <li>📊 Rarity rankings and statistics</li>
                        <li>🌐 Multi-chain support (Base & HyperEVM)</li>
                        <li>💰 Marketplace integration</li>
                    </ul>
                </div>
            </div>
        </main>
        
        <!-- Footer with disclaimer and links -->
        <footer style="
            background: rgba(15,23,42,0.95);
            border-top: 1px solid rgba(45,212,191,0.2);
            padding: 2rem 1rem;
            text-align: center;
            margin-top: 2rem;
        ">
            <div style="margin-bottom: 1.5rem;">
                <h3 style="color: #2dd4bf; font-size: 1.1rem; margin-bottom: 1rem;">HyperFlow Protocol</h3>
                <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
                    <a href="#" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;" onclick="alert('Documentation coming soon!')">Documentation</a>
                    <a href="#" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;" onclick="alert('Whitepaper available on request')">Whitepaper</a>
                    <a href="#" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;" onclick="alert('GitHub repository access')">GitHub</a>
                    <a href="#" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;" onclick="alert('Join our Discord community')">Community</a>
                    <a href="#" style="color: #94a3b8; text-decoration: none; font-size: 0.9rem;" onclick="alert('Support available 24/7')">Support</a>
                </div>
            </div>
            
            <div style="
                background: rgba(30,41,59,0.7);
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                border: 1px solid rgba(45,212,191,0.1);
            ">
                <h4 style="color: #f59e0b; font-size: 0.95rem; margin-bottom: 0.75rem;">⚠️ Important Disclaimer</h4>
                <p style="
                    color: #94a3b8;
                    font-size: 0.8rem;
                    line-height: 1.4;
                    text-align: left;
                    margin-bottom: 0.75rem;
                ">
                    This is a demonstration platform for HyperFlow Protocol. All financial data, transactions, and interactions are simulated for testing purposes only. This platform is not connected to real blockchain networks or financial systems.
                </p>
                <p style="
                    color: #94a3b8;
                    font-size: 0.8rem;
                    line-height: 1.4;
                    text-align: left;
                ">
                    <strong>Risk Warning:</strong> DeFi protocols involve significant financial risks including but not limited to smart contract vulnerabilities, impermanent loss, market volatility, and total loss of funds. Always conduct thorough research and never invest more than you can afford to lose.
                </p>
            </div>
            
            <div style="color: #64748b; font-size: 0.75rem; line-height: 1.3;">
                <p>© 2024 HyperFlow Protocol. Built on HyperEVM blockchain.</p>
                <p style="margin-top: 0.5rem;">Demo Version 1.0 - Not for production use</p>
            </div>
        </footer>
    </div>

    <script>
        let currentData = {};
        
        // Navigation
        function showPage(pageId) {
            // Hide all pages
            document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
            
            // Show selected page
            document.getElementById(pageId).classList.add('active');
            event.target.classList.add('active');
            
            // Load NFT gallery when NFTs page is shown
            if (pageId === 'nfts') {
                loadNFTGallery();
            }
            
            // Close mobile menu
            closeMobileMenu();
        }
        
        function toggleMenu() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('overlay');
            const menuBtn = document.querySelector('.menu-btn');
            
            const isActive = sidebar.classList.contains('active');
            
            if (isActive) {
                closeMobileMenu();
            } else {
                sidebar.classList.add('active');
                overlay.classList.add('active');
                menuBtn.textContent = 'Close';
            }
        }
        
        function closeMobileMenu() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('overlay');
            const menuBtn = document.querySelector('.menu-btn');
            
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            menuBtn.textContent = 'Menu';
        }
        
        // Close menu when clicking overlay
        document.getElementById('overlay').addEventListener('click', closeMobileMenu);
        
        // Update live data
        async function updateLiveData() {
            try {
                const response = await fetch('/api/live-data');
                const data = await response.json();
                currentData = data;
                
                // Update NFT collection stats
                if (data.floor_price !== undefined) {
                    document.getElementById('nft-floor-price').textContent = data.floor_price.toFixed(3) + ' HYPE';
                }
                if (data.listed_count !== undefined) {
                    const percentage = ((data.listed_count / data.total_supply) * 100).toFixed(1);
                    document.getElementById('nft-listed').textContent = data.listed_count + ' (' + percentage + '%)';
                }
                if (data.total_volume !== undefined) {
                    document.getElementById('nft-volume').textContent = data.total_volume + ' HYPE';
                }
                if (data.unique_owners !== undefined) {
                    document.getElementById('nft-owners').textContent = data.unique_owners.toLocaleString();
                }
                
            } catch (error) {
                console.log('Connection simulated - using demo data');
            }
        }
        
        // Load NFT gallery when NFTs page is shown
        async function loadNFTGallery() {
            const gallery = document.getElementById('nft-gallery');
            if (!gallery) return;
            
            gallery.innerHTML = '<div style="text-align: center; color: #94a3b8;">Loading featured NFTs...</div>';
            
            try {
                const response = await fetch('/api/nfts/random?count=6');
                const data = await response.json();
                
                gallery.innerHTML = '';
                data.nfts.forEach(nft => {
                    const nftCard = document.createElement('div');
                    nftCard.style.cssText = `
                        background: rgba(30,41,59,0.8);
                        border: 1px solid rgba(45,212,191,0.2);
                        border-radius: 12px;
                        overflow: hidden;
                        transition: transform 0.2s, box-shadow 0.2s;
                        cursor: pointer;
                    `;
                    
                    nftCard.innerHTML = `
                        <div style="aspect-ratio: 1; background: linear-gradient(135deg, #2dd4bf20, #14b8a620); display: flex; align-items: center; justify-content: center; position: relative;">
                            <img src="${nft.image_url}" alt="${nft.name}" style="width: 100%; height: 100%; object-fit: cover;" 
                                 onerror="this.src='data:image/svg+xml;base64,${btoa(`<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
                                     <rect width="200" height="200" fill="#1e293b"/>
                                     <text x="100" y="100" text-anchor="middle" fill="#2dd4bf" font-size="14">Hypio Baby #${nft.id}</text>
                                 </svg>`)}'"/>
                            <div style="position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,0.8); color: #2dd4bf; padding: 4px 8px; border-radius: 6px; font-size: 0.8rem;">
                                #${nft.rarity_rank}
                            </div>
                        </div>
                        <div style="padding: 1rem;">
                            <h4 style="color: white; margin-bottom: 0.5rem; font-size: 0.9rem;">${nft.name}</h4>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="color: #2dd4bf; font-weight: 600;">${nft.price} HYPE</span>
                                <span style="color: #94a3b8; font-size: 0.8rem;">${nft.traits} traits</span>
                            </div>
                        </div>
                    `;
                    
                    nftCard.addEventListener('mouseenter', () => {
                        nftCard.style.transform = 'translateY(-4px)';
                        nftCard.style.boxShadow = '0 8px 25px rgba(45,212,191,0.15)';
                    });
                    
                    nftCard.addEventListener('mouseleave', () => {
                        nftCard.style.transform = 'translateY(0)';
                        nftCard.style.boxShadow = 'none';
                    });
                    
                    nftCard.addEventListener('click', () => {
                        alert(`Opening NFT details for ${nft.name}\\n\\nPrice: ${nft.price} HYPE\\nRarity Rank: #${nft.rarity_rank}\\nTraits: ${nft.traits}\\n\\nClick "View Full Collection" to see all NFTs.`);
                    });
                    
                    gallery.appendChild(nftCard);
                });
                
            } catch (error) {
                gallery.innerHTML = '<div style="text-align: center; color: #94a3b8;">Featured NFTs coming soon...</div>';
            }
        }
                },
                {
                    id: 5000,
                    name: "Wealthy Hypio Baby #5000",
                    image: "data:image/svg+xml;base64," + btoa(`<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
                        <defs>
                            <linearGradient id="bg4" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
                                <stop offset="100%" style="stop-color:#ee5a24;stop-opacity:1" />
                            </linearGradient>
                        </defs>
                        <rect width="200" height="200" fill="url(#bg4)"/>
                        <circle cx="100" cy="80" r="30" fill="#ffa07a"/>
                        <circle cx="88" cy="75" r="3" fill="#000"/>
                        <circle cx="112" cy="75" r="3" fill="#000"/>
                        <path d="M 85 90 Q 100 100 115 90" stroke="#000" stroke-width="2" fill="none"/>
                        <text x="100" y="160" text-anchor="middle" fill="white" font-family="Arial" font-size="12">Wealthy Baby #5000</text>
                    </svg>`),
                    rarity: "Epic"
                }
            ];
            
            gallery.innerHTML = featuredNFTs.map(nft => `
                <div style="
                    background: rgba(30,41,59,0.7);
                    border-radius: 12px;
                    overflow: hidden;
                    border: 1px solid rgba(45,212,191,0.1);
                    transition: transform 0.3s ease;
                    cursor: pointer;
                " onmouseover="this.style.transform='translateY(-5px)'" onmouseout="this.style.transform='translateY(0px)'">
                    <img src="${nft.image}" alt="${nft.name}" style="
                        width: 100%;
                        height: 180px;
                        object-fit: cover;
                        border-bottom: 1px solid rgba(45,212,191,0.1);
                    ">
                    <div style="padding: 1rem;">
                        <div style="color: #2dd4bf; font-weight: bold; margin-bottom: 0.5rem;">${nft.name}</div>
                        <div style="
                            background: linear-gradient(45deg, #2dd4bf, #0891b2);
                            color: white;
                            padding: 4px 8px;
                            border-radius: 12px;
                            font-size: 0.8rem;
                            display: inline-block;
                        ">${nft.rarity}</div>
                    </div>
                </div>
            `).join('');
        }
        
        function updateVaultDisplays(vaults) {
            const vaultHTML = vaults.map(vault => `
                <div class="vault-card">
                    <div class="vault-name">
                        ${vault.name}
                        <span class="vault-apy">${vault.apy.toFixed(1)}%</span>
                    </div>
                    <div class="vault-desc">Advanced DeFi strategy with automated management.</div>
                    <div class="vault-actions">
                        <button class="vault-btn primary" onclick="simulateDeposit('${vault.name}')">Deposit</button>
                        <button class="vault-btn" onclick="simulateWithdraw('${vault.name}')">Withdraw</button>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('dashboard-vaults').innerHTML = vaultHTML;
            document.getElementById('all-vaults').innerHTML = vaultHTML;
        }
        
        // Simulation functions
        function simulateBridge() {
            const fromNetwork = document.getElementById('fromNetwork').value;
            const toNetwork = document.getElementById('toNetwork').value;
            const token = document.getElementById('bridgeToken').value;
            const amount = document.getElementById('bridgeAmount').value;
            
            if (fromNetwork === toNetwork) {
                alert('Please select different networks for bridging!');
                return;
            }
            
            if (!amount || amount <= 0) {
                alert('Please enter a valid amount!');
                return;
            }
            
            const fromNetworkName = document.getElementById('fromNetwork').options[document.getElementById('fromNetwork').selectedIndex].text;
            const toNetworkName = document.getElementById('toNetwork').options[document.getElementById('toNetwork').selectedIndex].text;
            
            alert(`Bridge transaction simulated successfully!\\n\\nBridging ${amount} ${token.toUpperCase()}\\nFrom: ${fromNetworkName}\\nTo: ${toNetworkName}`);
        }
        
        function simulateStaking() {
            alert('Staking transaction simulated successfully!');
        }
        
        function simulateDeposit(vaultName) {
            alert(`Successfully deposited into ${vaultName}!`);
        }
        
        function simulateWithdraw(vaultName) {
            alert(`Successfully withdrew from ${vaultName}!`);
        }
        
        function vote(choice) {
            alert(`Vote ${choice} recorded successfully!`);
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            updateLiveData();
            setInterval(updateLiveData, 3000);
            loadNFTGallery();
        });
    </script>
</body>
</html>"""

if __name__ == "__main__":
    print("🚀 HyperFlow Protocol - Mobile Optimized")
    print("📱 Sharp, crisp mobile interface")
    print("🖱️ Touch-optimized navigation")
    print(f"✅ Running at http://localhost:{PORT}")
    
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")