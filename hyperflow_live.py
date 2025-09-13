#!/usr/bin/env python3

import http.server
import socketserver
import json
import random
import time
import threading

PORT = 5002

# Real-time data simulation
protocol_data = {
    'tvl': 2_450_000,
    'flow_price': 0.0125,
    'users': 2_847,
    'revenue': 85_000,
    'vaults': [
        {'name': 'Delta Neutral Vault', 'apy': 12.5, 'tvl': 620000, 'users': 189},
        {'name': 'Yield Optimizer', 'apy': 15.2, 'tvl': 890000, 'users': 245},
        {'name': 'Cross-Protocol Aggregator', 'apy': 9.8, 'tvl': 430000, 'users': 156},
        {'name': 'Risk Parity Strategy', 'apy': 11.3, 'tvl': 510000, 'users': 178}
    ]
}

def update_data():
    """Simulate real-time data updates"""
    while True:
        # Update TVL with small fluctuations
        protocol_data['tvl'] += random.randint(-5000, 15000)
        protocol_data['tvl'] = max(2_000_000, protocol_data['tvl'])
        
        # Update FLOW price
        protocol_data['flow_price'] += random.uniform(-0.0002, 0.0003)
        protocol_data['flow_price'] = max(0.01, protocol_data['flow_price'])
        
        # Update users count
        if random.random() < 0.3:  # 30% chance to add new user
            protocol_data['users'] += random.randint(1, 3)
        
        # Update vault data
        for vault in protocol_data['vaults']:
            vault['tvl'] += random.randint(-2000, 8000)
            vault['tvl'] = max(100000, vault['tvl'])
            vault['apy'] += random.uniform(-0.1, 0.1)
            vault['apy'] = max(5.0, min(20.0, vault['apy']))
        
        time.sleep(2)  # Update every 2 seconds

# Start background data updater
data_thread = threading.Thread(target=update_data, daemon=True)
data_thread.start()

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
        else:
            super().do_GET()

    def get_main_page(self):
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, shrink-to-fit=no, viewport-fit=cover">
    <title>HyperFlow Protocol - Live DeFi Infrastructure</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        html, body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; 
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); 
            color: white; 
            min-height: 100vh;
            overflow-x: hidden;
            width: 100%;
            max-width: 100vw;
            position: relative;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            -khtml-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            /* Fix blurry rendering on mobile */
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
            transform: translateZ(0);
            -webkit-transform: translateZ(0);
        }
        
        /* Fix viewport issues on mobile */
        @media (max-width: 768px) {
            html {
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
                font-size: 16px; /* Prevent zoom on input focus */
            }
            
            body {
                -webkit-overflow-scrolling: touch;
                position: relative;
                /* Prevent blurry rendering */
                image-rendering: crisp-edges;
                image-rendering: -webkit-crisp-edges;
                image-rendering: -moz-crisp-edges;
                image-rendering: -o-crisp-edges;
            }
            
            /* Ensure all elements are hardware accelerated */
            * {
                -webkit-transform: translateZ(0);
                transform: translateZ(0);
                -webkit-backface-visibility: hidden;
                backface-visibility: hidden;
            }
        }
        
        /* Animated background particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        
        .particle {
            position: absolute;
            background: #2dd4bf;
            border-radius: 50%;
            opacity: 0.1;
            animation: float 20s infinite linear;
        }
        
        @keyframes float {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 0.1; }
            90% { opacity: 0.1; }
            100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
        }
        
        .app { 
            display: flex; 
            min-height: 100vh; 
            position: relative;
            z-index: 2;
            width: 100%;
            max-width: 100vw;
            overflow-x: hidden;
        }
        
        .sidebar { 
            width: 280px; 
            background: rgba(30,41,59,0.95); 
            padding: 2rem 1.5rem; 
            border-right: 1px solid rgba(45,212,191,0.3);
            backdrop-filter: blur(10px);
        }
        
        .logo { 
            font-size: 1.5rem; 
            font-weight: 700; 
            color: #2dd4bf; 
            margin-bottom: 2rem; 
            text-align: center;
            padding: 1rem;
            background: linear-gradient(135deg, rgba(45,212,191,0.1), rgba(20,184,166,0.1));
            border-radius: 12px;
            border: 1px solid rgba(45,212,191,0.2);
        }
        
        .nav { list-style: none; }
        .nav-item { margin-bottom: 0.5rem; }
        .nav-link { 
            display: flex; 
            align-items: center; 
            padding: 1rem 1.25rem; 
            color: #94a3b8; 
            cursor: pointer; 
            border-radius: 8px; 
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .nav-link::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(45,212,191,0.1), transparent);
            transition: left 0.5s;
        }
        
        .nav-link:hover::before { left: 100%; }
        .nav-link:hover { 
            background: rgba(45,212,191,0.1); 
            color: #2dd4bf; 
            transform: translateX(5px);
        }
        .nav-link.active { 
            background: linear-gradient(135deg, #2dd4bf, #14b8a6); 
            color: #0f172a; 
            font-weight: 600;
        }
        .nav-link svg { margin-right: 0.75rem; transition: all 0.3s ease; }
        
        .main { 
            flex: 1; 
            padding: 2rem; 
            width: 100%;
            min-width: 0;
            overflow-x: hidden;
        }
        .page { display: none; }
        .page.active { display: block; animation: fadeIn 0.5s ease-in; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 1.5rem; 
            margin-bottom: 2rem;
            width: 100%;
            overflow-x: hidden;
        }
        
        .stat-card { 
            background: rgba(30,41,59,0.8); 
            padding: 1.5rem; 
            border-radius: 12px; 
            border: 1px solid rgba(45,212,191,0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #2dd4bf, #14b8a6, #0d9488);
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { opacity: 0.5; }
            to { opacity: 1; }
        }
        
        .stat-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 10px 30px rgba(45,212,191,0.2);
        }
        
        .stat-label { color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem; }
        .stat-value { 
            font-size: 2rem; 
            font-weight: 700; 
            color: #2dd4bf; 
            transition: all 0.3s ease;
        }
        .stat-change { 
            font-size: 0.8rem; 
            color: #10b981; 
            margin-top: 0.25rem;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.7; }
            50% { opacity: 1; }
        }
        
        .vaults { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 1.5rem;
            width: 100%;
            overflow-x: hidden;
        }
        
        .vault-card { 
            background: rgba(30,41,59,0.8); 
            padding: 1.5rem; 
            border-radius: 12px; 
            border: 1px solid rgba(45,212,191,0.2);
            transition: all 0.3s ease;
        }
        
        .vault-card:hover { 
            transform: translateY(-3px); 
            border-color: #2dd4bf;
            box-shadow: 0 8px 25px rgba(45,212,191,0.15);
        }
        
        .vault-name { 
            font-size: 1.2rem; 
            font-weight: 600; 
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .vault-apy { 
            color: #10b981; 
            font-size: 1.1rem; 
            font-weight: 700;
            animation: countUp 0.5s ease-out;
        }
        
        @keyframes countUp {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        
        .vault-desc { color: #94a3b8; margin-bottom: 1rem; line-height: 1.5; }
        
        .vault-metrics {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .metric {
            text-align: center;
            padding: 0.75rem;
            background: rgba(15,23,42,0.6);
            border-radius: 8px;
            border: 1px solid rgba(45,212,191,0.1);
        }
        
        .metric-label { 
            color: #64748b; 
            font-size: 0.8rem; 
            margin-bottom: 0.25rem; 
        }
        
        .metric-value { 
            color: #2dd4bf; 
            font-weight: 600; 
            font-size: 1rem;
        }
        
        .vault-actions { 
            display: flex; 
            gap: 1rem; 
        }
        
        .vault-btn { 
            flex: 1; 
            padding: 0.875rem 1.5rem; 
            border: 1px solid rgba(45,212,191,0.4); 
            background: transparent; 
            color: #2dd4bf; 
            border-radius: 8px; 
            cursor: pointer; 
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .vault-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(45,212,191,0.1), transparent);
            transition: left 0.5s;
        }
        
        .vault-btn:hover::before { left: 100%; }
        .vault-btn:hover { 
            background: rgba(45,212,191,0.1); 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(45,212,191,0.2);
        }
        
        .vault-btn.primary { 
            background: linear-gradient(135deg, #2dd4bf, #14b8a6); 
            color: #0f172a; 
            border: none;
            font-weight: 600;
        }
        
        .vault-btn.primary:hover { 
            background: linear-gradient(135deg, #14b8a6, #0d9488); 
        }
        
        .form-container { 
            max-width: 500px; 
            margin: 0 auto; 
            background: rgba(30,41,59,0.9); 
            padding: 2.5rem; 
            border-radius: 16px; 
            border: 1px solid rgba(45,212,191,0.3);
            backdrop-filter: blur(10px);
        }
        
        .form-group { margin-bottom: 1.5rem; }
        .form-label { 
            display: block; 
            color: #94a3b8; 
            margin-bottom: 0.75rem; 
            font-weight: 500;
        }
        
        .form-input, .form-select { 
            width: 100%; 
            padding: 1rem 1.25rem; 
            background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(30,41,59,0.6)); 
            border: 1px solid rgba(45,212,191,0.4); 
            border-radius: 10px; 
            color: white; 
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .form-input:focus, .form-select:focus {
            outline: none;
            border-color: #2dd4bf;
            box-shadow: 0 0 0 3px rgba(45,212,191,0.1);
            background: linear-gradient(135deg, rgba(15,23,42,1), rgba(30,41,59,0.8));
        }
        
        .form-select {
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23ffffff' viewBox='0 0 24 24'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 1rem center;
            background-size: 1.2em;
            padding-right: 3rem;
            color-scheme: dark;
        }
        
        .form-select option {
            background-color: #0f172a !important;
            color: #ffffff !important;
            padding: 0.75rem;
        }
        
        .form-btn { 
            width: 100%; 
            padding: 1.25rem; 
            background: linear-gradient(135deg, #2dd4bf, #14b8a6); 
            color: #0f172a; 
            border: none; 
            border-radius: 10px; 
            font-weight: 600; 
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(45,212,191,0.3);
        }
        
        .form-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(45,212,191,0.4);
            background: linear-gradient(135deg, #14b8a6, #0d9488);
        }
        
        .wallet-status {
            position: fixed;
            top: 2rem;
            right: 2rem;
            background: rgba(30,41,59,0.95);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(45,212,191,0.3);
            backdrop-filter: blur(10px);
            z-index: 10;
        }
        
        .connect-btn {
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: #0f172a;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .connect-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(45,212,191,0.3);
        }
        
        .loading-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #2dd4bf, #14b8a6, #0d9488);
            transform: translateX(-100%);
            animation: loading 2s ease-in-out infinite;
            z-index: 100;
        }
        
        @keyframes loading {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(0%); }
            100% { transform: translateX(100%); }
        }
        
        @media (max-width: 768px) {
            .sidebar { 
                width: 100%; 
                height: 100vh; 
                position: fixed;
                top: 0;
                left: -100%;
                z-index: 1000;
                transition: left 0.3s ease;
                overflow-y: auto;
                padding: 6rem 1.5rem 2rem 1.5rem;
                background: rgba(15,23,42,0.98);
                backdrop-filter: blur(15px);
            }
            .sidebar.active { left: 0; }
            
            .app { 
                flex-direction: column; 
                padding-left: 0;
                width: 100vw;
                max-width: 100vw;
                overflow-x: hidden;
            }
            
            .main { 
                padding: 1rem; 
                padding-top: 5rem;
                width: 100vw;
                max-width: 100vw;
                overflow-x: hidden;
                min-height: 100vh;
                box-sizing: border-box;
            }
            
            .stats-grid { 
                grid-template-columns: 1fr; 
                gap: 1rem;
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
            }
            
            .vaults { 
                display: grid;
                grid-template-columns: 1fr; 
                gap: 1rem;
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
            }
            
            .vault-card {
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
                margin: 0;
            }
            
            .vault-actions {
                flex-direction: column;
                gap: 0.75rem;
            }
            
            .stat-card {
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
                margin: 0;
            }
            
            .mobile-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1rem 1.5rem;
                background: rgba(15,23,42,0.98);
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 998;
                backdrop-filter: blur(15px);
                border-bottom: 1px solid rgba(45,212,191,0.2);
                width: 100vw;
                max-width: 100vw;
                box-sizing: border-box;
            }
            
            .mobile-header h1 {
                color: #2dd4bf;
                font-size: 1.2rem;
                font-weight: 600;
                margin: 0;
                flex: 1;
            }
            
            .menu-toggle {
                background: linear-gradient(135deg, #2dd4bf, #14b8a6);
                border: none;
                color: #0f172a;
                padding: 1rem 1.25rem;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s ease;
                min-width: 80px;
                min-height: 44px; /* Apple recommended touch target size */
                text-align: center;
                touch-action: manipulation;
                -webkit-tap-highlight-color: transparent;
            }
            
            .menu-toggle:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 15px rgba(45,212,191,0.3);
            }
            
            .form-container {
                margin: 0;
                padding: 1.5rem;
                max-width: 100%;
                width: 100%;
                box-sizing: border-box;
            }
            
            .overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.7);
                z-index: 999;
                backdrop-filter: blur(2px);
            }
            .overlay.active { display: block; }
            
            /* Enhanced navigation for mobile */
            .nav-link {
                padding: 1.25rem 1.5rem;
                font-size: 1rem;
                margin-bottom: 0.75rem;
                min-height: 60px;
                display: flex;
                align-items: center;
                cursor: pointer;
                user-select: none;
                -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
                position: relative;
                border-radius: 12px;
                border: 1px solid rgba(45,212,191,0.2);
                background: rgba(30,41,59,0.6);
            }
            
            .nav-link:hover,
            .nav-link:active,
            .nav-link:focus {
                background: rgba(45,212,191,0.2);
                border-color: rgba(45,212,191,0.4);
                transform: translateX(2px);
            }
            
            .nav-link.active {
                background: linear-gradient(135deg, #2dd4bf, #14b8a6);
                color: #0f172a;
                border-color: #2dd4bf;
                font-weight: 600;
            }
            
            .nav-link svg {
                margin-right: 1rem;
                flex-shrink: 0;
            }
            
            .logo {
                font-size: 1.4rem;
                font-weight: 700;
                padding: 1.5rem 1rem;
                margin-bottom: 2rem;
                text-align: center;
                border: 2px solid rgba(45,212,191,0.3);
            }
            
            /* Hide desktop wallet status on mobile */
            .wallet-status { display: none !important; }
            
            /* Ensure all content stays within viewport */
            * {
                max-width: 100vw;
                box-sizing: border-box;
            }
            
            body {
                width: 100vw;
                max-width: 100vw;
                overflow-x: hidden;
            }
            
            html {
                width: 100vw;
                max-width: 100vw;
                overflow-x: hidden;
            }
        }
        
        @media (min-width: 769px) {
            .mobile-header { display: none; }
            .overlay { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="particles" id="particles"></div>
    <div class="loading-bar"></div>
    <div class="overlay" id="overlay"></div>
    
    <!-- Mobile Header -->
    <div class="mobile-header">
        <h1>HyperFlow Protocol</h1>
        <button class="menu-toggle" onclick="toggleMenu()">Menu</button>
    </div>
    
    <div class="wallet-status">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="color: #94a3b8; font-size: 0.9rem;">
                <div style="color: #2dd4bf; font-weight: 600;">HyperEVM Connected</div>
                <div id="wallet-address">0x742d...2a8f</div>
            </div>
            <button class="connect-btn" onclick="connectWallet()">Connect Wallet</button>
        </div>
    </div>

    <div class="app">
        <nav class="sidebar">
            <div class="logo">HyperFlow Protocol</div>
            <ul class="nav">
                <li class="nav-item">
                    <div class="nav-link active" data-page="dashboard">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                        </svg>
                        Dashboard
                    </div>
                </li>
                <li class="nav-item">
                    <div class="nav-link" data-page="vaults">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM12 17c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zM15.1 8H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                        </svg>
                        Smart Vaults
                    </div>
                </li>
                <li class="nav-item">
                    <div class="nav-link" data-page="bridge">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M6.5 10c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5S8 12.33 8 11.5 7.33 10 6.5 10zM12 10c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm5.5 0c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5S19 12.33 19 11.5s-.67-1.5-1.5-1.5z"/>
                        </svg>
                        Cross-Chain Bridge
                    </div>
                </li>
                <li class="nav-item">
                    <div class="nav-link" data-page="staking">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                        FLOW Staking
                    </div>
                </li>
                <li class="nav-item">
                    <div class="nav-link" data-page="governance">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                        </svg>
                        DAO Governance
                    </div>
                </li>
            </ul>
        </nav>
        
        <main class="main">
            <!-- Dashboard -->
            <div class="page active" id="dashboard">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Total Value Locked</div>
                        <div class="stat-value" id="tvl-value">$2.45M</div>
                        <div class="stat-change" id="tvl-change">+4.8% (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">FLOW Token Price</div>
                        <div class="stat-value" id="flow-price">$0.0125</div>
                        <div class="stat-change" id="price-change">+2.3% (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Active Users</div>
                        <div class="stat-value" id="users-count">2.8K</div>
                        <div class="stat-change" id="users-change">+156 (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Protocol Revenue</div>
                        <div class="stat-value" id="revenue-value">$85.0K</div>
                        <div class="stat-change" id="revenue-change">+5.8% (24h)</div>
                    </div>
                </div>
                
                <h2 style="margin-bottom: 1.5rem; color: #2dd4bf; font-size: 1.8rem;">Featured Vaults</h2>
                <div class="vaults" id="dashboard-vaults">
                    <!-- Vaults will be populated by JavaScript -->
                </div>
            </div>
            
            <!-- Vaults -->
            <div class="page" id="vaults">
                <h2 style="margin-bottom: 1.5rem; color: #2dd4bf; font-size: 1.8rem;">Smart Vaults Portfolio</h2>
                <div class="vaults" id="all-vaults">
                    <!-- All vaults will be populated by JavaScript -->
                </div>
            </div>
            
            <!-- Bridge -->
            <div class="page" id="bridge">
                <div class="form-container">
                    <h2 style="text-align: center; margin-bottom: 2rem; color: #2dd4bf; font-size: 1.8rem;">Cross-Chain Bridge</h2>
                    <div class="form-group">
                        <label class="form-label">From Network</label>
                        <select class="form-select" style="color-scheme: dark;">
                            <option>HyperEVM</option>
                            <option>Ethereum</option>
                            <option>BSC</option>
                            <option>Polygon</option>
                            <option>Arbitrum</option>
                            <option>Optimism</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">To Network</label>
                        <select class="form-select" style="color-scheme: dark;">
                            <option>Ethereum</option>
                            <option>HyperEVM</option>
                            <option>BSC</option>
                            <option>Polygon</option>
                            <option>Arbitrum</option>
                            <option>Optimism</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Token</label>
                        <select class="form-select" style="color-scheme: dark;">
                            <option>FLOW - HyperFlow Protocol Token</option>
                            <option>ETH - Ethereum</option>
                            <option>USDC - USD Coin</option>
                            <option>USDT - Tether USD</option>
                            <option>WBTC - Wrapped Bitcoin</option>
                            <option>DAI - Dai Stablecoin</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Amount</label>
                        <input type="number" class="form-input" placeholder="0.0" step="0.000001">
                        <small style="color: #64748b; margin-top: 0.75rem; display: block;">Balance: <span id="token-balance">245.67 FLOW</span></small>
                    </div>
                    <button class="form-btn" onclick="simulateBridge()">Bridge Assets</button>
                </div>
            </div>
            
            <!-- Staking -->
            <div class="page" id="staking">
                <div class="form-container">
                    <h2 style="text-align: center; margin-bottom: 2rem; color: #2dd4bf; font-size: 1.8rem;">Stake FLOW Tokens</h2>
                    <div class="stat-card" style="margin-bottom: 2rem; text-align: center;">
                        <div class="stat-label">Current APY</div>
                        <div class="stat-value" id="staking-apy">18.5%</div>
                        <div class="stat-change">Revenue sharing enabled</div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Amount to Stake</label>
                        <input type="number" class="form-input" placeholder="0.0" id="stake-amount">
                        <small style="color: #64748b; margin-top: 0.75rem; display: block;">Available: <span id="available-flow">245.67 FLOW</span></small>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Lock Period</label>
                        <select class="form-select" style="color-scheme: dark;" id="lock-period">
                            <option>No Lock (15.5% APY)</option>
                            <option>30 Days (18.5% APY)</option>
                            <option>90 Days (21.2% APY)</option>
                            <option>180 Days (24.8% APY)</option>
                        </select>
                    </div>
                    <button class="form-btn" onclick="simulateStaking()">Stake FLOW</button>
                </div>
            </div>
            
            <!-- Governance -->
            <div class="page" id="governance">
                <h2 style="margin-bottom: 1.5rem; color: #2dd4bf; font-size: 1.8rem;">DAO Governance Proposals</h2>
                <div class="vaults">
                    <div class="vault-card">
                        <div class="vault-name">
                            Proposal #001 
                            <span style="color: #10b981; font-size: 0.9rem; padding: 0.25rem 0.75rem; background: rgba(16,185,129,0.1); border-radius: 20px;">Active</span>
                        </div>
                        <div class="vault-desc">Add new yield strategy for USDC/ETH LP tokens with automated rebalancing and MEV protection.</div>
                        <div class="vault-metrics">
                            <div class="metric">
                                <div class="metric-label">Yes Votes</div>
                                <div class="metric-value">245,678 FLOW</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">No Votes</div>
                                <div class="metric-value">45,123 FLOW</div>
                            </div>
                        </div>
                        <div class="vault-actions">
                            <button class="vault-btn primary" onclick="vote('yes')">Vote Yes</button>
                            <button class="vault-btn" onclick="vote('no')">Vote No</button>
                        </div>
                    </div>
                    
                    <div class="vault-card">
                        <div class="vault-name">
                            Proposal #002 
                            <span style="color: #f59e0b; font-size: 0.9rem; padding: 0.25rem 0.75rem; background: rgba(245,158,11,0.1); border-radius: 20px;">Pending</span>
                        </div>
                        <div class="vault-desc">Increase protocol fee from 10% to 15% of yield to fund development and security audits.</div>
                        <div class="vault-metrics">
                            <div class="metric">
                                <div class="metric-label">Voting Starts</div>
                                <div class="metric-value">2 Days</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Duration</div>
                                <div class="metric-value">7 Days</div>
                            </div>
                        </div>
                        <div class="vault-actions">
                            <button class="vault-btn" disabled>Voting Soon</button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        let currentData = {};
        
        // Initialize particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 20; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.width = particle.style.height = Math.random() * 4 + 2 + 'px';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = (Math.random() * 10 + 15) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        // Enhanced Navigation functionality with touch support
        document.querySelectorAll('.nav-link').forEach(link => {
            // Add both click and touch event listeners
            const handleNavigation = (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                const targetPage = link.getAttribute('data-page');
                
                // Update active nav link
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Show target page
                document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
                document.getElementById(targetPage).classList.add('active');
                
                // Close mobile menu if on mobile
                if (window.innerWidth <= 768) {
                    setTimeout(() => {
                        const sidebar = document.querySelector('.sidebar');
                        const overlay = document.getElementById('overlay');
                        sidebar.classList.remove('active');
                        overlay.classList.remove('active');
                    }, 200);
                }
            };
            
            link.addEventListener('click', handleNavigation);
            link.addEventListener('touchend', handleNavigation);
        });

        // Fetch and update live data
        async function updateLiveData() {
            try {
                const response = await fetch('/api/live-data');
                const data = await response.json();
                currentData = data;
                
                // Update dashboard stats
                document.getElementById('tvl-value').textContent = '$' + (data.tvl / 1000000).toFixed(2) + 'M';
                document.getElementById('flow-price').textContent = '$' + data.flow_price.toFixed(4);
                document.getElementById('users-count').textContent = (data.users / 1000).toFixed(1) + 'K';
                document.getElementById('revenue-value').textContent = '$' + (data.revenue / 1000).toFixed(1) + 'K';
                
                // Update staking APY
                document.getElementById('staking-apy').textContent = '18.5%';
                
                // Update balances with animation
                const balanceElements = ['token-balance', 'available-flow'];
                balanceElements.forEach(id => {
                    const element = document.getElementById(id);
                    if (element) {
                        const currentBalance = parseFloat(element.textContent);
                        const newBalance = currentBalance + (Math.random() - 0.5) * 2;
                        element.textContent = Math.max(0, newBalance).toFixed(2) + ' FLOW';
                    }
                });
                
                // Update vault displays
                updateVaultDisplays(data.vaults);
                
            } catch (error) {
                console.log('Connection simulated - using demo data');
            }
        }

        function updateVaultDisplays(vaults) {
            const dashboardVaults = document.getElementById('dashboard-vaults');
            const allVaults = document.getElementById('all-vaults');
            
            const vaultHTML = vaults.map(vault => `
                <div class="vault-card">
                    <div class="vault-name">
                        ${vault.name} 
                        <span class="vault-apy">${vault.apy.toFixed(1)}%</span>
                    </div>
                    <div class="vault-desc">
                        ${getVaultDescription(vault.name)}
                    </div>
                    <div class="vault-metrics">
                        <div class="metric">
                            <div class="metric-label">TVL</div>
                            <div class="metric-value">$${(vault.tvl / 1000).toFixed(0)}K</div>
                        </div>
                        <div class="metric">
                            <div class="metric-label">Users</div>
                            <div class="metric-value">${vault.users}</div>
                        </div>
                    </div>
                    <div class="vault-actions">
                        <button class="vault-btn primary" onclick="simulateDeposit('${vault.name}')">Deposit</button>
                        <button class="vault-btn" onclick="simulateWithdraw('${vault.name}')">Withdraw</button>
                    </div>
                </div>
            `).join('');
            
            dashboardVaults.innerHTML = vaultHTML;
            allVaults.innerHTML = vaultHTML;
        }

        function getVaultDescription(name) {
            const descriptions = {
                'Delta Neutral Vault': 'Advanced delta-neutral strategies with automated rebalancing and market-neutral positioning.',
                'Yield Optimizer': 'Multi-protocol yield optimization with compound farming across top DeFi protocols.',
                'Cross-Protocol Aggregator': 'Automated cross-DEX arbitrage and liquidity provision with MEV protection.',
                'Risk Parity Strategy': 'Diversified risk-adjusted portfolio with dynamic allocation optimization.'
            };
            return descriptions[name] || 'Advanced yield generation strategy with automated management.';
        }

        // Simulation functions
        function simulateBridge() {
            const btn = event.target;
            btn.innerHTML = 'Processing...';
            btn.disabled = true;
            
            setTimeout(() => {
                btn.innerHTML = 'Transaction Confirmed!';
                btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                
                setTimeout(() => {
                    btn.innerHTML = 'Bridge Assets';
                    btn.disabled = false;
                    btn.style.background = 'linear-gradient(135deg, #2dd4bf, #14b8a6)';
                }, 2000);
            }, 3000);
        }

        function simulateStaking() {
            const btn = event.target;
            const amount = document.getElementById('stake-amount').value;
            
            if (!amount || parseFloat(amount) <= 0) {
                alert('Please enter a valid amount');
                return;
            }
            
            btn.innerHTML = 'Staking...';
            btn.disabled = true;
            
            setTimeout(() => {
                btn.innerHTML = 'Staked Successfully!';
                btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                document.getElementById('stake-amount').value = '';
                
                setTimeout(() => {
                    btn.innerHTML = 'Stake FLOW';
                    btn.disabled = false;
                    btn.style.background = 'linear-gradient(135deg, #2dd4bf, #14b8a6)';
                }, 2000);
            }, 2500);
        }

        function simulateDeposit(vaultName) {
            const amount = prompt(`Enter amount to deposit into ${vaultName}:`, '100');
            if (amount && parseFloat(amount) > 0) {
                alert(`Successfully deposited ${amount} tokens into ${vaultName}!`);
            }
        }

        function simulateWithdraw(vaultName) {
            const amount = prompt(`Enter amount to withdraw from ${vaultName}:`, '50');
            if (amount && parseFloat(amount) > 0) {
                alert(`Successfully withdrew ${amount} tokens from ${vaultName}!`);
            }
        }

        function vote(choice) {
            const btn = event.target;
            btn.innerHTML = choice === 'yes' ? 'Voting Yes...' : 'Voting No...';
            btn.disabled = true;
            
            setTimeout(() => {
                btn.innerHTML = 'Vote Recorded!';
                btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                
                setTimeout(() => {
                    btn.innerHTML = choice === 'yes' ? 'Vote Yes' : 'Vote No';
                    btn.disabled = false;
                    btn.style.background = choice === 'yes' ? 
                        'linear-gradient(135deg, #2dd4bf, #14b8a6)' : 
                        'transparent';
                }, 2000);
            }, 1500);
        }

        function connectWallet() {
            const btn = event.target;
            btn.innerHTML = 'Connecting...';
            btn.disabled = true;
            
            setTimeout(() => {
                btn.innerHTML = 'Connected!';
                btn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                document.getElementById('wallet-address').textContent = '0x742d...2a8f';
                
                setTimeout(() => {
                    btn.innerHTML = 'Disconnect';
                    btn.disabled = false;
                }, 1500);
            }, 2000);
        }

        // Enhanced Mobile menu functions with touch support
        function toggleMenu() {
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.getElementById('overlay');
            const menuBtn = document.querySelector('.menu-toggle');
            
            const isActive = sidebar.classList.contains('active');
            
            if (isActive) {
                sidebar.classList.remove('active');
                overlay.classList.remove('active');
                menuBtn.textContent = 'Menu';
            } else {
                sidebar.classList.add('active');
                overlay.classList.add('active');
                menuBtn.textContent = 'Close';
            }
        }

        // Close menu when clicking/touching overlay
        document.getElementById('overlay').addEventListener('click', toggleMenu);
        document.getElementById('overlay').addEventListener('touchend', toggleMenu);
        
        // Prevent touch scroll on body when menu is open
        function preventScroll(e) {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar.classList.contains('active')) {
                e.preventDefault();
            }
        }
        
        // Add touch scroll prevention
        document.addEventListener('touchmove', preventScroll, { passive: false });

        // Initialize everything
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
            updateLiveData();
            
            // Update data every 3 seconds for realistic feel
            setInterval(updateLiveData, 3000);
            
            // Add some dynamic effects
            setTimeout(() => {
                document.querySelector('.loading-bar').style.display = 'none';
            }, 2000);
        });
    </script>
</body>
</html>"""

if __name__ == "__main__":
    print("🚀 HyperFlow Protocol - Live DeFi Infrastructure")
    print("📊 Real-time data simulation active")
    print("🏦 Smart Vaults with dynamic APY updates")
    print("🌉 Cross-chain bridge with transaction simulation")  
    print("💎 Interactive staking with multiple lock periods")
    print("🗳️ DAO governance with live voting")
    print("✨ Animated UI with particle effects")
    print(f"✅ Running at http://localhost:{PORT}")
    
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")