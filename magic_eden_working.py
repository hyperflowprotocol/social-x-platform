#!/usr/bin/env python3

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs

PORT = 5001

class HyperFlowNFTHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow NFT Marketplace - Magic Eden Style</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .hero {
            text-align: center;
            padding: 80px 0 40px 0;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        }
        
        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .btn {
            display: inline-block;
            padding: 16px 32px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 18px;
            border: none;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            padding: 60px 0;
        }
        
        .feature-card {
            background: rgba(30, 41, 59, 0.4);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid rgba(45, 212, 191, 0.1);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: rgba(45, 212, 191, 0.4);
        }
        
        .form-container {
            background: rgba(30, 41, 59, 0.4);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            color: white;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        input[type="text"],
        input[type="number"],
        input[type="file"],
        input[type="datetime-local"],
        textarea {
            width: 100%;
            padding: 16px;
            background: rgba(15, 23, 42, 0.6);
            border: 2px solid rgba(45, 212, 191, 0.2);
            border-radius: 12px;
            color: white;
            font-size: 16px;
        }
        
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .phase-section {
            border: 2px solid rgba(45, 212, 191, 0.3);
            border-radius: 16px;
            padding: 30px;
            background: rgba(45, 212, 191, 0.05);
            margin: 30px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="main-content">
            <section class="hero">
                <h1>Magic Eden Style Marketplace</h1>
                <p>Launch NFT collections on HyperEVM with advanced launchpad features</p>
                <br>
                <button class="btn" onclick="showCreateNFT()">🚀 Create NFT Collection</button>
            </section>

            <section class="features">
                <div class="feature-card">
                    <h3 style="color: #2dd4bf; margin-bottom: 15px;">NFT Launchpad</h3>
                    <p style="color: #94a3b8;">Complete collection creation with logo/banner uploads, whitelist management, and smart contract deployment</p>
                </div>
                
                <div class="feature-card">
                    <h3 style="color: #2dd4bf; margin-bottom: 15px;">HYPE Token Integration</h3>
                    <p style="color: #94a3b8;">Native HyperEVM token payments with dual pricing structure and creator royalties</p>
                </div>
                
                <div class="feature-card">
                    <h3 style="color: #2dd4bf; margin-bottom: 15px;">Phase-Based Minting</h3>
                    <p style="color: #94a3b8;">Time-controlled whitelist and public mint phases with per-wallet limits and supply allocation</p>
                </div>
            </section>
        </div>
    </div>

    <script>
        console.log('✅ Clean Magic Eden Marketplace Ready');
        
        function showCreateNFT() {
            console.log('🚀 Showing Create NFT interface...');
            document.getElementById('main-content').innerHTML = `
                <div style="padding: 40px 0;">
                    <div style="text-align: center; margin-bottom: 40px;">
                        <h1 style="font-size: 48px; margin-bottom: 20px; color: white;">🎨 NFT Collection Creator</h1>
                        <p style="font-size: 18px; color: #94a3b8;">Magic Eden-style launchpad with complete features</p>
                    </div>
                    
                    <div class="form-container">
                        <h2 style="color: #2dd4bf; margin-bottom: 30px;">Launch Your NFT Collection</h2>
                        
                        <form id="nft-launch-form" onsubmit="handleFormSubmit(event)">
                            <div class="form-group">
                                <label>Collection Name</label>
                                <input type="text" placeholder="e.g., HyperFlow Genesis" required>
                            </div>
                            
                            <div class="grid-2">
                                <div class="form-group">
                                    <label>Symbol</label>
                                    <input type="text" placeholder="e.g., HFGEN" required>
                                </div>
                                <div class="form-group">
                                    <label>Total Supply</label>
                                    <input type="number" placeholder="e.g., 10000" min="1" max="100000" required>
                                </div>
                            </div>
                            
                            <div class="grid-2">
                                <div class="form-group">
                                    <label>Whitelist Price (HYPE)</label>
                                    <input type="number" placeholder="50" step="0.1" min="0" required>
                                </div>
                                <div class="form-group">
                                    <label>Public Price (HYPE)</label>
                                    <input type="number" placeholder="80" step="0.1" min="0" required>
                                </div>
                            </div>
                            
                            <div class="grid-2">
                                <div class="form-group">
                                    <label>Collection Logo (400x400)</label>
                                    <input type="file" accept="image/*">
                                </div>
                                <div class="form-group">
                                    <label>Banner Image (1400x400)</label>
                                    <input type="file" accept="image/*">
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>Whitelist CSV File</label>
                                <input type="file" accept=".csv" onchange="handleCSVUpload(this)">
                                <div id="csv-status" style="margin-top: 8px; font-size: 14px; color: #64748b;">
                                    Format: address,maxMints (e.g., 0x123...,3)
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>Base IPFS URI</label>
                                <input type="text" placeholder="ipfs://QmYourHash/" required>
                            </div>
                            
                            <div class="form-group">
                                <label>Collection Description</label>
                                <textarea placeholder="Describe your NFT collection and its unique features..." rows="4" required></textarea>
                            </div>
                            
                            <!-- Phase Configuration -->
                            <div class="phase-section">
                                <h3 style="color: #2dd4bf; margin-bottom: 25px;">Multi-Phase Minting Configuration</h3>
                                
                                <div id="phases-container">
                                    <div class="phase-item" style="margin-bottom: 30px; padding: 20px; background: rgba(15, 23, 42, 0.3); border-radius: 12px;">
                                        <h4 style="color: #2dd4bf; margin-bottom: 20px;">Phase 1: Whitelist Mint</h4>
                                        
                                        <div class="grid-2" style="margin-bottom: 20px;">
                                            <div class="form-group">
                                                <label>Start Date & Time</label>
                                                <input type="datetime-local" required>
                                            </div>
                                            <div class="form-group">
                                                <label>End Date & Time</label>
                                                <input type="datetime-local" required>
                                            </div>
                                        </div>
                                        
                                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
                                            <div class="form-group">
                                                <label>Price (HYPE)</label>
                                                <input type="number" placeholder="50" step="0.1" min="0" required>
                                            </div>
                                            <div class="form-group">
                                                <label>Max Per Wallet</label>
                                                <input type="number" placeholder="5" min="1" max="50" value="5" required>
                                            </div>
                                            <div class="form-group">
                                                <label>Supply Allocation</label>
                                                <input type="number" placeholder="3000" min="1" required>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <button type="button" class="btn" onclick="addPhase()" style="margin-bottom: 20px;">+ Add Phase</button>
                                
                                <div style="background: rgba(45, 212, 191, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #2dd4bf;">
                                    <div style="color: #94a3b8; font-size: 14px;">
                                        Phase times are in UTC. Each phase should start after the previous one ends. Supply allocations should total your collection size.
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Fund Distribution -->
                            <div class="phase-section">
                                <h3 style="color: #2dd4bf; margin-bottom: 25px;">Fund Distribution Settings</h3>
                                
                                <div class="form-group">
                                    <label>Primary Treasury Address</label>
                                    <input type="text" placeholder="0x..." required style="font-family: monospace;">
                                    <div style="margin-top: 8px; font-size: 12px; color: #64748b;">
                                        HyperEVM wallet address where mint proceeds will be sent
                                    </div>
                                </div>
                                
                                <div class="form-group">
                                    <label>Secondary Beneficiary Address (Optional)</label>
                                    <input type="text" placeholder="0x... (optional)" style="font-family: monospace;">
                                    <div style="margin-top: 8px; font-size: 12px; color: #64748b;">
                                        Optional second wallet for revenue sharing
                                    </div>
                                </div>
                                
                                <div class="grid-2">
                                    <div class="form-group">
                                        <label>Primary Split (%)</label>
                                        <input type="number" placeholder="100" min="0" max="100" value="100" required>
                                    </div>
                                    <div class="form-group">
                                        <label>Secondary Split (%)</label>
                                        <input type="number" placeholder="0" min="0" max="100" value="0">
                                    </div>
                                </div>
                                
                                <div style="background: rgba(45, 212, 191, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #2dd4bf;">
                                    <div style="color: #94a3b8; font-size: 14px;">
                                        Revenue splits must total 100%. All HYPE tokens from mints will be automatically distributed to specified addresses.
                                    </div>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>Creator Royalty (%)</label>
                                <input type="number" placeholder="5" min="0" max="10" step="0.1" value="5" required>
                                <div style="margin-top: 8px; font-size: 12px; color: #64748b;">
                                    Percentage of secondary sales that goes to the creator
                                </div>
                            </div>
                            
                            <div style="text-align: center; padding-top: 30px;">
                                <button type="submit" class="btn">🚀 Deploy NFT Collection</button>
                                <button type="button" class="btn" onclick="showCreateNFT()" style="margin-left: 20px; background: rgba(75, 85, 99, 0.5);">← Back</button>
                            </div>
                        </form>
                    </div>
                </div>
            `;
        }
        
        function handleFormSubmit(event) {
            event.preventDefault();
            alert('🎉 NFT Collection form submitted successfully!\\n\\nReady for HyperEVM deployment with HYPE token integration.');
        }
        
        function handleCSVUpload(input) {
            const statusDiv = document.getElementById('csv-status');
            if (input.files && input.files[0]) {
                const file = input.files[0];
                if (file.name.toLowerCase().endsWith('.csv')) {
                    statusDiv.innerHTML = '✅ CSV file uploaded successfully';
                    statusDiv.style.color = '#22c55e';
                } else {
                    statusDiv.innerHTML = '❌ Please upload a .csv file';
                    statusDiv.style.color = '#ef4444';
                }
            }
        }
        
        let phaseCount = 1;
        function addPhase() {
            phaseCount++;
            const container = document.getElementById('phases-container');
            const newPhase = document.createElement('div');
            newPhase.className = 'phase-item';
            newPhase.style.cssText = 'margin-bottom: 30px; padding: 20px; background: rgba(15, 23, 42, 0.3); border-radius: 12px;';
            
            newPhase.innerHTML = '<h4 style="color: #2dd4bf; margin-bottom: 20px;">Phase ' + phaseCount + ': Public Mint <button type="button" onclick="removePhase(this)" style="float: right; background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); border-radius: 6px; padding: 8px; color: #ef4444; cursor: pointer;">Remove</button></h4>' +
                '<div class="grid-2" style="margin-bottom: 20px;">' +
                    '<div class="form-group"><label>Start Date & Time</label><input type="datetime-local" required></div>' +
                    '<div class="form-group"><label>End Date & Time</label><input type="datetime-local" required></div>' +
                '</div>' +
                '<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">' +
                    '<div class="form-group"><label>Price (HYPE)</label><input type="number" placeholder="80" step="0.1" min="0" required></div>' +
                    '<div class="form-group"><label>Max Per Wallet</label><input type="number" placeholder="10" min="1" max="100" value="10" required></div>' +
                    '<div class="form-group"><label>Supply Allocation</label><input type="number" placeholder="7000" min="1" required></div>' +
                '</div>';
            
            container.appendChild(newPhase);
        }
        
        function removePhase(button) {
            const phases = document.querySelectorAll('.phase-item');
            if (phases.length > 1) {
                button.closest('.phase-item').remove();
            } else {
                alert('At least one mint phase is required');
            }
        }
    </script>
</body>
</html>
            """
            
            self.wfile.write(html.encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    httpd = socketserver.TCPServer(("", PORT), HyperFlowNFTHandler)
    httpd.allow_reuse_address = True
    print(f"🚀 Clean HyperFlow NFT Marketplace - Magic Eden Style")
    print(f"✅ Running at http://localhost:{PORT}")
    print(f"🌐 External access: https://{PORT}-workspace-hypurrs75.replit.dev")
    print(f"✅ Clean Magic Eden Launchpad serving at port {PORT}")
    httpd.serve_forever()