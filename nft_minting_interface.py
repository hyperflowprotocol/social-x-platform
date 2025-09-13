#!/usr/bin/env python3
"""
🎯 NFT Minting Interface for Users
Complete Web3 minting experience with IPFS metadata integration
"""

import http.server
import socketserver
import json
import time
import hashlib
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs

PORT = 5001

class NFTMintingHandler(http.server.SimpleHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        # NFT Collection Configuration
        self.collection_config = {
            "name": "HyperFlow Genesis",
            "symbol": "HFGEN",
            "description": "First-ever NFT collection on HyperFlow SocialFi platform with exclusive utilities and community access",
            "max_supply": 10000,
            "max_mint_per_wallet": 5,
            
            # Contract Addresses (will be deployed)
            "nft_contract": "0x742d35Cc6084f4056B5A4c0A4aB3e4a4f6e3B8d1",  # Example address
            "hype_token": "0x4Ed7c70F96B99c776995fB64377f0d4aB3B389A0",     # HYPE token
            
            # IPFS Configuration
            "base_ipfs_uri": "ipfs://QmYx6GsYAKnNzZ9A6NvETC4WiNj8VxzhMHdRKx5YdrAnC6/",
            "contract_uri": "ipfs://QmContract123.../collection.json",
            
            # Current Pricing (HYPE is native currency on HyperEVM)
            "whitelist_hype_price": 50,
            "public_hype_price": 80,
            "whitelist_hype_token_price": 50,
            "public_hype_token_price": 80,
            
            # Current Phase Info
            "current_phase": "WHITELIST",  # CLOSED, WHITELIST, PUBLIC
            "whitelist_start": int(time.time()) - 3600,  # Started 1 hour ago
            "whitelist_end": int(time.time()) + 82800,   # Ends in 23 hours  
            "public_start": int(time.time()) + 86400,    # Starts in 24 hours
            "public_end": int(time.time()) + 259200,     # Ends in 72 hours
            
            # Live Statistics
            "total_minted": 1247,
            "remaining_supply": 8753,
            "whitelist_size": 2340,
            "holders_count": 892
        }
        
        # Sample IPFS Metadata Structure
        self.sample_metadata = {
            "name": "HyperFlow Genesis #1",
            "description": "A unique collectible from the HyperFlow Genesis collection with exclusive SocialFi utilities",
            "image": "ipfs://QmYx6GsYAKnNzZ9A6NvETC4WiNj8VxzhMHdRKx5YdrAnC6/1.png",
            "external_url": "https://hyperflow.xyz/nft/1",
            "attributes": [
                {"trait_type": "Background", "value": "Cyber Blue"},
                {"trait_type": "Character", "value": "Genesis Warrior"},
                {"trait_type": "Rarity", "value": "Legendary"},
                {"trait_type": "Power Level", "value": 95},
                {"trait_type": "Social Score", "value": "9.2/10"}
            ],
            "properties": {
                "category": "Character",
                "creators": [{"address": "0x...", "share": 100}]
            }
        }
        
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.send_minting_page()
        elif parsed_path.path == '/api/collection-info':
            self.send_collection_info()
        elif parsed_path.path == '/api/mint-eligibility':
            self.send_mint_eligibility(parse_qs(parsed_path.query))
        elif parsed_path.path == '/api/phase-status':
            self.send_phase_status()
        elif parsed_path.path.startswith('/api/metadata/'):
            token_id = parsed_path.path.split('/')[-1]
            self.send_nft_metadata(token_id)
        else:
            super().do_GET()
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            if parsed_path.path == '/api/simulate-mint':
                self.handle_simulate_mint(json.loads(post_data))
            elif parsed_path.path == '/api/check-whitelist':
                self.handle_check_whitelist(json.loads(post_data))
            else:
                self.send_error_response("Invalid endpoint")
        except Exception as e:
            self.send_error_response(f"Error: {str(e)}")
    
    def send_minting_page(self):
        """Send the main NFT minting interface"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.collection_config['name']} - Mint NFT</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #2d1b69 100%);
                    min-height: 100vh;
                    color: white;
                    overflow-x: hidden;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                .hero-section {{
                    text-align: center;
                    padding: 60px 0;
                    position: relative;
                }}
                
                .hero-section h1 {{
                    font-size: 3.5rem;
                    margin-bottom: 20px;
                    background: linear-gradient(45deg, #FFD700, #FF6B35, #F7931E);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    animation: glow 2s ease-in-out infinite alternate;
                }}
                
                @keyframes glow {{
                    from {{ text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }}
                    to {{ text-shadow: 0 0 30px rgba(255, 215, 0, 0.8); }}
                }}
                
                .collection-preview {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 40px;
                    margin: 40px 0;
                    align-items: center;
                }}
                
                .preview-nft {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 20px;
                    padding: 20px;
                    backdrop-filter: blur(10px);
                    border: 2px solid rgba(255, 215, 0, 0.3);
                    transform: perspective(1000px) rotateY(-5deg);
                    transition: transform 0.3s ease;
                }}
                
                .preview-nft:hover {{
                    transform: perspective(1000px) rotateY(0deg) scale(1.02);
                }}
                
                .nft-image {{
                    width: 100%;
                    height: 300px;
                    background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
                    border-radius: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 3rem;
                    margin-bottom: 15px;
                    position: relative;
                    overflow: hidden;
                }}
                
                .nft-image::before {{
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(%23grid)"/></svg>');
                }}
                
                .nft-info {{
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 10px;
                    padding: 15px;
                    margin-top: 10px;
                }}
                
                .mint-interface {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 20px;
                    padding: 30px;
                    backdrop-filter: blur(10px);
                    border: 2px solid rgba(255, 215, 0, 0.3);
                }}
                
                .phase-indicator {{
                    text-align: center;
                    padding: 15px;
                    border-radius: 15px;
                    margin-bottom: 25px;
                    font-size: 1.2rem;
                    font-weight: bold;
                }}
                
                .phase-whitelist {{
                    background: linear-gradient(45deg, #FF6B35, #F7931E);
                    animation: pulse 2s infinite;
                }}
                
                .phase-public {{
                    background: linear-gradient(45deg, #4CAF50, #45a049);
                }}
                
                .phase-closed {{
                    background: linear-gradient(45deg, #9E9E9E, #757575);
                }}
                
                @keyframes pulse {{
                    0% {{ box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.7); }}
                    70% {{ box-shadow: 0 0 0 10px rgba(255, 107, 53, 0); }}
                    100% {{ box-shadow: 0 0 0 0 rgba(255, 107, 53, 0); }}
                }}
                
                .countdown {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 10px;
                    margin: 20px 0;
                }}
                
                .countdown-item {{
                    text-align: center;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 10px;
                }}
                
                .countdown-number {{
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #FFD700;
                }}
                
                .quantity-selector {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 15px;
                    margin: 20px 0;
                }}
                
                .quantity-btn {{
                    width: 40px;
                    height: 40px;
                    border: none;
                    border-radius: 50%;
                    background: linear-gradient(45deg, #FF6B35, #F7931E);
                    color: white;
                    font-size: 1.2rem;
                    cursor: pointer;
                    transition: transform 0.2s;
                }}
                
                .quantity-btn:hover {{
                    transform: scale(1.1);
                }}
                
                .quantity-display {{
                    font-size: 2rem;
                    font-weight: bold;
                    color: #FFD700;
                    min-width: 60px;
                    text-align: center;
                }}
                
                .pricing-options {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin: 20px 0;
                }}
                
                .price-option {{
                    background: rgba(255, 255, 255, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    padding: 20px;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                
                .price-option.selected {{
                    border-color: #FFD700;
                    background: rgba(255, 215, 0, 0.1);
                    transform: scale(1.02);
                }}
                
                .price-option:hover {{
                    border-color: #FFD700;
                }}
                
                .mint-button {{
                    width: 100%;
                    padding: 20px;
                    border: none;
                    border-radius: 15px;
                    background: linear-gradient(45deg, #FF6B35, #F7931E, #FFD700);
                    color: white;
                    font-size: 1.3rem;
                    font-weight: bold;
                    cursor: pointer;
                    transition: transform 0.3s ease;
                    position: relative;
                    overflow: hidden;
                }}
                
                .mint-button:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 10px 20px rgba(255, 107, 53, 0.3);
                }}
                
                .mint-button:disabled {{
                    background: #666;
                    cursor: not-allowed;
                    transform: none;
                }}
                
                .collection-stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 15px;
                    margin: 30px 0;
                }}
                
                .stat-item {{
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 15px;
                    text-align: center;
                }}
                
                .stat-value {{
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #FFD700;
                }}
                
                .stat-label {{
                    font-size: 0.9rem;
                    opacity: 0.8;
                    margin-top: 5px;
                }}
                
                .wallet-connection {{
                    text-align: center;
                    margin: 20px 0;
                }}
                
                .connect-wallet-btn {{
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 10px;
                    font-size: 1.1rem;
                    cursor: pointer;
                    transition: transform 0.2s;
                }}
                
                .connect-wallet-btn:hover {{
                    transform: scale(1.05);
                }}
                
                .connected-wallet {{
                    background: rgba(76, 175, 80, 0.2);
                    border: 2px solid #4CAF50;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                }}
                
                .ipfs-info {{
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 15px;
                    padding: 20px;
                    margin: 20px 0;
                    border-left: 4px solid #FFD700;
                }}
                
                .how-it-works {{
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 15px;
                    padding: 25px;
                    margin: 30px 0;
                }}
                
                .step {{
                    display: flex;
                    align-items: center;
                    margin: 15px 0;
                    padding: 15px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                }}
                
                .step-number {{
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background: linear-gradient(45deg, #FF6B35, #F7931E);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    margin-right: 15px;
                }}
                
                @media (max-width: 768px) {{
                    .collection-preview {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .hero-section h1 {{
                        font-size: 2.5rem;
                    }}
                    
                    .pricing-options {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Hero Section -->
                <div class="hero-section">
                    <h1>{self.collection_config['name']}</h1>
                    <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 20px;">
                        {self.collection_config['description']}
                    </p>
                </div>
                
                <!-- Collection Preview -->
                <div class="collection-preview">
                    <div class="preview-nft">
                        <div class="nft-image">
                            🎨
                        </div>
                        <div class="nft-info">
                            <h3>Preview: Genesis Warrior #1</h3>
                            <p>Each NFT is stored on IPFS with unique metadata</p>
                            <div style="margin-top: 10px;">
                                <strong>IPFS URI:</strong><br>
                                <code style="font-size: 0.8rem; background: rgba(0,0,0,0.3); padding: 5px; border-radius: 5px;">
                                    {self.collection_config['base_ipfs_uri']}1.json
                                </code>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mint-interface">
                        <!-- Phase Status -->
                        <div class="phase-indicator phase-{self.collection_config['current_phase'].lower()}" id="phaseIndicator">
                            🎫 WHITELIST PHASE ACTIVE
                        </div>
                        
                        <!-- Countdown Timer -->
                        <div class="countdown" id="countdown">
                            <div class="countdown-item">
                                <div class="countdown-number" id="hours">23</div>
                                <div>Hours</div>
                            </div>
                            <div class="countdown-item">
                                <div class="countdown-number" id="minutes">45</div>
                                <div>Minutes</div>
                            </div>
                            <div class="countdown-item">
                                <div class="countdown-number" id="seconds">30</div>
                                <div>Seconds</div>
                            </div>
                            <div class="countdown-item">
                                <div class="countdown-number" id="remaining">{self.collection_config['remaining_supply']}</div>
                                <div>Left</div>
                            </div>
                        </div>
                        
                        <!-- Wallet Connection -->
                        <div class="wallet-connection" id="walletSection">
                            <button class="connect-wallet-btn" onclick="connectWallet()">
                                🔗 Connect Wallet
                            </button>
                        </div>
                        
                        <!-- Mint Quantity -->
                        <div class="quantity-selector">
                            <button class="quantity-btn" onclick="changeQuantity(-1)">-</button>
                            <div class="quantity-display" id="quantity">1</div>
                            <button class="quantity-btn" onclick="changeQuantity(1)">+</button>
                        </div>
                        
                        <!-- Pricing Options -->
                        <div class="pricing-options">
                            <div class="price-option selected" onclick="selectPayment('hype')" id="hypeOption">
                                <h3>💎 Pay with HYPE (Native)</h3>
                                <div class="stat-value" id="hypePrice">{self.collection_config['whitelist_hype_price']} HYPE</div>
                                <div>HyperEVM Native Currency</div>
                            </div>
                            <div class="price-option" onclick="selectPayment('hype_token')" id="hypeTokenOption">
                                <h3>🪙 Pay with HYPE Token</h3>
                                <div class="stat-value" id="hypeTokenPrice">{self.collection_config['whitelist_hype_token_price']} HYPE</div>
                                <div>ERC20 Token Version</div>
                            </div>
                        </div>
                        
                        <!-- Mint Button -->
                        <button class="mint-button" onclick="mintNFT()" id="mintButton" disabled>
                            🎯 Connect Wallet to Mint
                        </button>
                    </div>
                </div>
                
                <!-- Collection Stats -->
                <div class="collection-stats">
                    <div class="stat-item">
                        <div class="stat-value">{self.collection_config['total_minted']:,}</div>
                        <div class="stat-label">Minted</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{self.collection_config['max_supply']:,}</div>
                        <div class="stat-label">Total Supply</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{self.collection_config['whitelist_size']:,}</div>
                        <div class="stat-label">Whitelisted</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{self.collection_config['holders_count']:,}</div>
                        <div class="stat-label">Holders</div>
                    </div>
                </div>
                
                <!-- IPFS & Technical Info -->
                <div class="ipfs-info">
                    <h3>🌐 IPFS Integration</h3>
                    <p><strong>How it works:</strong> Your NFT metadata and images are permanently stored on IPFS (InterPlanetary File System), ensuring true ownership and decentralization.</p>
                    <br>
                    <p><strong>Base IPFS URI:</strong> <code>{self.collection_config['base_ipfs_uri']}</code></p>
                    <p><strong>Contract Address:</strong> <code>{self.collection_config['nft_contract']}</code></p>
                    <p><strong>HYPE Token:</strong> <code>{self.collection_config['hype_token']}</code></p>
                </div>
                
                <!-- How It Works -->
                <div class="how-it-works">
                    <h3>🚀 How Minting Works</h3>
                    <div class="step">
                        <div class="step-number">1</div>
                        <div>
                            <strong>Connect Wallet:</strong> Connect your Web3 wallet (MetaMask, WalletConnect, etc.)
                        </div>
                    </div>
                    <div class="step">
                        <div class="step-number">2</div>
                        <div>
                            <strong>Check Eligibility:</strong> Verify you're whitelisted (if in whitelist phase) and have sufficient funds
                        </div>
                    </div>
                    <div class="step">
                        <div class="step-number">3</div>
                        <div>
                            <strong>Select Quantity:</strong> Choose how many NFTs to mint (max {self.collection_config['max_mint_per_wallet']} per wallet)
                        </div>
                    </div>
                    <div class="step">
                        <div class="step-number">4</div>
                        <div>
                            <strong>Pay & Mint:</strong> Transaction calls smart contract → Contract assigns token ID → IPFS metadata linked
                        </div>
                    </div>
                    <div class="step">
                        <div class="step-number">5</div>
                        <div>
                            <strong>Receive NFT:</strong> Your unique NFT appears in wallet with metadata from IPFS
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                let currentQuantity = 1;
                let selectedPayment = 'hype';
                let walletConnected = false;
                let userAddress = null;
                
                // Wallet Connection Simulation
                async function connectWallet() {{
                    try {{
                        // Simulate wallet connection
                        setTimeout(() => {{
                            walletConnected = true;
                            userAddress = '0x742d35Cc6084f4056B5A4c0A4aB3e4a4f6e3B8d1';
                            updateWalletUI();
                        }}, 1000);
                    }} catch (error) {{
                        alert('Failed to connect wallet: ' + error.message);
                    }}
                }}
                
                function updateWalletUI() {{
                    const walletSection = document.getElementById('walletSection');
                    if (walletConnected) {{
                        walletSection.innerHTML = `
                            <div class="connected-wallet">
                                ✅ Connected: ${{userAddress.slice(0, 6)}}...${{userAddress.slice(-4)}}
                                <br><small>HyperEVM Network</small>
                            </div>
                        `;
                        document.getElementById('mintButton').disabled = false;
                        updateMintButton();
                    }}
                }}
                
                function changeQuantity(delta) {{
                    const newQuantity = currentQuantity + delta;
                    if (newQuantity >= 1 && newQuantity <= {self.collection_config['max_mint_per_wallet']}) {{
                        currentQuantity = newQuantity;
                        document.getElementById('quantity').textContent = currentQuantity;
                        updateMintButton();
                    }}
                }}
                
                function selectPayment(type) {{
                    selectedPayment = type;
                    
                    // Update UI
                    document.getElementById('hypeOption').classList.toggle('selected', type === 'hype');
                    document.getElementById('hypeTokenOption').classList.toggle('selected', type === 'hype_token');
                    
                    updateMintButton();
                }}
                
                function updateMintButton() {{
                    const button = document.getElementById('mintButton');
                    if (!walletConnected) {{
                        button.textContent = '🔗 Connect Wallet to Mint';
                        button.disabled = true;
                        return;
                    }}
                    
                    const currentPhase = '{self.collection_config['current_phase']}';
                    let price, symbol;
                    
                    if (selectedPayment === 'hype') {{
                        price = currentPhase === 'WHITELIST' ? {self.collection_config['whitelist_hype_price']} : {self.collection_config['public_hype_price']};
                        symbol = 'HYPE';
                    }} else {{
                        price = currentPhase === 'WHITELIST' ? {self.collection_config['whitelist_hype_token_price']} : {self.collection_config['public_hype_token_price']};
                        symbol = 'HYPE';
                    }}
                    
                    const totalPrice = (price * currentQuantity).toFixed(selectedPayment === 'eth' ? 3 : 0);
                    button.textContent = `🎯 Mint ${{currentQuantity}} NFT${{currentQuantity > 1 ? 's' : ''}} for ${{totalPrice}} ${{symbol}}`;
                    button.disabled = false;
                }}
                
                async function mintNFT() {{
                    if (!walletConnected) {{
                        alert('Please connect your wallet first');
                        return;
                    }}
                    
                    try {{
                        const button = document.getElementById('mintButton');
                        button.disabled = true;
                        button.textContent = '⏳ Minting in progress...';
                        
                        // Simulate minting process
                        setTimeout(() => {{
                            alert(`🎉 Successfully minted ${{currentQuantity}} NFT${{currentQuantity > 1 ? 's' : ''}}!\\n\\nYour NFTs will appear in your wallet shortly.\\nMetadata stored on IPFS: {self.collection_config['base_ipfs_uri']}`);
                            button.disabled = false;
                            updateMintButton();
                        }}, 3000);
                        
                    }} catch (error) {{
                        alert('Minting failed: ' + error.message);
                        document.getElementById('mintButton').disabled = false;
                        updateMintButton();
                    }}
                }}
                
                // Countdown Timer
                function updateCountdown() {{
                    const now = Math.floor(Date.now() / 1000);
                    const endTime = {self.collection_config['whitelist_end']};
                    const timeLeft = endTime - now;
                    
                    if (timeLeft > 0) {{
                        const hours = Math.floor(timeLeft / 3600);
                        const minutes = Math.floor((timeLeft % 3600) / 60);
                        const seconds = timeLeft % 60;
                        
                        document.getElementById('hours').textContent = hours;
                        document.getElementById('minutes').textContent = minutes;
                        document.getElementById('seconds').textContent = seconds;
                    }} else {{
                        document.getElementById('phaseIndicator').textContent = '🌍 PUBLIC PHASE ACTIVE';
                        document.getElementById('phaseIndicator').className = 'phase-indicator phase-public';
                    }}
                }}
                
                // Update countdown every second
                setInterval(updateCountdown, 1000);
                updateCountdown();
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_nft_metadata(self, token_id):
        """Return IPFS-style metadata for a specific token"""
        try:
            token_id = int(token_id)
            
            # Generate unique metadata based on token ID
            metadata = {
                "name": f"{self.collection_config['name']} #{token_id}",
                "description": self.sample_metadata["description"],
                "image": f"{self.collection_config['base_ipfs_uri']}{token_id}.png",
                "external_url": f"https://hyperflow.xyz/nft/{token_id}",
                "attributes": self.generate_random_attributes(token_id),
                "properties": {
                    "category": "Character",
                    "creators": [{"address": self.collection_config['nft_contract'], "share": 100}]
                }
            }
            
            self.send_json_response(metadata)
            
        except Exception as e:
            self.send_error_response(f"Invalid token ID: {str(e)}")
    
    def generate_random_attributes(self, token_id):
        """Generate random but deterministic attributes based on token ID"""
        random.seed(token_id)
        
        backgrounds = ["Cyber Blue", "Neon Purple", "Golden Aura", "Digital Red", "Cosmic Black"]
        characters = ["Genesis Warrior", "Cyber Knight", "Digital Mage", "Tech Samurai", "Code Master"]
        rarities = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
        
        # Rarity distribution
        rarity_weights = [0.4, 0.3, 0.2, 0.07, 0.03]
        rarity = random.choices(rarities, weights=rarity_weights)[0]
        
        return [
            {"trait_type": "Background", "value": random.choice(backgrounds)},
            {"trait_type": "Character", "value": random.choice(characters)},
            {"trait_type": "Rarity", "value": rarity},
            {"trait_type": "Power Level", "value": random.randint(1, 100)},
            {"trait_type": "Social Score", "value": f"{random.randint(10, 100)/10:.1f}/10"},
            {"trait_type": "Generation", "value": "Genesis"},
            {"trait_type": "Element", "value": random.choice(["Fire", "Water", "Earth", "Air", "Digital"])}
        ]
    
    def send_collection_info(self):
        """Send collection configuration and statistics"""
        self.send_json_response(self.collection_config)
    
    def send_phase_status(self):
        """Send current phase status and timing"""
        current_time = int(time.time())
        
        phase_info = {
            "current_phase": self.collection_config['current_phase'],
            "current_time": current_time,
            "whitelist_start": self.collection_config['whitelist_start'],
            "whitelist_end": self.collection_config['whitelist_end'],
            "public_start": self.collection_config['public_start'],
            "public_end": self.collection_config['public_end'],
            "time_remaining": self.collection_config['whitelist_end'] - current_time
        }
        
        self.send_json_response(phase_info)
    
    def send_mint_eligibility(self, query_params):
        """Check mint eligibility for a wallet address"""
        address = query_params.get('address', [''])[0]
        
        if not address:
            self.send_error_response("Address parameter required")
            return
        
        # Simulate eligibility check
        eligibility = {
            "address": address,
            "is_whitelisted": True,  # Simulate whitelist status
            "minted_count": 0,       # How many already minted
            "max_mint": self.collection_config['max_mint_per_wallet'],
            "can_mint": True,
            "current_phase": self.collection_config['current_phase'],
            "eth_balance": 1.5,      # Simulated ETH balance
            "hype_balance": 500      # Simulated HYPE balance
        }
        
        self.send_json_response(eligibility)
    
    def handle_simulate_mint(self, data):
        """Simulate the minting process"""
        try:
            quantity = data.get('quantity', 1)
            payment_type = data.get('payment_type', 'eth')
            address = data.get('address', '')
            
            if not address:
                raise ValueError("Wallet address required")
            
            if quantity < 1 or quantity > self.collection_config['max_mint_per_wallet']:
                raise ValueError(f"Invalid quantity. Max {self.collection_config['max_mint_per_wallet']} per wallet")
            
            # Calculate pricing
            if self.collection_config['current_phase'] == 'WHITELIST':
                eth_price = self.collection_config['whitelist_eth_price']
                hype_price = self.collection_config['whitelist_hype_price']
            else:
                eth_price = self.collection_config['public_eth_price'] 
                hype_price = self.collection_config['public_hype_price']
            
            total_cost = (eth_price if payment_type == 'eth' else hype_price) * quantity
            
            # Simulate successful mint
            self.send_json_response({
                "success": True,
                "message": f"Successfully minted {quantity} NFT(s)",
                "transaction_hash": f"0x{hashlib.md5(f'{address}{quantity}{time.time()}'.encode()).hexdigest()}",
                "token_ids": list(range(self.collection_config['total_minted'] + 1, 
                                       self.collection_config['total_minted'] + quantity + 1)),
                "total_cost": total_cost,
                "payment_type": payment_type,
                "ipfs_metadata": [f"{self.collection_config['base_ipfs_uri']}{i}.json" 
                                 for i in range(self.collection_config['total_minted'] + 1, 
                                               self.collection_config['total_minted'] + quantity + 1)]
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "error": str(e)
            })
    
    def handle_check_whitelist(self, data):
        """Check if address is whitelisted"""
        try:
            address = data.get('address', '').lower()
            
            if not address:
                raise ValueError("Address required")
            
            # Simulate whitelist check (in reality, this would query the smart contract)
            is_whitelisted = address.startswith('0x7') or address.startswith('0x4')  # Simulate some being whitelisted
            
            self.send_json_response({
                "address": address,
                "is_whitelisted": is_whitelisted,
                "message": "Whitelisted! You can mint during whitelist phase." if is_whitelisted else "Not whitelisted. Wait for public phase."
            })
            
        except Exception as e:
            self.send_json_response({
                "success": False,
                "error": str(e)
            })
    
    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_error_response(self, message):
        """Send error response"""
        self.send_json_response({
            "success": False,
            "error": message
        })

if __name__ == "__main__":
    print("🎯 Starting NFT Minting Interface...")
    print(f"🌐 Minting Page: http://localhost:{PORT}")
    print("\n🚀 Features Available:")
    print("  🎫 Phase-based minting (Whitelist → Public)")
    print("  💰 Dual payment options (ETH & HYPE tokens)")
    print("  🌐 IPFS metadata integration")
    print("  📱 Mobile-responsive design")
    print("  ⏱️ Live countdown timers")
    print("  🔗 Web3 wallet connection")
    
    print("\n📋 IPFS Integration Flow:")
    print("  1. Metadata uploaded to IPFS before launch")
    print("  2. Smart contract stores base IPFS URI")
    print("  3. User mints → Contract assigns token ID")
    print("  4. tokenURI() = baseURI + tokenID + '.json'")
    print("  5. NFT displays with IPFS metadata")
    
    try:
        import socket
        class ReuseTCPServer(socketserver.TCPServer):
            def server_bind(self):
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.socket.bind(self.server_address)
        
        with ReuseTCPServer(("0.0.0.0", PORT), NFTMintingHandler) as httpd:
            print(f"\n✅ NFT minting interface serving at port {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⚠️ Minting interface stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting minting interface: {e}")