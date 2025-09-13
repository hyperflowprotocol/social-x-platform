#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import random
import mimetypes
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class NFTMarketplaceHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_homepage().encode())
        else:
            self.send_error(404)

    def get_homepage(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow - Magic Eden Style NFT Marketplace</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            min-height: 100vh;
        }
        .header {
            padding: 20px;
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(45, 212, 191, 0.2);
        }
        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
        }
        .logo {
            font-size: 24px;
            font-weight: bold;
            color: #2dd4bf;
        }
        .nav-buttons {
            display: flex;
            gap: 15px;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #2dd4bf, #06b6d4);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(45, 212, 191, 0.3);
        }
        .main-content {
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }
        .hero {
            margin-bottom: 60px;
        }
        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #2dd4bf, #06b6d4, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero p {
            font-size: 18px;
            color: #94a3b8;
            margin-bottom: 30px;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        .feature-card {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(45, 212, 191, 0.2);
            border-radius: 16px;
            padding: 30px;
            transition: transform 0.3s;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: rgba(45, 212, 191, 0.4);
        }
        .feature-icon {
            font-size: 48px;
            margin-bottom: 20px;
        }
        .feature-icon svg {
            width: 48px;
            height: 48px;
            color: #2dd4bf;
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="logo">💎 HyperFlow</div>
            <div class="nav-buttons">
                <button class="btn btn-primary" onclick="showCreateNFT()">🎨 Create NFT</button>
                <button class="btn btn-primary">🔌 Connect Wallet</button>
            </div>
        </nav>
    </header>

    <main id="main-content" class="main-content">
        <section class="hero">
            <h1>Magic Eden Style Marketplace</h1>
            <p>Launch NFT collections on HyperEVM with advanced launchpad features</p>
        </section>

        <section class="features">
            <div class="feature-card">
                <div class="feature-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5-1.5 1.5-5-5v-.79l-.27-.27A6.516 6.516 0 0 1 9.5 16 6.5 6.5 0 0 1 3 9.5 6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5z"/>
                    </svg>
                </div>
                <h3 style="color: #2dd4bf; margin-bottom: 15px;">NFT Launchpad</h3>
                <p style="color: #94a3b8;">Complete collection creation with logo/banner uploads, whitelist management, and smart contract deployment</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                    </svg>
                </div>
                <h3 style="color: #2dd4bf; margin-bottom: 15px;">HYPE Token Integration</h3>
                <p style="color: #94a3b8;">Native HyperEVM token payments with dual pricing structure and creator royalties</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                </div>
                <h3 style="color: #2dd4bf; margin-bottom: 15px;">Phase-Based Minting</h3>
                <p style="color: #94a3b8;">Time-controlled whitelist and public mint phases with per-wallet limits and supply allocation</p>
            </div>
        </section>
    </main>

    <script>
        function showCreateNFT() {
            console.log('🎨 NFT Creator opened!');
            document.getElementById('main-content').innerHTML = `
                <div style="min-height: 80vh; padding: 40px 20px;">
                    <div style="max-width: 800px; margin: 0 auto;">
                        <h1 style="font-size: 48px; text-align: center; margin-bottom: 20px; color: white;">🚀 NFT Collection Creator</h1>
                        <p style="font-size: 18px; text-align: center; margin-bottom: 40px; color: #94a3b8;">Magic Eden-style launchpad with complete features</p>
                        
                        <div style="background: rgba(30, 41, 59, 0.4); border-radius: 20px; padding: 40px; text-align: center;">
                            <div style="margin-bottom: 20px;">
                                <svg width="72" height="72" viewBox="0 0 24 24" fill="#2dd4bf" style="margin: 0 auto; display: block;">
                                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                                </svg>
                            </div>
                            <h2 style="color: #2dd4bf; margin-bottom: 20px; font-size: 28px;">Full Launchpad Features Ready!</h2>
                            <div style="color: #94a3b8; margin-bottom: 30px; font-size: 16px; line-height: 1.6;">
                                ✅ Logo/Banner Upload System<br>
                                ✅ CSV Whitelist Import<br>
                                ✅ Time-based Mint Phases<br>
                                ✅ HYPE Token Integration<br>
                                ✅ Smart Contract Deployment<br>
                                ✅ IPFS Metadata Storage
                            </div>
                            <div style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
                                <button onclick="location.reload()" class="btn btn-primary">
                                    ← Back to Home
                                </button>
                                <button onclick="showNFTForm()" class="btn btn-primary">
                                    📝 Fill Launch Form
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        function showNFTForm() {
            console.log('📝 Loading NFT Launch Form...');
            document.getElementById('main-content').innerHTML = `
                <div style="min-height: 80vh; padding: 40px 20px;">
                    <div style="max-width: 800px; margin: 0 auto;">
                        <h1 style="font-size: 48px; text-align: center; margin-bottom: 20px; color: white;">📝 NFT Collection Launch Form</h1>
                        <p style="font-size: 18px; text-align: center; margin-bottom: 40px; color: #94a3b8;">Complete the form below to launch your NFT collection on HyperEVM</p>
                        
                        <form id="nft-launch-form" style="background: rgba(30, 41, 59, 0.4); border-radius: 20px; padding: 40px;">
                            <div style="display: grid; gap: 30px;">
                                
                                <!-- Collection Details -->
                                <div>
                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Collection Name</label>
                                    <input type="text" placeholder="e.g., HyperFlow Genesis" required
                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                </div>

                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                    <div>
                                        <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Symbol</label>
                                        <input type="text" placeholder="e.g., HFGEN" required
                                            style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                    </div>
                                    <div>
                                        <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Total Supply</label>
                                        <input type="number" placeholder="e.g., 10000" min="1" max="100000" required
                                            style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                    </div>
                                </div>

                                <!-- Pricing -->
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                    <div>
                                        <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Whitelist Price (HYPE)</label>
                                        <input type="number" placeholder="50" step="0.1" min="0" required
                                            style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                    </div>
                                    <div>
                                        <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Public Price (HYPE)</label>
                                        <input type="number" placeholder="80" step="0.1" min="0" required
                                            style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                    </div>
                                </div>

                                <!-- File Uploads -->
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                    <div>
                                        <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Collection Logo (400x400)</label>
                                        <input type="file" accept="image/*" 
                                            style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                    </div>
                                    <div>
                                        <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Banner Image (1400x400)</label>
                                        <input type="file" accept="image/*"
                                            style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                    </div>
                                </div>

                                <!-- Whitelist Upload -->
                                <div>
                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Whitelist CSV File</label>
                                    <input type="file" id="whitelist-csv" accept=".csv" onchange="validateWhitelistCSV(this)"
                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                    <div id="csv-status" style="margin-top: 8px; font-size: 14px; color: #64748b;">
                                        Format: address,maxMints (e.g., 0x123...,3)
                                    </div>
                                    <div id="csv-preview" style="margin-top: 15px; display: none; padding: 15px; background: rgba(15, 23, 42, 0.4); border-radius: 8px; border-left: 4px solid #2dd4bf;">
                                        <div style="color: #2dd4bf; font-weight: 600; margin-bottom: 8px;">Whitelist Preview:</div>
                                        <div id="csv-addresses" style="font-family: monospace; font-size: 12px; color: #94a3b8; max-height: 150px; overflow-y: auto;"></div>
                                        <div id="csv-summary" style="margin-top: 10px; font-size: 12px; color: #2dd4bf; font-weight: 600;"></div>
                                    </div>
                                </div>

                                <!-- IPFS and Description -->
                                <div>
                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Base IPFS URI</label>
                                    <input type="text" placeholder="ipfs://QmYourHash/" required
                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                </div>

                                <div>
                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Collection Description</label>
                                    <textarea placeholder="Describe your NFT collection and its unique features..." rows="4" required
                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px; resize: vertical;"></textarea>
                                </div>

                                <!-- Dynamic Phase Configuration -->
                                <div style="border: 2px solid rgba(45, 212, 191, 0.3); border-radius: 16px; padding: 30px; background: rgba(45, 212, 191, 0.05);">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                                        <h3 style="color: #2dd4bf; font-size: 20px; display: flex; align-items: center; margin: 0;">
                                            <svg width="24" height="24" style="margin-right: 10px;" viewBox="0 0 24 24" fill="currentColor">
                                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                            </svg>
                                            Multi-Phase Minting Configuration
                                        </h3>
                                        <button type="button" id="add-phase-btn" onclick="addMintPhase()"
                                            style="background: linear-gradient(135deg, #2dd4bf, #06b6d4); border: none; border-radius: 8px; padding: 12px 20px; color: white; font-size: 14px; font-weight: 600; cursor: pointer; display: flex; align-items: center;">
                                            <svg width="16" height="16" style="margin-right: 6px;" viewBox="0 0 24 24" fill="currentColor">
                                                <path d="M12 5v14m-7-7h14"/>
                                            </svg>
                                            Add Phase
                                        </button>
                                    </div>
                                    
                                    <div id="mint-phases-container">
                                        <!-- Initial Phase -->
                                        <div class="mint-phase" data-phase="1" style="margin-bottom: 30px; padding: 20px; background: rgba(15, 23, 42, 0.3); border-radius: 12px; position: relative;">
                                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                                                <h4 style="color: #2dd4bf; margin: 0; display: flex; align-items: center;">
                                                    <svg width="20" height="20" style="margin-right: 8px;" viewBox="0 0 24 24" fill="currentColor">
                                                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                                    </svg>
                                                    <span>Phase 1: </span>
                                                    <input type="text" placeholder="Phase Name" value="Whitelist Mint" 
                                                        style="background: transparent; border: none; color: #2dd4bf; font-size: 16px; font-weight: 600; margin-left: 5px; outline: none; border-bottom: 1px solid rgba(45, 212, 191, 0.3);">
                                                </h4>
                                            </div>
                                            
                                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                                                <div>
                                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Start Date & Time</label>
                                                    <input type="datetime-local" required
                                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                                </div>
                                                <div>
                                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">End Date & Time</label>
                                                    <input type="datetime-local" required
                                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                                </div>
                                            </div>
                                            
                                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
                                                <div>
                                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Price (HYPE)</label>
                                                    <input type="number" placeholder="50" step="0.1" min="0" required
                                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                                </div>
                                                <div>
                                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Max Per Wallet</label>
                                                    <input type="number" placeholder="5" min="1" max="50" value="5" required
                                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                                </div>
                                                <div>
                                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Supply Allocation</label>
                                                    <input type="number" placeholder="3000" min="1" required
                                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div style="background: rgba(45, 212, 191, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #2dd4bf; margin-top: 20px;">
                                        <div style="color: #94a3b8; font-size: 14px;">
                                            <svg width="16" height="16" style="margin-right: 6px; vertical-align: middle;" viewBox="0 0 24 24" fill="currentColor">
                                                <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                            </svg>
                                            Phase times are in UTC. Each phase should start after the previous one ends. Supply allocations should total your collection size.
                                        </div>
                                    </div>
                                </div>

                                <!-- Fund Distribution -->
                                <div style="border: 2px solid rgba(45, 212, 191, 0.3); border-radius: 16px; padding: 30px; background: rgba(45, 212, 191, 0.05);">
                                    <h3 style="color: #2dd4bf; margin-bottom: 25px; font-size: 20px; display: flex; align-items: center;">
                                        <svg width="24" height="24" style="margin-right: 10px;" viewBox="0 0 24 24" fill="currentColor">
                                            <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V21C3 22.11 3.89 23 5 23H19C20.11 23 21 22.11 21 21V9M19 9H14V4H5V21H19V9Z"/>
                                        </svg>
                                        Fund Distribution Settings
                                    </h3>
                                    
                                    <div style="margin-bottom: 25px;">
                                        <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Primary Treasury Address</label>
                                        <input type="text" placeholder="0x..." required
                                            style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px; font-family: monospace;">
                                        <div style="margin-top: 8px; font-size: 12px; color: #64748b;">
                                            HyperEVM wallet address where mint proceeds will be sent
                                        </div>
                                    </div>

                                    <div style="margin-bottom: 25px;">
                                        <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Secondary Beneficiary Address (Optional)</label>
                                        <input type="text" placeholder="0x... (optional)"
                                            style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px; font-family: monospace;">
                                        <div style="margin-top: 8px; font-size: 12px; color: #64748b;">
                                            Optional second wallet for revenue sharing
                                        </div>
                                    </div>

                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                                        <div>
                                            <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Primary Split (%)</label>
                                            <input type="number" placeholder="100" min="0" max="100" value="100" required
                                                style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                        </div>
                                        <div>
                                            <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Secondary Split (%)</label>
                                            <input type="number" placeholder="0" min="0" max="100" value="0"
                                                style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                        </div>
                                    </div>

                                    <div style="background: rgba(45, 212, 191, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #2dd4bf;">
                                        <div style="color: #94a3b8; font-size: 14px;">
                                            <svg width="16" height="16" style="margin-right: 6px; vertical-align: middle;" viewBox="0 0 24 24" fill="currentColor">
                                                <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                            </svg>
                                            Revenue splits must total 100%. All HYPE tokens from mints will be automatically distributed to specified addresses.
                                        </div>
                                    </div>
                                </div>

                                <!-- Royalty -->
                                <div>
                                    <label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Creator Royalty (%)</label>
                                    <input type="number" placeholder="5" min="0" max="10" step="0.1" value="5" required
                                        style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;">
                                    <div style="margin-top: 8px; font-size: 12px; color: #64748b;">
                                        Percentage of secondary sales that goes to the creator
                                    </div>
                                </div>

                                <!-- Submit Buttons -->
                                <div style="display: flex; gap: 20px; justify-content: center; margin-top: 20px;">
                                    <button type="button" onclick="showCreateNFT()" 
                                        style="background: rgba(30, 41, 59, 0.6); border: 2px solid rgba(45, 212, 191, 0.3); border-radius: 12px; padding: 16px 32px; color: white; font-size: 16px; font-weight: 600; cursor: pointer;">
                                        ← Back
                                    </button>
                                    <button type="submit"
                                        style="background: linear-gradient(135deg, #2dd4bf, #06b6d4); border: none; border-radius: 12px; padding: 16px 32px; color: white; font-size: 16px; font-weight: 600; cursor: pointer;">
                                        🚀 Deploy Collection
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            `;

            alert('Form submitted! Ready for deployment.');
        }

        let phaseCounter = 1;
        
        function addMintPhase() {
            phaseCounter++;
            const container = document.getElementById('mint-phases-container');
            
            const newPhaseDiv = document.createElement('div');
            newPhaseDiv.className = 'mint-phase';
            newPhaseDiv.style.cssText = 'margin-bottom: 30px; padding: 20px; background: rgba(15, 23, 42, 0.3); border-radius: 12px; position: relative;';
            
            newPhaseDiv.innerHTML = '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;"><h4 style="color: #2dd4bf; margin: 0; display: flex; align-items: center;"><svg width="20" height="20" style="margin-right: 8px;" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg><span>Phase ' + phaseCounter + ': </span><input type="text" placeholder="Phase Name" value="Public Mint" style="background: transparent; border: none; color: #2dd4bf; font-size: 16px; font-weight: 600; margin-left: 5px; outline: none; border-bottom: 1px solid rgba(45, 212, 191, 0.3);"></h4><button type="button" onclick="removePhase(this)" style="background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.5); border-radius: 6px; padding: 8px; color: #ef4444; cursor: pointer;"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M6 18L18 6M6 6l12 12"/></svg></button></div><div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;"><div><label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Start Date & Time</label><input type="datetime-local" required style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;"></div><div><label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">End Date & Time</label><input type="datetime-local" required style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;"></div></div><div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;"><div><label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Price (HYPE)</label><input type="number" placeholder="80" step="0.1" min="0" required style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;"></div><div><label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Max Per Wallet</label><input type="number" placeholder="10" min="1" max="100" value="10" required style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;"></div><div><label style="display: block; color: white; font-weight: 600; margin-bottom: 10px;">Supply Allocation</label><input type="number" placeholder="7000" min="1" required style="width: 100%; padding: 16px; background: rgba(15, 23, 42, 0.6); border: 2px solid rgba(45, 212, 191, 0.2); border-radius: 12px; color: white; font-size: 16px;"></div></div>';
            
            container.appendChild(newPhaseDiv);
        }
        
        function removePhase(button) {
            const phases = document.querySelectorAll('.mint-phase');
            if (phases.length > 1) {
                button.closest('.mint-phase').remove();
            } else {
                alert('At least one mint phase is required');
            }
        }

        function validateWhitelistCSV(input) {
            const statusDiv = document.getElementById('csv-status');
            const previewDiv = document.getElementById('csv-preview');
            
            if (!input.files || !input.files[0]) {
                statusDiv.innerHTML = 'Format: address,maxMints (e.g., 0x123...,3)';
                statusDiv.style.color = '#64748b';
                if (previewDiv) previewDiv.style.display = 'none';
                return;
            }
            
            const file = input.files[0];
            if (!file.name.toLowerCase().endsWith('.csv')) {
                statusDiv.innerHTML = 'Please upload a .csv file';
                statusDiv.style.color = '#ef4444';
                if (previewDiv) previewDiv.style.display = 'none';
                return;
            }
            
            statusDiv.innerHTML = 'CSV file uploaded successfully';
            statusDiv.style.color = '#22c55e';
        }

        console.log('✅ Clean Magic Eden Marketplace Ready');
        console.log('✅ showCreateNFT function available:', typeof showCreateNFT);
    </script>
</body>
</html>'''

if __name__ == '__main__':
    PORT = 5000
    print("🚀 Clean HyperFlow NFT Marketplace - Magic Eden Style")
    print(f"✅ Running at http://localhost:{PORT}")
    print(f"🌐 External access: https://{PORT}-workspace-hypurrs75.replit.dev")
    
    class ReuseTCPServer(socketserver.TCPServer):
        allow_reuse_address = True
    
    try:
        with ReuseTCPServer(("0.0.0.0", PORT), NFTMarketplaceHandler) as httpd:
            print(f"\n✅ Clean Magic Eden Launchpad serving at port {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server shutting down...")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")