#!/usr/bin/env python3
"""
🎛️ NFT Minting Admin Panel
Complete administrative control for NFT collection management
"""

import http.server
import socketserver
import json
import csv
import io
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

PORT = 5000

class NFTAdminHandler(http.server.SimpleHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        # Admin Configuration
        self.admin_config = {
            "collection_name": "HyperFlow Genesis",
            "collection_symbol": "HFGEN",
            "max_supply": 10000,
            "max_mint_per_wallet": 5,
            "contract_address": "0x...",  # Will be set after deployment
            "base_uri": "https://metadata.hyperflow.xyz/",
            
            # Pricing Configuration
            "whitelist_eth_price": 0.05,  # ETH
            "public_eth_price": 0.08,     # ETH
            "whitelist_hype_price": 100,  # HYPE tokens
            "public_hype_price": 150,     # HYPE tokens
            
            # Phase Timing (Unix timestamps)
            "whitelist_start": 0,
            "whitelist_end": 0,
            "public_start": 0,
            "public_end": 0,
            "current_phase": "CLOSED",
            
            # Fund Distribution Wallets
            "platform_wallet": "0x...",
            "creator_wallet": "0x...",
            "development_wallet": "0x...",
            
            # Statistics
            "total_minted": 0,
            "whitelist_size": 0,
            "eth_collected": 0.0,
            "hype_collected": 0.0
        }
        
        # Whitelist Management
        self.whitelist = set()
        self.mint_history = []
        
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_admin_dashboard()
        elif parsed_path.path == '/api/config':
            self.send_config_data()
        elif parsed_path.path == '/api/whitelist':
            self.send_whitelist_data()
        elif parsed_path.path == '/api/mint-history':
            self.send_mint_history()
        elif parsed_path.path == '/api/phase-info':
            self.send_phase_info()
        else:
            super().do_GET()
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            if parsed_path.path == '/api/set-phases':
                self.handle_set_phases(json.loads(post_data))
            elif parsed_path.path == '/api/add-whitelist':
                self.handle_add_whitelist(json.loads(post_data))
            elif parsed_path.path == '/api/upload-csv':
                self.handle_csv_upload(post_data)
            elif parsed_path.path == '/api/set-phase':
                self.handle_set_phase(json.loads(post_data))
            elif parsed_path.path == '/api/update-config':
                self.handle_update_config(json.loads(post_data))
            elif parsed_path.path == '/api/emergency-pause':
                self.handle_emergency_pause()
            else:
                self.send_error_response("Invalid endpoint")
        except Exception as e:
            self.send_error_response(f"Error: {str(e)}")
    
    def send_admin_dashboard(self):
        """Send the main admin dashboard HTML"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>NFT Minting Admin Panel</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: white;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                
                .header h1 {{
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                    background: linear-gradient(45deg, #FFD700, #FFA500);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }}
                
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                
                .stat-card {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                
                .stat-card h3 {{
                    font-size: 0.9rem;
                    margin-bottom: 10px;
                    opacity: 0.8;
                }}
                
                .stat-card .value {{
                    font-size: 2rem;
                    font-weight: bold;
                    color: #FFD700;
                }}
                
                .admin-section {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 20px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                
                .admin-section h2 {{
                    margin-bottom: 20px;
                    color: #FFD700;
                    border-bottom: 2px solid rgba(255, 215, 0, 0.3);
                    padding-bottom: 10px;
                }}
                
                .form-group {{
                    margin-bottom: 15px;
                }}
                
                .form-group label {{
                    display: block;
                    margin-bottom: 5px;
                    font-weight: 500;
                }}
                
                .form-group input, .form-group select {{
                    width: 100%;
                    padding: 10px;
                    border: none;
                    border-radius: 8px;
                    background: rgba(255, 255, 255, 0.9);
                    color: #333;
                    font-size: 14px;
                }}
                
                .form-row {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                }}
                
                .btn {{
                    background: linear-gradient(45deg, #4CAF50, #45a049);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 500;
                    transition: transform 0.2s;
                }}
                
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                }}
                
                .btn-danger {{
                    background: linear-gradient(45deg, #f44336, #d32f2f);
                }}
                
                .btn-warning {{
                    background: linear-gradient(45deg, #ff9800, #f57c00);
                }}
                
                .btn-primary {{
                    background: linear-gradient(45deg, #2196F3, #1976D2);
                }}
                
                .phase-controls {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 10px;
                    margin-bottom: 20px;
                }}
                
                .current-phase {{
                    text-align: center;
                    padding: 15px;
                    border-radius: 10px;
                    font-size: 1.2rem;
                    font-weight: bold;
                    margin-bottom: 20px;
                }}
                
                .phase-closed {{ background: linear-gradient(45deg, #9E9E9E, #757575); }}
                .phase-whitelist {{ background: linear-gradient(45deg, #FF9800, #F57C00); }}
                .phase-public {{ background: linear-gradient(45deg, #4CAF50, #388E3C); }}
                
                .csv-upload {{
                    border: 2px dashed rgba(255, 255, 255, 0.3);
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 15px;
                    cursor: pointer;
                    transition: border-color 0.3s;
                }}
                
                .csv-upload:hover {{
                    border-color: rgba(255, 255, 255, 0.6);
                }}
                
                .csv-upload input[type="file"] {{
                    display: none;
                }}
                
                .whitelist-count {{
                    background: rgba(76, 175, 80, 0.2);
                    padding: 10px;
                    border-radius: 8px;
                    text-align: center;
                    margin-top: 10px;
                }}
                
                @media (max-width: 768px) {{
                    .form-row {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .stats-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎛️ NFT Minting Admin Panel</h1>
                    <p>Complete control over your NFT collection phases, pricing, and whitelist</p>
                </div>
                
                <!-- Live Statistics -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total Minted</h3>
                        <div class="value" id="totalMinted">{self.admin_config['total_minted']}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Whitelist Size</h3>
                        <div class="value" id="whitelistSize">{len(self.whitelist)}</div>
                    </div>
                    <div class="stat-card">
                        <h3>ETH Collected</h3>
                        <div class="value" id="ethCollected">{self.admin_config['eth_collected']:.2f}</div>
                    </div>
                    <div class="stat-card">
                        <h3>HYPE Collected</h3>
                        <div class="value" id="hypeCollected">{self.admin_config['hype_collected']:.0f}</div>
                    </div>
                </div>
                
                <!-- Current Phase Status -->
                <div class="current-phase phase-{self.admin_config['current_phase'].lower()}" id="currentPhase">
                    Current Phase: {self.admin_config['current_phase']}
                </div>
                
                <!-- Phase Management -->
                <div class="admin-section">
                    <h2>⏰ Phase Management</h2>
                    <div class="phase-controls">
                        <button class="btn btn-danger" onclick="setPhase('CLOSED')">🔒 Close Minting</button>
                        <button class="btn btn-warning" onclick="setPhase('WHITELIST')">🎫 Start Whitelist</button>
                        <button class="btn btn-primary" onclick="setPhase('PUBLIC')">🌍 Start Public</button>
                        <button class="btn btn-danger" onclick="emergencyPause()">⛔ Emergency Pause</button>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Whitelist Start Time</label>
                            <input type="datetime-local" id="whitelistStart" 
                                   value="{self.format_datetime_for_input(self.admin_config['whitelist_start'])}">
                        </div>
                        <div class="form-group">
                            <label>Whitelist End Time</label>
                            <input type="datetime-local" id="whitelistEnd"
                                   value="{self.format_datetime_for_input(self.admin_config['whitelist_end'])}">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Public Start Time</label>
                            <input type="datetime-local" id="publicStart"
                                   value="{self.format_datetime_for_input(self.admin_config['public_start'])}">
                        </div>
                        <div class="form-group">
                            <label>Public End Time</label>
                            <input type="datetime-local" id="publicEnd"
                                   value="{self.format_datetime_for_input(self.admin_config['public_end'])}">
                        </div>
                    </div>
                    
                    <button class="btn btn-primary" onclick="updatePhases()">💾 Update Phase Times</button>
                </div>
                
                <!-- Whitelist Management -->
                <div class="admin-section">
                    <h2>📋 Whitelist Management</h2>
                    
                    <!-- CSV Upload -->
                    <div class="csv-upload" onclick="document.getElementById('csvFile').click()">
                        <input type="file" id="csvFile" accept=".csv" onchange="uploadCSV()">
                        <p>📁 Click to Upload CSV Whitelist</p>
                        <small>Format: One wallet address per line</small>
                    </div>
                    
                    <!-- Manual Add -->
                    <div class="form-group">
                        <label>Add Single Wallet Address</label>
                        <input type="text" id="singleWallet" placeholder="0x..." maxlength="42">
                    </div>
                    <button class="btn btn-primary" onclick="addSingleWallet()">➕ Add to Whitelist</button>
                    
                    <div class="whitelist-count">
                        <strong>Current Whitelist: <span id="whitelistCount">{len(self.whitelist)}</span> addresses</strong>
                    </div>
                </div>
                
                <!-- Pricing Configuration -->
                <div class="admin-section">
                    <h2>💰 Pricing Configuration</h2>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Whitelist ETH Price</label>
                            <input type="number" id="whitelistEthPrice" step="0.001" 
                                   value="{self.admin_config['whitelist_eth_price']}" min="0">
                        </div>
                        <div class="form-group">
                            <label>Public ETH Price</label>
                            <input type="number" id="publicEthPrice" step="0.001" 
                                   value="{self.admin_config['public_eth_price']}" min="0">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Whitelist HYPE Price</label>
                            <input type="number" id="whitelistHypePrice" 
                                   value="{self.admin_config['whitelist_hype_price']}" min="0">
                        </div>
                        <div class="form-group">
                            <label>Public HYPE Price</label>
                            <input type="number" id="publicHypePrice" 
                                   value="{self.admin_config['public_hype_price']}" min="0">
                        </div>
                    </div>
                    
                    <button class="btn btn-primary" onclick="updatePricing()">💾 Update Pricing</button>
                </div>
                
                <!-- Collection Settings -->
                <div class="admin-section">
                    <h2>⚙️ Collection Settings</h2>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Collection Name</label>
                            <input type="text" id="collectionName" value="{self.admin_config['collection_name']}">
                        </div>
                        <div class="form-group">
                            <label>Symbol</label>
                            <input type="text" id="collectionSymbol" value="{self.admin_config['collection_symbol']}">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Max Supply</label>
                            <input type="number" id="maxSupply" value="{self.admin_config['max_supply']}" min="1">
                        </div>
                        <div class="form-group">
                            <label>Max Mint Per Wallet</label>
                            <input type="number" id="maxMintPerWallet" value="{self.admin_config['max_mint_per_wallet']}" min="1">
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Base Metadata URI</label>
                        <input type="url" id="baseUri" value="{self.admin_config['base_uri']}">
                    </div>
                    
                    <button class="btn btn-primary" onclick="updateCollectionSettings()">💾 Update Collection</button>
                </div>
            </div>
            
            <script>
                // Phase Management
                function setPhase(phase) {{
                    fetch('/api/set-phase', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{phase: phase}})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        alert(data.message);
                        if (data.success) location.reload();
                    }});
                }}
                
                function updatePhases() {{
                    const phases = {{
                        whitelist_start: new Date(document.getElementById('whitelistStart').value).getTime() / 1000,
                        whitelist_end: new Date(document.getElementById('whitelistEnd').value).getTime() / 1000,
                        public_start: new Date(document.getElementById('publicStart').value).getTime() / 1000,
                        public_end: new Date(document.getElementById('publicEnd').value).getTime() / 1000
                    }};
                    
                    fetch('/api/set-phases', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify(phases)
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        alert(data.message);
                        if (data.success) location.reload();
                    }});
                }}
                
                // Whitelist Management
                function uploadCSV() {{
                    const file = document.getElementById('csvFile').files[0];
                    if (!file) return;
                    
                    const formData = new FormData();
                    formData.append('csv', file);
                    
                    fetch('/api/upload-csv', {{
                        method: 'POST',
                        body: formData
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        alert(data.message);
                        if (data.success) {{
                            document.getElementById('whitelistCount').textContent = data.total_count;
                            document.getElementById('whitelistSize').textContent = data.total_count;
                        }}
                    }});
                }}
                
                function addSingleWallet() {{
                    const wallet = document.getElementById('singleWallet').value.trim();
                    if (!wallet) return;
                    
                    fetch('/api/add-whitelist', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{address: wallet}})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        alert(data.message);
                        if (data.success) {{
                            document.getElementById('singleWallet').value = '';
                            document.getElementById('whitelistCount').textContent = data.total_count;
                            document.getElementById('whitelistSize').textContent = data.total_count;
                        }}
                    }});
                }}
                
                // Configuration Updates
                function updatePricing() {{
                    const pricing = {{
                        whitelist_eth_price: parseFloat(document.getElementById('whitelistEthPrice').value),
                        public_eth_price: parseFloat(document.getElementById('publicEthPrice').value),
                        whitelist_hype_price: parseInt(document.getElementById('whitelistHypePrice').value),
                        public_hype_price: parseInt(document.getElementById('publicHypePrice').value)
                    }};
                    
                    fetch('/api/update-config', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{type: 'pricing', data: pricing}})
                    }})
                    .then(response => response.json())
                    .then(data => alert(data.message));
                }}
                
                function updateCollectionSettings() {{
                    const settings = {{
                        collection_name: document.getElementById('collectionName').value,
                        collection_symbol: document.getElementById('collectionSymbol').value,
                        max_supply: parseInt(document.getElementById('maxSupply').value),
                        max_mint_per_wallet: parseInt(document.getElementById('maxMintPerWallet').value),
                        base_uri: document.getElementById('baseUri').value
                    }};
                    
                    fetch('/api/update-config', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{type: 'collection', data: settings}})
                    }})
                    .then(response => response.json())
                    .then(data => alert(data.message));
                }}
                
                function emergencyPause() {{
                    if (confirm('Emergency pause will immediately stop all minting. Continue?')) {{
                        fetch('/api/emergency-pause', {{method: 'POST'}})
                        .then(response => response.json())
                        .then(data => {{
                            alert(data.message);
                            if (data.success) location.reload();
                        }});
                    }}
                }}
                
                // Auto-refresh statistics every 30 seconds
                setInterval(() => {{
                    fetch('/api/config')
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('totalMinted').textContent = data.total_minted;
                        document.getElementById('ethCollected').textContent = data.eth_collected.toFixed(2);
                        document.getElementById('hypeCollected').textContent = data.hype_collected.toFixed(0);
                    }});
                }}, 30000);
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_set_phases(self, data):
        """Set whitelist and public phase times"""
        try:
            # Validate timestamps
            whitelist_start = int(data['whitelist_start'])
            whitelist_end = int(data['whitelist_end'])
            public_start = int(data['public_start'])
            public_end = int(data['public_end'])
            
            current_time = int(time.time())
            
            # Validation
            if whitelist_start <= current_time:
                raise ValueError("Whitelist start must be in the future")
            if whitelist_end <= whitelist_start:
                raise ValueError("Whitelist end must be after start")
            if public_start <= whitelist_end:
                raise ValueError("Public must start after whitelist ends")
            if public_end <= public_start:
                raise ValueError("Public end must be after start")
            
            # Update configuration
            self.admin_config.update({
                'whitelist_start': whitelist_start,
                'whitelist_end': whitelist_end,
                'public_start': public_start,
                'public_end': public_end
            })
            
            # Auto-update current phase based on times
            self.update_current_phase()
            
            self.send_json_response({
                "success": True,
                "message": "Phase times updated successfully!"
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "message": f"Error updating phases: {str(e)}"
            })
    
    def handle_set_phase(self, data):
        """Manually set the current phase"""
        try:
            phase = data['phase'].upper()
            if phase not in ['CLOSED', 'WHITELIST', 'PUBLIC']:
                raise ValueError("Invalid phase")
            
            self.admin_config['current_phase'] = phase
            
            self.send_json_response({
                "success": True,
                "message": f"Phase set to {phase}"
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "message": f"Error setting phase: {str(e)}"
            })
    
    def handle_add_whitelist(self, data):
        """Add single wallet to whitelist"""
        try:
            address = data['address'].strip().lower()
            
            # Basic validation
            if not address.startswith('0x') or len(address) != 42:
                raise ValueError("Invalid wallet address format")
            
            if address in self.whitelist:
                raise ValueError("Address already whitelisted")
            
            self.whitelist.add(address)
            
            self.send_json_response({
                "success": True,
                "message": "Address added to whitelist",
                "total_count": len(self.whitelist)
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "message": f"Error adding to whitelist: {str(e)}"
            })
    
    def handle_csv_upload(self, post_data):
        """Handle CSV upload for bulk whitelist"""
        try:
            # Parse multipart form data (simplified)
            content_type = self.headers.get('Content-Type', '')
            if 'boundary=' not in content_type:
                raise ValueError("Invalid multipart form data")
            boundary = content_type.split('boundary=')[1]
            parts = post_data.split(f'--{boundary}'.encode())
            
            csv_content = None
            for part in parts:
                if b'filename=' in part and b'.csv' in part:
                    # Extract CSV content
                    content_start = part.find(b'\r\n\r\n') + 4
                    if content_start > 3:
                        csv_content = part[content_start:].decode('utf-8').strip()
                        break
            
            if not csv_content:
                raise ValueError("No CSV content found")
            
            # Parse CSV addresses
            csv_file = io.StringIO(csv_content)
            csv_reader = csv.reader(csv_file)
            
            added_count = 0
            invalid_count = 0
            
            for row in csv_reader:
                if row and len(row) > 0:
                    address = row[0].strip().lower()
                    
                    # Validate address
                    if address.startswith('0x') and len(address) == 42:
                        if address not in self.whitelist:
                            self.whitelist.add(address)
                            added_count += 1
                    else:
                        invalid_count += 1
            
            message = f"Added {added_count} addresses to whitelist"
            if invalid_count > 0:
                message += f" ({invalid_count} invalid addresses skipped)"
            
            self.send_json_response({
                "success": True,
                "message": message,
                "added_count": added_count,
                "invalid_count": invalid_count,
                "total_count": len(self.whitelist)
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "message": f"CSV upload error: {str(e)}"
            })
    
    def handle_update_config(self, data):
        """Update configuration settings"""
        try:
            config_type = data['type']
            config_data = data['data']
            
            if config_type == 'pricing':
                self.admin_config.update({
                    'whitelist_eth_price': config_data['whitelist_eth_price'],
                    'public_eth_price': config_data['public_eth_price'],
                    'whitelist_hype_price': config_data['whitelist_hype_price'],
                    'public_hype_price': config_data['public_hype_price']
                })
                message = "Pricing updated successfully"
                
            elif config_type == 'collection':
                self.admin_config.update({
                    'collection_name': config_data['collection_name'],
                    'collection_symbol': config_data['collection_symbol'],
                    'max_supply': config_data['max_supply'],
                    'max_mint_per_wallet': config_data['max_mint_per_wallet'],
                    'base_uri': config_data['base_uri']
                })
                message = "Collection settings updated successfully"
                
            else:
                raise ValueError("Invalid configuration type")
            
            self.send_json_response({
                "success": True,
                "message": message
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "message": f"Configuration update error: {str(e)}"
            })
    
    def handle_emergency_pause(self):
        """Emergency pause all minting"""
        try:
            self.admin_config['current_phase'] = 'CLOSED'
            
            self.send_json_response({
                "success": True,
                "message": "🚨 EMERGENCY PAUSE ACTIVATED - All minting stopped"
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "message": f"Emergency pause error: {str(e)}"
            })
    
    def send_config_data(self):
        """Send current configuration"""
        self.send_json_response(self.admin_config)
    
    def send_whitelist_data(self):
        """Send whitelist data"""
        self.send_json_response({
            "whitelist": list(self.whitelist),
            "count": len(self.whitelist)
        })
    
    def send_mint_history(self):
        """Send mint history"""
        self.send_json_response({
            "history": self.mint_history[-50],  # Last 50 mints
            "total": len(self.mint_history)
        })
    
    def send_phase_info(self):
        """Send current phase information"""
        current_time = int(time.time())
        self.update_current_phase()
        
        phase_info = {
            "current_phase": self.admin_config['current_phase'],
            "current_time": current_time,
            "whitelist_start": self.admin_config['whitelist_start'],
            "whitelist_end": self.admin_config['whitelist_end'],
            "public_start": self.admin_config['public_start'],
            "public_end": self.admin_config['public_end'],
            "time_until_next_phase": self.get_time_until_next_phase()
        }
        
        self.send_json_response(phase_info)
    
    def update_current_phase(self):
        """Update current phase based on timestamps"""
        current_time = int(time.time())
        
        if (self.admin_config['whitelist_start'] <= current_time <= self.admin_config['whitelist_end']):
            self.admin_config['current_phase'] = 'WHITELIST'
        elif (self.admin_config['public_start'] <= current_time <= self.admin_config['public_end']):
            self.admin_config['current_phase'] = 'PUBLIC'
        else:
            self.admin_config['current_phase'] = 'CLOSED'
    
    def get_time_until_next_phase(self):
        """Calculate time until next phase starts"""
        current_time = int(time.time())
        
        if current_time < self.admin_config['whitelist_start']:
            return self.admin_config['whitelist_start'] - current_time
        elif current_time < self.admin_config['public_start']:
            return self.admin_config['public_start'] - current_time
        else:
            return 0
    
    def format_datetime_for_input(self, timestamp):
        """Format timestamp for HTML datetime-local input"""
        if timestamp == 0:
            return ""
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M')
    
    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, message):
        """Send error response"""
        self.send_json_response({
            "success": False,
            "error": message
        })

if __name__ == "__main__":
    print("🎛️ Starting NFT Minting Admin Panel...")
    print(f"🌐 Admin Dashboard: http://localhost:{PORT}")
    print("\n📋 Admin Features Available:")
    print("  ⏰ Set mint phase times (whitelist & public)")
    print("  🎫 Upload CSV whitelist (bulk import)")
    print("  💰 Configure pricing (ETH & HYPE tokens)")
    print("  📊 Live statistics & mint tracking")
    print("  🚨 Emergency pause controls")
    print("  ⚙️ Collection settings management")
    
    try:
        with socketserver.TCPServer(("", PORT), NFTAdminHandler) as httpd:
            print(f"\n✅ Admin panel serving at port {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⚠️ Admin panel stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting admin panel: {e}")