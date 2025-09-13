#!/usr/bin/env python3
"""
Multi-Chain Pre-Market Trading Platform
Allows users to buy/sell tokens before official launch with ticket-based communication system
"""

import json
import time
import uuid
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import html

class PreMarketTradingHandler(BaseHTTPRequestHandler):
    
    # In-memory storage (use database in production)
    listings = {}
    orders = {}
    tickets = {}
    users = {}
    order_book = {}  # Store buy/sell orders for each listing
    price_history = {}  # Store price history for charts
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/":
            self.serve_homepage()
        elif path == "/api/listings":
            self.serve_listings_api()
        elif path == "/api/orders":
            self.serve_orders_api()
        elif path == "/api/orderbook":
            params = parse_qs(parsed_url.query)
            listing_id = params.get('listing', [''])[0]
            self.serve_orderbook_api(listing_id)
        elif path == "/api/chart":
            params = parse_qs(parsed_url.query)
            listing_id = params.get('listing', [''])[0]
            self.serve_chart_api(listing_id)
        elif path.startswith("/ticket/"):
            ticket_id = path.split("/")[-1]
            self.serve_ticket_page(ticket_id)
        elif path.startswith("/listing/"):
            listing_id = path.split("/")[-1]
            self.serve_listing_page(listing_id)
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
        else:
            self.send_404()
    
    def serve_homepage(self):
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PreMarket Pro - Multi-Chain Token Trading</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', system-ui, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: #333;
                }
                .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                .header {
                    text-align: center;
                    color: white;
                    padding: 40px 0;
                    margin-bottom: 40px;
                }
                .header h1 {
                    font-size: 3rem;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .header p {
                    font-size: 1.2rem;
                    opacity: 0.9;
                }
                .main-content {
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }
                .stat-card {
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 15px;
                    text-align: center;
                }
                .stat-number {
                    font-size: 2.5rem;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .stat-label {
                    font-size: 1rem;
                    opacity: 0.9;
                }
                .listings-section {
                    margin-top: 40px;
                }
                .trading-view {
                    display: grid;
                    grid-template-columns: 1fr 350px;
                    gap: 20px;
                    margin-top: 30px;
                }
                .chart-container {
                    background: white;
                    border-radius: 15px;
                    padding: 20px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                }
                .orderbook-container {
                    background: white;
                    border-radius: 15px;
                    padding: 20px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                }
                .chart-title {
                    font-size: 1.2rem;
                    font-weight: bold;
                    margin-bottom: 15px;
                    color: #333;
                }
                #price-chart {
                    width: 100%;
                    height: 400px;
                    border: 2px solid #e9ecef;
                    border-radius: 10px;
                }
                .orderbook-title {
                    font-size: 1.2rem;
                    font-weight: bold;
                    margin-bottom: 15px;
                    color: #333;
                    text-align: center;
                }
                .orderbook-section {
                    margin-bottom: 20px;
                }
                .orderbook-header {
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    gap: 10px;
                    padding: 10px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 0.9rem;
                    color: #666;
                }
                .order-row {
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    gap: 10px;
                    padding: 8px 10px;
                    border-bottom: 1px solid #f0f0f0;
                    font-size: 0.9rem;
                }
                .sell-order {
                    color: #ff6b6b;
                }
                .buy-order {
                    color: #56ab2f;
                }
                .current-price {
                    text-align: center;
                    padding: 15px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 10px;
                    margin: 15px 0;
                    font-weight: bold;
                }
                .order-form {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    margin-top: 20px;
                }
                .form-group {
                    margin-bottom: 15px;
                }
                .form-label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                    color: #333;
                }
                .form-input {
                    width: 100%;
                    padding: 10px;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    font-size: 1rem;
                }
                .order-buttons {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 10px;
                }
                @media (max-width: 768px) {
                    .trading-view {
                        grid-template-columns: 1fr;
                    }
                }
                .section-title {
                    font-size: 2rem;
                    margin-bottom: 20px;
                    color: #333;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 10px;
                }
                .listing-card {
                    background: #f8f9fa;
                    border: 2px solid #e9ecef;
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 20px;
                    transition: all 0.3s ease;
                }
                .listing-card:hover {
                    border-color: #667eea;
                    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.1);
                    transform: translateY(-2px);
                }
                .listing-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                }
                .token-name {
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #333;
                }
                .chain-badge {
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    font-weight: bold;
                }
                .price-info {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 15px;
                }
                .price-item {
                    text-align: center;
                }
                .price-label {
                    color: #666;
                    font-size: 0.9rem;
                    margin-bottom: 5px;
                }
                .price-value {
                    font-size: 1.2rem;
                    font-weight: bold;
                    color: #333;
                }
                .action-buttons {
                    display: flex;
                    gap: 15px;
                }
                .btn {
                    flex: 1;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 10px;
                    font-size: 1rem;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                .btn-buy {
                    background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
                    color: white;
                }
                .btn-buy:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(86, 171, 47, 0.3);
                }
                .btn-sell {
                    background: linear-gradient(135deg, #ff6b6b 0%, #ffa8a8 100%);
                    color: white;
                }
                .btn-sell:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
                }
                .create-listing-btn {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 15px;
                    font-size: 1.1rem;
                    font-weight: bold;
                    cursor: pointer;
                    margin-bottom: 30px;
                    transition: all 0.3s ease;
                }
                .create-listing-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
                }
                .no-listings {
                    text-align: center;
                    color: #666;
                    font-size: 1.1rem;
                    margin: 40px 0;
                }
                @media (max-width: 768px) {
                    .main-content { padding: 20px; }
                    .header h1 { font-size: 2rem; }
                    .stats-grid { grid-template-columns: 1fr; }
                    .action-buttons { flex-direction: column; }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 PreMarket Pro</h1>
                    <p>Trade tokens before they launch - Multi-chain pre-market trading platform</p>
                </div>
                
                <div class="main-content">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">0</div>
                            <div class="stat-label">Active Listings</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">$0</div>
                            <div class="stat-label">Total Volume</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">0</div>
                            <div class="stat-label">Completed Trades</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">2-5%</div>
                            <div class="stat-label">Trading Fees</div>
                        </div>
                    </div>
                    
                    <button class="create-listing-btn" onclick="showCreateListing()">
                        ➕ Create New Pre-Market Listing
                    </button>
                    
                    <div class="listings-section">
                        <h2 class="section-title">📈 Active Pre-Market Listings</h2>
                        <div id="listings-container">
                            <div class="no-listings">
                                No active listings yet. Be the first to create a pre-market listing!
                            </div>
                        </div>
                    </div>
                    
                    <div class="trading-view" id="trading-view" style="display: none;">
                        <div class="chart-container">
                            <div class="chart-title">📊 Price Chart</div>
                            <canvas id="price-chart"></canvas>
                        </div>
                        
                        <div class="orderbook-container">
                            <div class="orderbook-title">📋 Order Book</div>
                            
                            <div class="orderbook-section">
                                <div class="orderbook-header">
                                    <span>Price (USD)</span>
                                    <span>Amount</span>
                                    <span>Total</span>
                                </div>
                                <div id="sell-orders">
                                    <!-- Sell orders will be populated here -->
                                </div>
                            </div>
                            
                            <div class="current-price" id="current-price">
                                $0.00
                            </div>
                            
                            <div class="orderbook-section">
                                <div id="buy-orders">
                                    <!-- Buy orders will be populated here -->
                                </div>
                            </div>
                            
                            <div class="order-form">
                                <div class="form-group">
                                    <label class="form-label">Price (USD)</label>
                                    <input type="number" class="form-input" id="order-price" placeholder="0.00" step="0.01">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Amount</label>
                                    <input type="number" class="form-input" id="order-amount" placeholder="0" step="1">
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Email</label>
                                    <input type="email" class="form-input" id="order-email" placeholder="your@email.com">
                                </div>
                                <div class="order-buttons">
                                    <button class="btn btn-buy" onclick="placeOrderFromForm('buy')">Buy</button>
                                    <button class="btn btn-sell" onclick="placeOrderFromForm('sell')">Sell</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                function showCreateListing() {
                    const tokenName = prompt("Enter token name:");
                    const tokenSymbol = prompt("Enter token symbol:");
                    const blockchain = prompt("Enter blockchain (ETH/BSC/MATIC/etc):");
                    const priceUSD = prompt("Enter target price in USD:");
                    const totalSupply = prompt("Enter total supply:");
                    const launchDate = prompt("Enter expected launch date (YYYY-MM-DD):");
                    
                    if (tokenName && tokenSymbol && blockchain && priceUSD && totalSupply && launchDate) {
                        createListing({
                            tokenName,
                            tokenSymbol,
                            blockchain,
                            priceUSD: parseFloat(priceUSD),
                            totalSupply: parseFloat(totalSupply),
                            launchDate
                        });
                    }
                }
                
                function createListing(data) {
                    fetch('/api/create-listing', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.success) {
                            alert('Listing created successfully!');
                            location.reload();
                        } else {
                            alert('Error creating listing: ' + result.error);
                        }
                    });
                }
                
                function placeOrder(listingId, orderType) {
                    const amount = prompt(`Enter amount to ${orderType}:`);
                    const price = prompt("Enter price per token (USD):");
                    const email = prompt("Enter your email for communication:");
                    
                    if (amount && price && email) {
                        fetch('/api/place-order', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                listingId,
                                orderType,
                                amount: parseFloat(amount),
                                price: parseFloat(price),
                                email
                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            if (result.success) {
                                alert(`${orderType} order placed successfully! Ticket ID: ${result.ticketId}`);
                                window.open(`/ticket/${result.ticketId}`, '_blank');
                            } else {
                                alert('Error placing order: ' + result.error);
                            }
                        });
                    }
                }
                
                // Load listings on page load
                window.onload = function() {
                    fetch('/api/listings')
                        .then(response => response.json())
                        .then(listings => {
                            displayListings(listings);
                        });
                };
                
                let currentListing = null;
                
                function displayListings(listings) {
                    const container = document.getElementById('listings-container');
                    
                    if (Object.keys(listings).length === 0) {
                        container.innerHTML = '<div class="no-listings">No active listings yet. Be the first to create a pre-market listing!</div>';
                        return;
                    }
                    
                    let html = '';
                    for (let id in listings) {
                        const listing = listings[id];
                        html += `
                            <div class="listing-card">
                                <div class="listing-header">
                                    <div class="token-name">${listing.tokenName} (${listing.tokenSymbol})</div>
                                    <div class="chain-badge">${listing.blockchain}</div>
                                </div>
                                <div class="price-info">
                                    <div class="price-item">
                                        <div class="price-label">Target Price</div>
                                        <div class="price-value">$${listing.priceUSD}</div>
                                    </div>
                                    <div class="price-item">
                                        <div class="price-label">Total Supply</div>
                                        <div class="price-value">${listing.totalSupply.toLocaleString()}</div>
                                    </div>
                                    <div class="price-item">
                                        <div class="price-label">Launch Date</div>
                                        <div class="price-value">${listing.launchDate}</div>
                                    </div>
                                </div>
                                <div class="action-buttons">
                                    <button class="btn btn-buy" onclick="placeOrder('${id}', 'buy')">
                                        💰 Place Buy Order
                                    </button>
                                    <button class="btn btn-sell" onclick="placeOrder('${id}', 'sell')">
                                        💸 Place Sell Order
                                    </button>
                                    <button class="btn" onclick="showTradingView('${id}')" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                                        📊 View Trading
                                    </button>
                                </div>
                            </div>
                        `;
                    }
                    container.innerHTML = html;
                }
                
                function showTradingView(listingId) {
                    currentListing = listingId;
                    document.getElementById('trading-view').style.display = 'grid';
                    loadOrderBook(listingId);
                    loadPriceChart(listingId);
                    document.getElementById('trading-view').scrollIntoView({ behavior: 'smooth' });
                }
                
                function loadOrderBook(listingId) {
                    fetch(`/api/orderbook?listing=${listingId}`)
                        .then(response => response.json())
                        .then(orderbook => {
                            displayOrderBook(orderbook);
                        });
                }
                
                function loadPriceChart(listingId) {
                    fetch(`/api/chart?listing=${listingId}`)
                        .then(response => response.json())
                        .then(chartData => {
                            drawPriceChart(chartData);
                        });
                }
                
                function displayOrderBook(orderbook) {
                    const sellOrders = document.getElementById('sell-orders');
                    const buyOrders = document.getElementById('buy-orders');
                    const currentPrice = document.getElementById('current-price');
                    
                    // Display sell orders (highest price first)
                    let sellHtml = '';
                    orderbook.sells.forEach(order => {
                        const total = (order.price * order.amount).toFixed(2);
                        sellHtml += `
                            <div class="order-row sell-order">
                                <span>$${order.price}</span>
                                <span>${order.amount.toLocaleString()}</span>
                                <span>$${total}</span>
                            </div>
                        `;
                    });
                    sellOrders.innerHTML = sellHtml;
                    
                    // Display buy orders (highest price first)
                    let buyHtml = '';
                    orderbook.buys.forEach(order => {
                        const total = (order.price * order.amount).toFixed(2);
                        buyHtml += `
                            <div class="order-row buy-order">
                                <span>$${order.price}</span>
                                <span>${order.amount.toLocaleString()}</span>
                                <span>$${total}</span>
                            </div>
                        `;
                    });
                    buyOrders.innerHTML = buyHtml;
                    
                    // Update current price
                    const lastPrice = orderbook.lastPrice || 0;
                    currentPrice.innerHTML = `$${lastPrice.toFixed(4)}`;
                }
                
                function drawPriceChart(chartData) {
                    const canvas = document.getElementById('price-chart');
                    const ctx = canvas.getContext('2d');
                    
                    // Simple chart drawing (in production, use Chart.js or similar)
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = '#f8f9fa';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    if (chartData.prices && chartData.prices.length > 0) {
                        ctx.strokeStyle = '#667eea';
                        ctx.lineWidth = 2;
                        ctx.beginPath();
                        
                        const maxPrice = Math.max(...chartData.prices.map(p => p.price));
                        const minPrice = Math.min(...chartData.prices.map(p => p.price));
                        const priceRange = maxPrice - minPrice || 1;
                        
                        chartData.prices.forEach((point, index) => {
                            const x = (index / (chartData.prices.length - 1)) * canvas.width;
                            const y = canvas.height - ((point.price - minPrice) / priceRange) * canvas.height;
                            
                            if (index === 0) {
                                ctx.moveTo(x, y);
                            } else {
                                ctx.lineTo(x, y);
                            }
                        });
                        
                        ctx.stroke();
                    } else {
                        ctx.fillStyle = '#666';
                        ctx.font = '16px Arial';
                        ctx.textAlign = 'center';
                        ctx.fillText('No price data available', canvas.width / 2, canvas.height / 2);
                    }
                }
                
                function placeOrderFromForm(orderType) {
                    const price = document.getElementById('order-price').value;
                    const amount = document.getElementById('order-amount').value;
                    const email = document.getElementById('order-email').value;
                    
                    if (price && amount && email && currentListing) {
                        fetch('/api/place-order', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                listingId: currentListing,
                                orderType,
                                amount: parseFloat(amount),
                                price: parseFloat(price),
                                email
                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            if (result.success) {
                                alert(`${orderType} order placed successfully! Ticket ID: ${result.ticketId}`);
                                // Clear form
                                document.getElementById('order-price').value = '';
                                document.getElementById('order-amount').value = '';
                                // Reload order book
                                loadOrderBook(currentListing);
                                window.open(`/ticket/${result.ticketId}`, '_blank');
                            } else {
                                alert('Error placing order: ' + result.error);
                            }
                        });
                    } else {
                        alert('Please fill in all fields');
                    }
                }
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_listings_api(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(self.listings).encode())
    
    def serve_orders_api(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(self.orders).encode())
    
    def serve_orderbook_api(self, listing_id):
        orderbook = {
            'buys': [],
            'sells': [],
            'lastPrice': 0
        }
        
        if listing_id in self.order_book:
            orders = self.order_book[listing_id]
            
            # Sort buy orders by price (highest first)
            buy_orders = sorted([o for o in orders if o['type'] == 'buy'], 
                              key=lambda x: x['price'], reverse=True)
            
            # Sort sell orders by price (lowest first)
            sell_orders = sorted([o for o in orders if o['type'] == 'sell'], 
                                key=lambda x: x['price'])
            
            orderbook['buys'] = buy_orders[:10]  # Top 10 buy orders
            orderbook['sells'] = sell_orders[:10]  # Top 10 sell orders
            
            # Get last traded price
            if listing_id in self.price_history and self.price_history[listing_id]:
                orderbook['lastPrice'] = self.price_history[listing_id][-1]['price']
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(orderbook).encode())
    
    def serve_chart_api(self, listing_id):
        chart_data = {
            'prices': []
        }
        
        if listing_id in self.price_history:
            chart_data['prices'] = self.price_history[listing_id]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(chart_data).encode())
    
    def serve_ticket_page(self, ticket_id):
        if ticket_id not in self.tickets:
            self.send_404()
            return
        
        ticket = self.tickets[ticket_id]
        listing = self.listings.get(ticket['listingId'], {})
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Trade Ticket #{ticket_id}</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', system-ui, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }}
                .ticket-container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .ticket-header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .ticket-header h1 {{
                    font-size: 2rem;
                    margin-bottom: 10px;
                }}
                .ticket-id {{
                    font-size: 1rem;
                    opacity: 0.9;
                }}
                .ticket-content {{
                    padding: 30px;
                }}
                .order-details {{
                    background: #f8f9fa;
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 30px;
                }}
                .detail-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 10px 0;
                    border-bottom: 1px solid #e9ecef;
                }}
                .detail-row:last-child {{
                    border-bottom: none;
                }}
                .detail-label {{
                    font-weight: bold;
                    color: #333;
                }}
                .detail-value {{
                    color: #666;
                }}
                .status-badge {{
                    display: inline-block;
                    background: linear-gradient(135deg, #ffa726 0%, #ffcc02 100%);
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    font-weight: bold;
                }}
                .chat-section {{
                    border-top: 2px solid #e9ecef;
                    padding-top: 30px;
                }}
                .chat-title {{
                    font-size: 1.5rem;
                    margin-bottom: 20px;
                    color: #333;
                }}
                .chat-messages {{
                    max-height: 400px;
                    overflow-y: auto;
                    border: 2px solid #e9ecef;
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 20px;
                    background: #f8f9fa;
                }}
                .message {{
                    background: white;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 15px;
                    border-left: 4px solid #667eea;
                }}
                .message-author {{
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 5px;
                }}
                .message-time {{
                    font-size: 0.8rem;
                    color: #999;
                    margin-bottom: 10px;
                }}
                .message-text {{
                    color: #333;
                    line-height: 1.6;
                }}
                .chat-input {{
                    display: flex;
                    gap: 15px;
                }}
                .message-input {{
                    flex: 1;
                    padding: 15px;
                    border: 2px solid #e9ecef;
                    border-radius: 10px;
                    font-size: 1rem;
                }}
                .send-button {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 15px 25px;
                    border-radius: 10px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                .send-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
                }}
                .no-messages {{
                    text-align: center;
                    color: #666;
                    font-style: italic;
                    padding: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="ticket-container">
                <div class="ticket-header">
                    <h1>🎫 Trade Ticket</h1>
                    <div class="ticket-id">Ticket ID: #{ticket_id}</div>
                </div>
                
                <div class="ticket-content">
                    <div class="order-details">
                        <div class="detail-row">
                            <span class="detail-label">Token:</span>
                            <span class="detail-value">{listing.get('tokenName', 'N/A')} ({listing.get('tokenSymbol', 'N/A')})</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Blockchain:</span>
                            <span class="detail-value">{listing.get('blockchain', 'N/A')}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Order Type:</span>
                            <span class="detail-value">{ticket['orderType'].upper()}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Amount:</span>
                            <span class="detail-value">{ticket['amount']:,} tokens</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Price:</span>
                            <span class="detail-value">${ticket['price']} per token</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Total Value:</span>
                            <span class="detail-value">${ticket['amount'] * ticket['price']:,.2f}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Status:</span>
                            <span class="detail-value"><span class="status-badge">{ticket['status']}</span></span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Created:</span>
                            <span class="detail-value">{ticket['created']}</span>
                        </div>
                    </div>
                    
                    <div class="chat-section">
                        <h3 class="chat-title">💬 Communication</h3>
                        <div class="chat-messages" id="chat-messages">
                            <div class="no-messages">No messages yet. Start the conversation!</div>
                        </div>
                        <div class="chat-input">
                            <input type="text" id="message-input" class="message-input" placeholder="Type your message...">
                            <button class="send-button" onclick="sendMessage()">Send</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                const ticketId = '{ticket_id}';
                
                function sendMessage() {{
                    const input = document.getElementById('message-input');
                    const message = input.value.trim();
                    
                    if (message) {{
                        fetch('/api/send-message', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{
                                ticketId: ticketId,
                                message: message,
                                author: 'User'
                            }})
                        }})
                        .then(response => response.json())
                        .then(result => {{
                            if (result.success) {{
                                input.value = '';
                                loadMessages();
                            }}
                        }});
                    }}
                }}
                
                function loadMessages() {{
                    // In a real implementation, you'd fetch messages from the server
                    // For now, we'll simulate with local storage or keep in memory
                }}
                
                document.getElementById('message-input').addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        sendMessage();
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def create_listing(self, data):
        try:
            listing_id = str(uuid.uuid4())
            listing = {
                'id': listing_id,
                'tokenName': data.get('tokenName', ''),
                'tokenSymbol': data.get('tokenSymbol', ''),
                'blockchain': data.get('blockchain', ''),
                'priceUSD': data.get('priceUSD', 0),
                'totalSupply': data.get('totalSupply', 0),
                'launchDate': data.get('launchDate', ''),
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'active'
            }
            
            self.listings[listing_id] = listing
            
            response = {'success': True, 'listingId': listing_id}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def place_order(self, data):
        try:
            ticket_id = str(uuid.uuid4())[:8]
            order_id = str(uuid.uuid4())
            
            order = {
                'id': order_id,
                'ticketId': ticket_id,
                'listingId': data.get('listingId', ''),
                'orderType': data.get('orderType', ''),
                'amount': data.get('amount', 0),
                'price': data.get('price', 0),
                'email': data.get('email', ''),
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'pending'
            }
            
            ticket = {
                'id': ticket_id,
                'orderId': order_id,
                'listingId': data.get('listingId', ''),
                'orderType': data.get('orderType', ''),
                'amount': data.get('amount', 0),
                'price': data.get('price', 0),
                'email': data.get('email', ''),
                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'Open',
                'messages': []
            }
            
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
            
            response = {'success': True, 'ticketId': ticket_id, 'orderId': order_id}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def send_message(self, data):
        try:
            ticket_id = data.get('ticketId', '')
            if ticket_id in self.tickets:
                message = {
                    'author': data.get('author', 'User'),
                    'message': data.get('message', ''),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.tickets[ticket_id]['messages'].append(message)
                response = {'success': True}
            else:
                response = {'success': False, 'error': 'Ticket not found'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"{self.address_string()} - {format % args}")

def main():
    print("🚀 Starting PreMarket Pro Trading Platform...")
    print("✅ Multi-chain pre-market token trading")
    print("💰 Fee structure: 2-5% per trade + escrow fees")
    print("🎫 Ticket-based communication system")
    print("🌐 Supporting ETH, BSC, Polygon, and more")
    print("")
    
    server_address = ('0.0.0.0', 5000)
    httpd = HTTPServer(server_address, PreMarketTradingHandler)
    
    print(f"✅ Server running at http://localhost:5000")
    print(f"🌐 External access: Available through Replit")
    print("💡 Features:")
    print("   • Create pre-market token listings")
    print("   • Place buy/sell orders before launch") 
    print("   • Ticket-based buyer-seller communication")
    print("   • Multi-chain support (ETH/BSC/Polygon/etc)")
    print("   • Automated fee collection system")
    print("")
    print("Ready to facilitate pre-market trading! 🎯")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    main()