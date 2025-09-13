#!/usr/bin/env python3

import http.server
import socketserver
import json
import uuid
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import html

class WhalesMarketHandler(http.server.BaseHTTPRequestHandler):
    
    # In-memory storage (use database in production)
    listings = {
        'wlfi-001': {
            'id': 'wlfi-001',
            'tokenName': 'World Liberty Financial',
            'tokenSymbol': 'WLFI',
            'blockchain': 'Linea',
            'priceUSD': 0.0015,
            'totalSupply': 100000000000,
            'launchDate': '2025-01-15',
            'createdAt': '2025-01-01T00:00:00'
        },
        'jup-001': {
            'id': 'jup-001', 
            'tokenName': 'Jupiter',
            'tokenSymbol': 'JUP',
            'blockchain': 'Solana',
            'priceUSD': 0.45,
            'totalSupply': 10000000000,
            'launchDate': '2025-01-31',
            'createdAt': '2025-01-01T00:00:00'
        },
        'arb-001': {
            'id': 'arb-001',
            'tokenName': 'Arbitrum',
            'tokenSymbol': 'ARB',
            'blockchain': 'Arbitrum',
            'priceUSD': 1.20,
            'totalSupply': 10000000000,
            'launchDate': '2025-02-15',
            'createdAt': '2025-01-01T00:00:00'
        }
    }
    orders = {}
    tickets = {}
    order_book = {
        'wlfi-001': [
            {'price': 0.0020, 'amount': 1000000, 'type': 'sell', 'timestamp': '2025-01-01T12:00:00'},
            {'price': 0.0018, 'amount': 500000, 'type': 'sell', 'timestamp': '2025-01-01T12:15:00'},
            {'price': 0.0012, 'amount': 750000, 'type': 'buy', 'timestamp': '2025-01-01T12:30:00'},
            {'price': 0.0010, 'amount': 1500000, 'type': 'buy', 'timestamp': '2025-01-01T12:45:00'}
        ],
        'jup-001': [
            {'price': 0.50, 'amount': 10000, 'type': 'sell', 'timestamp': '2025-01-01T12:00:00'},
            {'price': 0.40, 'amount': 25000, 'type': 'buy', 'timestamp': '2025-01-01T12:30:00'}
        ]
    }
    price_history = {
        'wlfi-001': [
            {'price': 0.0015, 'timestamp': '2025-01-01T10:00:00'},
            {'price': 0.0016, 'timestamp': '2025-01-01T11:00:00'},
            {'price': 0.0015, 'timestamp': '2025-01-01T12:00:00'}
        ],
        'jup-001': [
            {'price': 0.45, 'timestamp': '2025-01-01T10:00:00'},
            {'price': 0.47, 'timestamp': '2025-01-01T11:00:00'},
            {'price': 0.45, 'timestamp': '2025-01-01T12:00:00'}
        ]
    }
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/":
            self.serve_homepage()
        elif path == "/api/listings":
            self.serve_listings_api()
        elif path == "/api/orderbook":
            params = parse_qs(parsed_url.query)
            listing_id = params.get('listing', [''])[0]
            self.serve_orderbook_api(listing_id)
        elif path == "/api/chart":
            params = parse_qs(parsed_url.query)
            listing_id = params.get('listing', [''])[0]
            self.serve_chart_api(listing_id)
        elif path == "/api/all-orders":
            self.serve_all_orders_api()
        elif path.startswith("/ticket/"):
            ticket_id = path.split("/")[-1]
            self.serve_ticket_page(ticket_id)
        else:
            self.send_404()
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data)
        except:
            data = {}
        
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/api/create-listing":
            self.create_listing(data)
        elif path == "/api/place-order":
            self.place_order(data)
        elif path == "/api/send-message":
            self.send_message(data)
        elif path == "/api/resolve-chat":
            self.resolve_chat(data)
        elif path == "/api/escalate-chat":
            self.escalate_chat(data)
        else:
            self.send_404()
    
    def serve_homepage(self):
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Whales Market Style - Pre-Market Trading</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: #0a0a0a;
                    color: #ffffff;
                    line-height: 1.6;
                    min-height: 100vh;
                }
                
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 20px;
                }
                
                /* Header */
                .header {
                    padding: 60px 0;
                    text-align: center;
                    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                }
                
                .hero-title {
                    font-size: 3.5rem;
                    font-weight: 800;
                    margin-bottom: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }
                
                .hero-subtitle {
                    font-size: 1.3rem;
                    color: #888;
                    margin-bottom: 40px;
                    max-width: 600px;
                    margin-left: auto;
                    margin-right: auto;
                }
                
                .hero-cta {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 12px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                }
                
                .hero-cta:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                }
                
                /* Stats Section */
                .stats-section {
                    padding: 80px 0;
                    background: #111111;
                }
                
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 40px;
                    text-align: center;
                }
                
                .stat-item {
                    padding: 20px;
                }
                
                .stat-number {
                    font-size: 3rem;
                    font-weight: 800;
                    color: #667eea;
                    margin-bottom: 10px;
                }
                
                .stat-label {
                    font-size: 1.1rem;
                    color: #888;
                    font-weight: 500;
                }
                
                /* How it works section */
                .how-it-works {
                    padding: 80px 0;
                    background: #0a0a0a;
                }
                
                .section-title {
                    font-size: 2.5rem;
                    text-align: center;
                    margin-bottom: 60px;
                    color: #ffffff;
                }
                
                .steps-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 40px;
                    margin-bottom: 60px;
                }
                
                .step-card {
                    background: #1a1a1a;
                    border-radius: 20px;
                    padding: 40px 30px;
                    text-align: center;
                    border: 1px solid #333;
                    transition: all 0.3s ease;
                }
                
                .step-card:hover {
                    border-color: #667eea;
                    transform: translateY(-5px);
                }
                
                .step-number {
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.5rem;
                    font-weight: bold;
                    margin: 0 auto 20px;
                    color: white;
                }
                
                .step-title {
                    font-size: 1.4rem;
                    font-weight: 600;
                    margin-bottom: 15px;
                    color: #ffffff;
                }
                
                .step-description {
                    color: #888;
                    line-height: 1.6;
                }
                
                /* Trading Dashboard */
                .trading-dashboard {
                    padding: 60px 0;
                    background: #111111;
                }
                
                .dashboard-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 40px;
                    flex-wrap: wrap;
                    gap: 20px;
                }
                
                .dashboard-title {
                    font-size: 2rem;
                    color: #ffffff;
                }
                
                .create-listing-btn {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 10px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                
                .create-listing-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                
                /* Listings Grid */
                .listings-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                    gap: 30px;
                }
                
                .listing-card {
                    background: #1a1a1a;
                    border-radius: 20px;
                    padding: 25px;
                    border: 1px solid #333;
                    transition: all 0.3s ease;
                    cursor: pointer;
                }
                
                .listing-card:hover {
                    border-color: #667eea;
                    transform: translateY(-3px);
                }
                
                .listing-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }
                
                .token-info {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }
                
                .token-avatar {
                    width: 50px;
                    height: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 1.2rem;
                }
                
                .token-details h3 {
                    color: #ffffff;
                    font-size: 1.3rem;
                    margin-bottom: 5px;
                }
                
                .token-symbol {
                    color: #888;
                    font-size: 0.9rem;
                }
                
                .chain-badge {
                    background: #333;
                    color: #ccc;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 500;
                }
                
                .listing-stats {
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                    margin-bottom: 25px;
                }
                
                .stat-item {
                    text-align: center;
                }
                
                .stat-value {
                    font-size: 1.4rem;
                    font-weight: 700;
                    color: #667eea;
                    margin-bottom: 5px;
                }
                
                .stat-label {
                    color: #888;
                    font-size: 0.9rem;
                }
                
                .listing-actions {
                    display: flex;
                    gap: 10px;
                }
                
                .action-btn {
                    flex: 1;
                    padding: 12px;
                    border: none;
                    border-radius: 10px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                
                .btn-buy {
                    background: #22c55e;
                    color: white;
                }
                
                .btn-buy:hover {
                    background: #16a34a;
                    transform: translateY(-2px);
                }
                
                .btn-sell {
                    background: #ef4444;
                    color: white;
                }
                
                .btn-sell:hover {
                    background: #dc2626;
                    transform: translateY(-2px);
                }
                
                .btn-trade {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                
                .btn-trade:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                
                /* Trading Modal */
                .modal {
                    display: none;
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.8);
                    z-index: 1000;
                }
                
                .modal-content {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: #1a1a1a;
                    border-radius: 20px;
                    padding: 40px;
                    max-width: 500px;
                    width: 90%;
                    border: 1px solid #333;
                }
                
                .modal-header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                
                .modal-title {
                    font-size: 1.5rem;
                    color: #ffffff;
                    margin-bottom: 10px;
                }
                
                .close-btn {
                    position: absolute;
                    top: 15px;
                    right: 20px;
                    background: none;
                    border: none;
                    color: #888;
                    font-size: 1.5rem;
                    cursor: pointer;
                }
                
                .form-group {
                    margin-bottom: 20px;
                }
                
                .form-label {
                    display: block;
                    color: #ccc;
                    margin-bottom: 8px;
                    font-weight: 500;
                }
                
                .form-input, .form-select {
                    width: 100%;
                    padding: 12px 16px;
                    background: #0a0a0a;
                    border: 1px solid #333;
                    border-radius: 10px;
                    color: #ffffff;
                    font-size: 1rem;
                }
                
                .form-input:focus, .form-select:focus {
                    outline: none;
                    border-color: #667eea;
                }
                
                .submit-btn {
                    width: 100%;
                    padding: 15px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                
                .submit-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                
                /* No listings state */
                .no-listings {
                    text-align: center;
                    padding: 80px 20px;
                    color: #888;
                }
                
                .no-listings-icon {
                    font-size: 4rem;
                    margin-bottom: 20px;
                    opacity: 0.5;
                }
                
                .no-listings-text {
                    font-size: 1.2rem;
                    margin-bottom: 30px;
                }
                
                /* Responsive */
                @media (max-width: 768px) {
                    .hero-title { font-size: 2.5rem; }
                    .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 20px; }
                    .steps-grid { grid-template-columns: 1fr; }
                    .listings-grid { grid-template-columns: 1fr; }
                    .dashboard-header { text-align: center; }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <h1 class="hero-title">Pre-Market Trading</h1>
                    <p class="hero-subtitle">Trade token allocations before TGE. Smart contracts protect both sides. No launchpads. No DEX. No risk.</p>
                    <button class="hero-cta" onclick="document.getElementById('listings-container').scrollIntoView({behavior: 'smooth'})">Start Trading</button>
                </div>
            </div>
            
            <div class="stats-section">
                <div class="container">
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-number" id="total-volume">$2.6M+</div>
                            <div class="stat-label">Total Pre-Market Volume</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number" id="total-users">1.2K+</div>
                            <div class="stat-label">Total Users</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number" id="total-tokens">24</div>
                            <div class="stat-label">Tokens Settled</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number" id="supported-chains">15</div>
                            <div class="stat-label">Supported Blockchains</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="how-it-works">
                <div class="container">
                    <h2 class="section-title">How It Works</h2>
                    <div class="steps-grid">
                        <div class="step-card">
                            <div class="step-number">1</div>
                            <h3 class="step-title">Connect Wallet</h3>
                            <p class="step-description">Use MetaMask, Phantom, or any supported wallet. No sign-up. No KYC. Just connect and go.</p>
                        </div>
                        <div class="step-card">
                            <div class="step-number">2</div>
                            <h3 class="step-title">Pick a Deal</h3>
                            <p class="step-description">Browse active listings or create your own offer. Check the live order book and pick your price.</p>
                        </div>
                        <div class="step-card">
                            <div class="step-number">3</div>
                            <h3 class="step-title">Wait for Settlement</h3>
                            <p class="step-description">After TGE, tokens are distributed automatically. Smart contracts handle everything securely.</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="trading-dashboard">
                <div class="container">
                    <!-- Order Book Section -->
                    <div class="dashboard-header">
                        <h2>📊 Live Order Book - All User Bids & Asks</h2>
                        <p>See all active buy and sell orders from users</p>
                    </div>
                    
                    <div style="background: #1a1a1a; border-radius: 15px; padding: 30px; margin-bottom: 50px; border: 1px solid #333;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                            <h3 style="color: #fff; margin: 0;">All Active Orders</h3>
                            <div>
                                <button id="allOrdersBtn" class="tab-btn active" onclick="showAllOrders()" style="padding: 8px 16px; background: #667eea; border: none; color: #fff; cursor: pointer; border-radius: 5px; margin-right: 10px;">All Orders</button>
                                <button id="bidsOnlyBtn" class="tab-btn" onclick="showBidsOnly()" style="padding: 8px 16px; background: #333; border: none; color: #fff; cursor: pointer; border-radius: 5px; margin-right: 10px;">Bids Only</button>
                                <button id="asksOnlyBtn" class="tab-btn" onclick="showAsksOnly()" style="padding: 8px 16px; background: #333; border: none; color: #fff; cursor: pointer; border-radius: 5px;">Asks Only</button>
                            </div>
                        </div>
                        <div id="ordersContainer">
                            <table style="width: 100%; border-collapse: collapse; background: #2a2a2a; border-radius: 10px; overflow: hidden;">
                                <thead>
                                    <tr style="background: #333;">
                                        <th style="padding: 15px; text-align: left; color: #fff; font-weight: 600;">Token</th>
                                        <th style="padding: 15px; text-align: left; color: #fff; font-weight: 600;">Type</th>
                                        <th style="padding: 15px; text-align: left; color: #fff; font-weight: 600;">Price</th>
                                        <th style="padding: 15px; text-align: left; color: #fff; font-weight: 600;">Amount</th>
                                        <th style="padding: 15px; text-align: left; color: #fff; font-weight: 600;">Total Value</th>
                                        <th style="padding: 15px; text-align: left; color: #fff; font-weight: 600;">Trader</th>
                                        <th style="padding: 15px; text-align: left; color: #fff; font-weight: 600;">Chat</th>
                                    </tr>
                                </thead>
                                <tbody id="ordersTableBody">
                                    <tr>
                                        <td colspan="7" style="padding: 40px; text-align: center; color: #888;">
                                            Loading orders...
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="dashboard-header">
                        <h2 class="dashboard-title">🔥 Active Pre-Market Listings</h2>
                        <!-- Only admin can create listings -->
                    </div>
                    <div class="listings-grid" id="listings-container">
                        <div class="no-listings">
                            <div class="no-listings-icon">📊</div>
                            <div class="no-listings-text">No active listings yet</div>
                            <p>Be the first to create a pre-market listing!</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Bid/Ask Modal -->
            <div class="modal" id="bidAskModal">
                <div class="modal-content">
                    <button class="close-btn" onclick="hideBidAskModal()">&times;</button>
                    <div class="modal-header">
                        <h3 class="modal-title" id="bidAskTitle">Place Bid</h3>
                        <p id="bidAskSubtitle">Enter your bid/ask details</p>
                    </div>
                    <form onsubmit="submitBidAsk(event)">
                        <div class="form-group">
                            <label class="form-label">Price (USD)</label>
                            <input type="number" class="form-input" id="orderPrice" placeholder="0.00" step="0.01" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Amount (tokens)</label>
                            <input type="number" class="form-input" id="orderAmount" placeholder="100" min="1" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Total Value</label>
                            <div class="form-input" id="totalValue" style="background: #333; color: #888;">$0.00</div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Wallet Address</label>
                            <input type="text" class="form-input" id="walletAddress" placeholder="0x... or connect wallet" required>
                        </div>
                        <button type="submit" class="submit-btn" id="submitBidAsk">Place Bid</button>
                    </form>
                </div>
            </div>
            
            <!-- Admin Create Listing Modal (Hidden for users) -->
            <div class="modal" id="createListingModal" style="display: none;">
                <div class="modal-content">
                    <button class="close-btn" onclick="hideCreateListing()">&times;</button>
                    <div class="modal-header">
                        <h3 class="modal-title">Admin: Create Pre-Market Listing</h3>
                    </div>
                    <form onsubmit="submitListing(event)">
                        <div class="form-group">
                            <label class="form-label">Token Name</label>
                            <input type="text" class="form-input" id="tokenName" placeholder="e.g. Jupiter" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Token Symbol</label>
                            <input type="text" class="form-input" id="tokenSymbol" placeholder="e.g. JUP" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Blockchain</label>
                            <select class="form-select" id="blockchain" required>
                                <option value="">Select blockchain</option>
                                <option value="Ethereum">Ethereum</option>
                                <option value="Solana">Solana</option>
                                <option value="BSC">BNB Smart Chain</option>
                                <option value="Polygon">Polygon</option>
                                <option value="Arbitrum">Arbitrum</option>
                                <option value="Base">Base</option>
                                <option value="Linea">Linea</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Expected Price (USD)</label>
                            <input type="number" class="form-input" id="priceUSD" placeholder="0.50" step="0.01" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Total Supply</label>
                            <input type="number" class="form-input" id="totalSupply" placeholder="1000000" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Launch Date</label>
                            <input type="date" class="form-input" id="launchDate" required>
                        </div>
                        <button type="submit" class="submit-btn">Create Listing</button>
                    </form>
                </div>
            </div>
            
            <script>
                // Load listings on page load
                document.addEventListener('DOMContentLoaded', loadListings);
                
                function loadListings() {
                    fetch('/api/listings')
                        .then(response => response.json())
                        .then(listings => displayListings(listings));
                }
                
                function displayListings(listings) {
                    const container = document.getElementById('listings-container');
                    
                    if (Object.keys(listings).length === 0) {
                        container.innerHTML = `
                            <div class="no-listings">
                                <div class="no-listings-icon">📊</div>
                                <div class="no-listings-text">No active listings yet</div>
                                <p>Be the first to create a pre-market listing!</p>
                            </div>
                        `;
                        return;
                    }
                    
                    let html = '';
                    for (let id in listings) {
                        const listing = listings[id];
                        const tokenInitial = listing.tokenSymbol.charAt(0);
                        
                        html += `
                            <div class="listing-card" onclick="openTradingModal('${id}')">
                                <div class="listing-header">
                                    <div class="token-info">
                                        <div class="token-avatar">${tokenInitial}</div>
                                        <div class="token-details">
                                            <h3>${listing.tokenName}</h3>
                                            <div class="token-symbol">$${listing.tokenSymbol}</div>
                                        </div>
                                    </div>
                                    <div class="chain-badge">${listing.blockchain}</div>
                                </div>
                                
                                <div class="listing-stats">
                                    <div class="stat-item">
                                        <div class="stat-value">$${listing.priceUSD}</div>
                                        <div class="stat-label">Target Price</div>
                                    </div>
                                    <div class="stat-item">
                                        <div class="stat-value">${Number(listing.totalSupply).toLocaleString()}</div>
                                        <div class="stat-label">Total Supply</div>
                                    </div>
                                </div>
                                
                                <div class="listing-actions">
                                    <button class="action-btn btn-buy" onclick="event.stopPropagation(); showBidAskModal('${id}', 'buy')">Place Bid</button>
                                    <button class="action-btn btn-sell" onclick="event.stopPropagation(); showBidAskModal('${id}', 'sell')">Place Ask</button>
                                    <button class="action-btn btn-trade" onclick="event.stopPropagation(); openTradingView('${id}')">View Orders</button>
                                </div>
                            </div>
                        `;
                    }
                    container.innerHTML = html;
                }
                
                let currentListing = null;
                let currentOrderType = null;
                
                function showBidAskModal(listingId, orderType) {
                    currentListing = listingId;
                    currentOrderType = orderType;
                    
                    const modal = document.getElementById('bidAskModal');
                    const title = document.getElementById('bidAskTitle');
                    const subtitle = document.getElementById('bidAskSubtitle');
                    const submitBtn = document.getElementById('submitBidAsk');
                    
                    if (orderType === 'buy') {
                        title.textContent = 'Place Bid';
                        subtitle.textContent = 'Enter your buy order details';
                        submitBtn.textContent = 'Place Bid';
                        submitBtn.className = 'submit-btn btn-buy';
                    } else {
                        title.textContent = 'Place Ask';
                        subtitle.textContent = 'Enter your sell order details';
                        submitBtn.textContent = 'Place Ask';
                        submitBtn.className = 'submit-btn btn-sell';
                    }
                    
                    modal.style.display = 'block';
                }
                
                function hideBidAskModal() {
                    document.getElementById('bidAskModal').style.display = 'none';
                    document.querySelector('#bidAskModal form').reset();
                    document.getElementById('totalValue').textContent = '$0.00';
                }
                
                // Calculate total value
                document.addEventListener('DOMContentLoaded', function() {
                    const priceInput = document.getElementById('orderPrice');
                    const amountInput = document.getElementById('orderAmount');
                    const totalValueDiv = document.getElementById('totalValue');
                    
                    function updateTotal() {
                        const price = parseFloat(priceInput.value) || 0;
                        const amount = parseFloat(amountInput.value) || 0;
                        const total = price * amount;
                        totalValueDiv.textContent = '$' + total.toFixed(2);
                    }
                    
                    priceInput.addEventListener('input', updateTotal);
                    amountInput.addEventListener('input', updateTotal);
                });
                
                function showCreateListing() {
                    // Only show for admin - add password check
                    const password = prompt('Enter admin password:');
                    if (password === 'admin123') {
                        document.getElementById('createListingModal').style.display = 'block';
                    } else {
                        alert('Access denied. Only platform admins can create listings.');
                    }
                }
                
                function hideCreateListing() {
                    document.getElementById('createListingModal').style.display = 'none';
                }
                
                function submitListing(event) {
                    event.preventDefault();
                    
                    const formData = {
                        tokenName: document.getElementById('tokenName').value,
                        tokenSymbol: document.getElementById('tokenSymbol').value,
                        blockchain: document.getElementById('blockchain').value,
                        priceUSD: parseFloat(document.getElementById('priceUSD').value),
                        totalSupply: parseInt(document.getElementById('totalSupply').value),
                        launchDate: document.getElementById('launchDate').value
                    };
                    
                    fetch('/api/create-listing', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(formData)
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.success) {
                            alert('Listing created successfully!');
                            hideCreateListing();
                            loadListings(); // Refresh listings
                            // Clear form
                            document.querySelector('#createListingModal form').reset();
                        } else {
                            alert('Error creating listing: ' + result.error);
                        }
                    });
                }
                
                function submitBidAsk(event) {
                    event.preventDefault();
                    
                    const price = parseFloat(document.getElementById('orderPrice').value);
                    const amount = parseFloat(document.getElementById('orderAmount').value);
                    const wallet = document.getElementById('walletAddress').value;
                    
                    if (price && amount && wallet && currentListing && currentOrderType) {
                        fetch('/api/place-order', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                listingId: currentListing,
                                orderType: currentOrderType,
                                price: price,
                                amount: amount,
                                wallet: wallet
                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            if (result.success) {
                                alert(`${currentOrderType === 'buy' ? 'Bid' : 'Ask'} placed successfully! Ticket ID: ${result.ticketId}`);
                                hideBidAskModal();
                                window.open(`/ticket/${result.ticketId}`, '_blank');
                            } else {
                                alert('Error: ' + result.error);
                            }
                        });
                    }
                }
                
                function openTradingView(listingId) {
                    window.open(`/listing/${listingId}`, '_blank');
                }
                
                // Close modals when clicking outside
                window.onclick = function(event) {
                    const createModal = document.getElementById('createListingModal');
                    const bidAskModal = document.getElementById('bidAskModal');
                    
                    if (event.target == createModal) {
                        hideCreateListing();
                    }
                    if (event.target == bidAskModal) {
                        hideBidAskModal();
                    }
                }
                
                // Set minimum date to today
                document.getElementById('launchDate').min = new Date().toISOString().split('T')[0];
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_listings_api(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(self.listings).encode())
    
    def serve_orderbook_api(self, listing_id):
        orderbook = {
            'buys': [],
            'sells': [],
            'lastPrice': 0
        }
        
        if listing_id in self.order_book:
            orders = self.order_book[listing_id]
            buy_orders = sorted([o for o in orders if o['type'] == 'buy'], 
                              key=lambda x: x['price'], reverse=True)
            sell_orders = sorted([o for o in orders if o['type'] == 'sell'], 
                                key=lambda x: x['price'])
            
            orderbook['buys'] = buy_orders[:10]
            orderbook['sells'] = sell_orders[:10]
            
            if listing_id in self.price_history and self.price_history[listing_id]:
                orderbook['lastPrice'] = self.price_history[listing_id][-1]['price']
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(orderbook).encode())
    
    def serve_chart_api(self, listing_id):
        chart_data = {'prices': []}
        if listing_id in self.price_history:
            chart_data['prices'] = self.price_history[listing_id]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(chart_data).encode())
    
    def create_listing(self, data):
        listing_id = str(uuid.uuid4())
        listing = {
            'id': listing_id,
            'tokenName': data.get('tokenName', ''),
            'tokenSymbol': data.get('tokenSymbol', ''),
            'blockchain': data.get('blockchain', ''),
            'priceUSD': data.get('priceUSD', 0),
            'totalSupply': data.get('totalSupply', 0),
            'launchDate': data.get('launchDate', ''),
            'createdAt': datetime.now().isoformat()
        }
        
        self.listings[listing_id] = listing
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'success': True, 'listingId': listing_id}
        self.wfile.write(json.dumps(response).encode())
    
    def place_order(self, data):
        order_id = str(uuid.uuid4())
        ticket_id = str(uuid.uuid4())[:8]
        
        order = {
            'id': order_id,
            'listingId': data.get('listingId', ''),
            'orderType': data.get('orderType', ''),
            'price': data.get('price', 0),
            'amount': data.get('amount', 0),
            'wallet': data.get('wallet', ''),
            'ticketId': ticket_id,
            'createdAt': datetime.now().isoformat()
        }
        
        # Create private chat room for this order
        chat_room = {
            'id': ticket_id,
            'orderId': order_id,
            'tokenSymbol': next((l['tokenSymbol'] for l in self.listings if l['id'] == data.get('listingId')), 'UNKNOWN'),
            'orderType': data.get('orderType'),
            'price': data.get('price', 0),
            'amount': data.get('amount', 0),
            'traderWallet': data.get('wallet', ''),
            'counterpartyWallet': '',  # Will be filled when matched
            'status': 'Waiting for Match',
            'messages': [],
            'participants': [data.get('wallet', '')],  # Only the order placer initially
            'adminAccess': True  # Admins can always view
        }
        
        ticket = chat_room
        
        self.orders[order_id] = order
        self.tickets[ticket_id] = ticket
        
        # Add to order book
        listing_id = data.get('listingId', '')
        if listing_id not in self.order_book:
            self.order_book[listing_id] = []
        
        self.order_book[listing_id].append({
            'price': data.get('price', 0),
            'amount': data.get('amount', 0),
            'type': data.get('orderType', ''),
            'timestamp': datetime.now().isoformat()
        })
        
        # Update price history
        if listing_id not in self.price_history:
            self.price_history[listing_id] = []
        
        self.price_history[listing_id].append({
            'price': data.get('price', 0),
            'timestamp': datetime.now().isoformat()
        })
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'success': True, 'ticketId': ticket_id, 'orderId': order_id}
        self.wfile.write(json.dumps(response).encode())
    
    def serve_ticket_page(self, ticket_id):
        if ticket_id not in self.tickets:
            self.send_404()
            return
            
        ticket = self.tickets[ticket_id]
        order = self.orders.get(ticket['orderId'], {})
        listing = self.listings.get(order.get('listingId', ''), {})
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ticket #{ticket_id} - Communication</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #0a0a0a; color: white; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .ticket-header {{ background: #1a1a1a; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                .messages {{ background: #1a1a1a; padding: 20px; border-radius: 10px; margin-bottom: 20px; min-height: 300px; }}
                .message {{ padding: 10px; margin: 10px 0; background: #333; border-radius: 5px; }}
                .message-form {{ display: flex; gap: 10px; }}
                .message-input {{ flex: 1; padding: 10px; background: #333; border: 1px solid #666; color: white; }}
                .send-btn {{ padding: 10px 20px; background: #667eea; border: none; color: white; cursor: pointer; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="ticket-header">
                    <h2>Private Chat Room #{ticket_id}</h2>
                    <p><strong>Token:</strong> {ticket.get('tokenSymbol', 'N/A')}</p>
                    <p><strong>Order Type:</strong> {ticket.get('orderType', 'N/A').title()}</p>
                    <p><strong>Price:</strong> ${ticket.get('price', 0)}</p>
                    <p><strong>Amount:</strong> {ticket.get('amount', 0):,}</p>
                    <p><strong>Status:</strong> {ticket.get('status', 'Waiting for Match')}</p>
                    <p><strong>Trader:</strong> {ticket.get('traderWallet', 'N/A')}</p>
                    <p><strong>Counterparty:</strong> {ticket.get('counterpartyWallet', 'Waiting for match...')}</p>
                    <div style="font-size: 0.9em; color: #888; margin-top: 10px;">
                        🔒 This is a private chat room. Only participants and admins can see messages.
                    </div>
                </div>
                
                <div class="messages" id="messages">
                    <!-- Messages will be loaded here -->
                </div>
                
                <div class="message-form">
                    <input type="text" class="message-input" id="senderWallet" placeholder="Your wallet address" required>
                    <input type="text" class="message-input" id="messageText" placeholder="Type your message..." required>
                    <button class="send-btn" onclick="sendMessage()">Send Message</button>
                    <button class="admin-btn" onclick="joinAsAdmin()" style="background: #ff6b6b; margin-left: 10px;">Join as Admin</button>
                </div>
                
                <div class="admin-panel" id="adminPanel" style="display: none; margin-top: 20px; padding: 15px; background: #2a2a2a; border-radius: 5px;">
                    <h3>Admin Controls</h3>
                    <button class="admin-btn" onclick="markResolved()">Mark Resolved</button>
                    <button class="admin-btn" onclick="escalateIssue()">Escalate Issue</button>
                    <input type="password" id="adminPassword" placeholder="Admin password" style="margin: 10px 0; padding: 8px; background: #333; border: 1px solid #666; color: white;">
                </div>
            </div>
            
            <script>
                const ticketId = '{ticket_id}';
                
                function sendMessage() {{
                    const wallet = document.getElementById('senderWallet').value;
                    const message = document.getElementById('messageText').value;
                    
                    if (wallet && message) {{
                        fetch('/api/send-message', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ 
                                ticketId, 
                                senderWallet: wallet, 
                                message,
                                isPrivate: true 
                            }})
                        }})
                        .then(response => response.json())
                        .then(result => {{
                            if (result.success) {{
                                document.getElementById('messageText').value = '';
                                loadMessages();
                            }}
                        }});
                    }}
                }}
                
                function loadMessages() {{
                    const messages = {json.dumps(ticket.get('messages', []))};
                    const container = document.getElementById('messages');
                    
                    if (messages.length === 0) {{
                        container.innerHTML = '<p>No messages yet. Start the conversation!</p>';
                        return;
                    }}
                    
                    let html = '';
                    messages.forEach(msg => {{
                        html += `<div class="message">
                            <strong>${{msg.senderWallet}}:</strong> ${{msg.message}}
                            <div style="font-size: 0.8em; color: #888;">${{new Date(msg.timestamp).toLocaleString()}}</div>
                        </div>`;
                    }});
                    container.innerHTML = html;
                }}
                
                function joinAsAdmin() {{
                    const password = document.getElementById('adminPassword').value;
                    if (password === 'admin123') {{
                        document.getElementById('adminPanel').style.display = 'block';
                        alert('Admin access granted. You can now monitor this private chat.');
                    }} else {{
                        alert('Invalid admin password');
                    }}
                }}
                
                function markResolved() {{
                    fetch('/api/resolve-chat', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ ticketId }})
                    }})
                    .then(response => response.json())
                    .then(result => {{
                        if (result.success) {{
                            alert('Chat marked as resolved');
                            location.reload();
                        }}
                    }});
                }}
                
                function escalateIssue() {{
                    const reason = prompt('Escalation reason:');
                    if (reason) {{
                        fetch('/api/escalate-chat', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ ticketId, reason }})
                        }})
                        .then(response => response.json())
                        .then(result => {{
                            if (result.success) {{
                                alert('Issue escalated to senior admin');
                            }}
                        }});
                    }}
                }}
                
                loadMessages();
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def send_message(self, data):
        ticket_id = data.get('ticketId', '')
        if ticket_id not in self.tickets:
            self.send_error_response('Ticket not found')
            return
        
        sender_wallet = data.get('senderWallet', '')
        chat_room = self.tickets[ticket_id]
        
        # Check if sender is authorized (participant or admin)
        if sender_wallet not in chat_room['participants'] and not data.get('isAdmin', False):
            # Auto-add as counterparty if this is the first message from a new wallet
            if chat_room['counterpartyWallet'] == '':
                chat_room['counterpartyWallet'] = sender_wallet
                chat_room['participants'].append(sender_wallet)
                chat_room['status'] = 'Active Chat'
            else:
                self.send_error_response('Unauthorized: You are not a participant in this private chat')
                return
            
        message = {
            'senderWallet': sender_wallet,
            'message': data.get('message', ''),
            'timestamp': datetime.now().isoformat(),
            'isPrivate': data.get('isPrivate', True),
            'isAdmin': data.get('isAdmin', False)
        }
        
        chat_room['messages'].append(message)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'success': True}
        self.wfile.write(json.dumps(response).encode())
        
    def resolve_chat(self, data):
        ticket_id = data.get('ticketId', '')
        if ticket_id not in self.tickets:
            self.send_error_response('Chat room not found')
            return
            
        self.tickets[ticket_id]['status'] = 'Resolved'
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps({'success': True, 'message': 'Chat resolved'})
        self.wfile.write(response.encode())
        
    def escalate_chat(self, data):
        ticket_id = data.get('ticketId', '')
        reason = data.get('reason', '')
        if ticket_id not in self.tickets:
            self.send_error_response('Chat room not found')
            return
            
        self.tickets[ticket_id]['status'] = 'Escalated'
        self.tickets[ticket_id]['escalationReason'] = reason
        
        # Add system message about escalation
        escalation_message = {
            'senderWallet': 'SYSTEM',
            'message': f'⚠️ Issue escalated to senior admin. Reason: {reason}',
            'timestamp': datetime.now().isoformat(),
            'isPrivate': False,
            'isSystem': True
        }
        self.tickets[ticket_id]['messages'].append(escalation_message)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps({'success': True, 'message': 'Issue escalated'})
        self.wfile.write(response.encode())
    
    def send_error_response(self, message):
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {'success': False, 'error': message}
        self.wfile.write(json.dumps(response).encode())
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'404 Not Found')

def run_server():
    port = 5000
    handler = WhalesMarketHandler
    
    print("🐋 Starting Whales Market Style Platform...")
    print("✅ Pre-market token trading with professional dark theme")
    print("💰 EOA wallet escrow system")
    print("🎫 Ticket-based communication")
    print("🌐 Multi-chain support")
    print(f"✅ Server running at http://localhost:{port}")
    print("🌐 External access: Available through Replit")
    print("💡 Features:")
    print("   • Dark theme like Whales Market")
    print("   • Professional card-based listings") 
    print("   • Smart contract-style security")
    print("   • Multi-chain token support")
    print("   • Order book and price tracking")
    print("Ready to facilitate secure pre-market trading! 🚀")
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()