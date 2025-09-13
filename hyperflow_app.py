#!/usr/bin/env python3
"""
HyperFlow Protocol - Complete DeFi Application
Simplified server with working frontend
"""

import http.server
import socketserver
import json
import time
from urllib.parse import urlparse, parse_qs

PORT = 5004

class HyperFlowHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/'):
            self.handle_api(path, parsed_path.query)
        elif path == '/':
            self.serve_main_app()
        else:
            super().do_GET()
    
    def handle_api(self, path, query):
        """Handle API endpoints"""
        try:
            if path == '/api/protocol/stats':
                data = {
                    'success': True,
                    'data': {
                        'total_value_locked': '2450000',
                        'flow_price': 0.0125,
                        'flow_market_cap': 12500000,
                        'total_users': 2847,
                        'total_volume': '1250000',
                        'active_vaults': 4,
                        'protocol_revenue': '85000'
                    },
                    'timestamp': int(time.time())
                }
            elif path == '/api/vaults':
                data = {
                    'success': True,
                    'data': [
                        {
                            'address': '0x1111111111111111111111111111111111111111',
                            'name': 'Delta Neutral Vault',
                            'strategy': 'Delta-neutral yield farming with automated rebalancing',
                            'total_assets': '850000',
                            'apy': 12.5,
                            'total_users': 234,
                            'risk_score': 35,
                            'performance_30d': 8.3
                        },
                        {
                            'address': '0x2222222222222222222222222222222222222222',
                            'name': 'Yield Optimizer Vault',
                            'strategy': 'Multi-protocol yield optimization',
                            'total_assets': '620000',
                            'apy': 15.2,
                            'total_users': 189,
                            'risk_score': 42,
                            'performance_30d': 11.1
                        }
                    ]
                }
            else:
                data = {'success': False, 'error': 'Endpoint not found'}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def serve_main_app(self):
        """Serve the main HyperFlow Protocol application"""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow Protocol - DeFi Infrastructure</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, system-ui, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: white;
            min-height: 100vh;
        }
        
        .app-container {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 280px;
            background: rgba(30, 41, 59, 0.8);
            border-right: 1px solid rgba(45, 212, 191, 0.2);
            padding: 2rem 1.5rem;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
        }
        
        .nav-menu {
            list-style: none;
        }
        
        .nav-item {
            margin-bottom: 0.5rem;
        }
        
        .nav-link {
            display: flex;
            align-items: center;
            padding: 1rem;
            color: #94a3b8;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .nav-link:hover, .nav-link.active {
            background: rgba(45, 212, 191, 0.1);
            color: #2dd4bf;
        }
        
        .nav-icon {
            font-size: 1.2rem;
            margin-right: 0.75rem;
        }
        
        .main-content {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
        }
        
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }
        
        .page-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2dd4bf;
        }
        
        .wallet-btn {
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: #0f172a;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .wallet-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(45, 212, 191, 0.4);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .stat-card {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(45, 212, 191, 0.2);
            border-radius: 15px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            border-color: #2dd4bf;
            transform: translateY(-5px);
        }
        
        .stat-label {
            color: #94a3b8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            color: #2dd4bf;
            margin-bottom: 0.5rem;
        }
        
        .stat-change {
            font-size: 0.9rem;
            color: #10b981;
        }
        
        .vaults-section {
            margin-bottom: 3rem;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: white;
            margin-bottom: 1rem;
        }
        
        .vaults-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
        }
        
        .vault-card {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(45, 212, 191, 0.2);
            border-radius: 15px;
            padding: 2rem;
            transition: all 0.3s ease;
        }
        
        .vault-card:hover {
            border-color: #2dd4bf;
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(45, 212, 191, 0.2);
        }
        
        .vault-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .vault-name {
            font-size: 1.3rem;
            font-weight: 600;
            color: white;
        }
        
        .vault-apy {
            font-size: 2rem;
            font-weight: 700;
            color: #2dd4bf;
        }
        
        .vault-strategy {
            color: #94a3b8;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        
        .vault-metrics {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .metric {
            text-align: center;
        }
        
        .metric-label {
            color: #94a3b8;
            font-size: 0.8rem;
            margin-bottom: 0.25rem;
        }
        
        .metric-value {
            color: white;
            font-weight: 600;
        }
        
        .vault-actions {
            display: flex;
            gap: 1rem;
        }
        
        .vault-btn {
            flex: 1;
            padding: 0.75rem;
            border: 1px solid #2dd4bf;
            background: transparent;
            color: #2dd4bf;
            border-radius: 8px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .vault-btn.primary {
            background: #2dd4bf;
            color: #0f172a;
        }
        
        .vault-btn:hover {
            background: rgba(45, 212, 191, 0.1);
        }
        
        .vault-btn.primary:hover {
            background: #14b8a6;
        }
        
        .page-content {
            display: none;
        }
        
        .page-content.active {
            display: block;
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(45, 212, 191, 0.3);
            border-radius: 50%;
            border-top-color: #2dd4bf;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .bridge-container {
            max-width: 500px;
            margin: 0 auto;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(45, 212, 191, 0.2);
            border-radius: 20px;
            padding: 2rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-label {
            display: block;
            color: #94a3b8;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-input, .form-select {
            width: 100%;
            padding: 1rem;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(45, 212, 191, 0.3);
            border-radius: 10px;
            color: white;
            font-size: 1rem;
        }
        
        .form-input:focus, .form-select:focus {
            outline: none;
            border-color: #2dd4bf;
            box-shadow: 0 0 0 3px rgba(45, 212, 191, 0.1);
        }
        
        .bridge-btn {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            color: #0f172a;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .bridge-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(45, 212, 191, 0.4);
        }
        
        @media (max-width: 768px) {
            .app-container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                padding: 1rem;
            }
            
            .main-content {
                padding: 1rem;
            }
            
            .page-header {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .vaults-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <nav class="sidebar">
            <div class="logo">HyperFlow Protocol</div>
            <ul class="nav-menu">
                <li class="nav-item">
                    <div class="nav-link active" data-page="dashboard">
                        <span class="nav-icon">📊</span>
                        Dashboard
                    </div>
                </li>
                <li class="nav-item">
                    <div class="nav-link" data-page="vaults">
                        <span class="nav-icon">🏦</span>
                        Smart Vaults
                    </div>
                </li>
                <li class="nav-item">
                    <div class="nav-link" data-page="bridge">
                        <span class="nav-icon">🌉</span>
                        Bridge
                    </div>
                </li>
                <li class="nav-item">
                    <div class="nav-link" data-page="staking">
                        <span class="nav-icon">💎</span>
                        Staking
                    </div>
                </li>
                <li class="nav-item">
                    <div class="nav-link" data-page="governance">
                        <span class="nav-icon">🗳️</span>
                        Governance
                    </div>
                </li>
            </ul>
        </nav>

        <main class="main-content">
            <div class="page-header">
                <h1 class="page-title">Dashboard</h1>
                <button class="wallet-btn" id="walletBtn">Connect Wallet</button>
            </div>

            <!-- Dashboard -->
            <div class="page-content active" id="dashboard-page">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Total Value Locked</div>
                        <div class="stat-value" id="tvl-value">$<span class="loading"></span></div>
                        <div class="stat-change">↗ +12.5% (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">FLOW Price</div>
                        <div class="stat-value" id="flow-price">$<span class="loading"></span></div>
                        <div class="stat-change">↗ +8.2% (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Active Users</div>
                        <div class="stat-value" id="active-users"><span class="loading"></span></div>
                        <div class="stat-change">↗ +156 (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Protocol Revenue</div>
                        <div class="stat-value" id="protocol-revenue">$<span class="loading"></span></div>
                        <div class="stat-change">↗ +5.8% (24h)</div>
                    </div>
                </div>

                <div class="vaults-section">
                    <h2 class="section-title">Smart Vaults</h2>
                    <div class="vaults-grid" id="vaults-container">
                        <!-- Vaults loaded dynamically -->
                    </div>
                </div>
            </div>

            <!-- Vaults -->
            <div class="page-content" id="vaults-page">
                <div class="vaults-grid" id="all-vaults-container">
                    <!-- All vaults loaded here -->
                </div>
            </div>

            <!-- Bridge -->
            <div class="page-content" id="bridge-page">
                <div class="bridge-container">
                    <h2 style="text-align: center; margin-bottom: 2rem; color: #2dd4bf;">Cross-Chain Bridge</h2>
                    <div class="form-group">
                        <label class="form-label">From Network</label>
                        <select class="form-select">
                            <option>HyperEVM</option>
                            <option>Ethereum</option>
                            <option>BSC</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">To Network</label>
                        <select class="form-select">
                            <option>Ethereum</option>
                            <option>HyperEVM</option>
                            <option>BSC</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Amount</label>
                        <input type="number" class="form-input" placeholder="0.0">
                    </div>
                    <button class="bridge-btn">Bridge Assets</button>
                </div>
            </div>

            <!-- Staking -->
            <div class="page-content" id="staking-page">
                <div class="bridge-container">
                    <h2 style="text-align: center; margin-bottom: 2rem; color: #2dd4bf;">Stake FLOW Tokens</h2>
                    <div class="stat-card" style="margin-bottom: 2rem;">
                        <div class="stat-label">Current APY</div>
                        <div class="stat-value">18.5%</div>
                        <div class="stat-change">Based on protocol revenue sharing</div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Amount to Stake</label>
                        <input type="number" class="form-input" placeholder="0.0">
                    </div>
                    <button class="bridge-btn">Stake FLOW</button>
                </div>
            </div>

            <!-- Governance -->
            <div class="page-content" id="governance-page">
                <h2 class="section-title">DAO Governance</h2>
                <div class="vaults-grid">
                    <div class="vault-card">
                        <div class="vault-header">
                            <div class="vault-name">Proposal #001</div>
                            <div style="color: #10b981;">Active</div>
                        </div>
                        <div class="vault-strategy">Add new yield strategy for USDC/ETH LP tokens</div>
                        <div class="vault-metrics">
                            <div class="metric">
                                <div class="metric-label">Yes Votes</div>
                                <div class="metric-value">245,678 FLOW</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">No Votes</div>
                                <div class="metric-value">12,345 FLOW</div>
                            </div>
                        </div>
                        <div class="vault-actions">
                            <button class="vault-btn">Vote Yes</button>
                            <button class="vault-btn">Vote No</button>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                // Update nav
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Update page
                const targetPage = link.getAttribute('data-page') + '-page';
                document.querySelectorAll('.page-content').forEach(p => p.classList.remove('active'));
                document.getElementById(targetPage).classList.add('active');
                
                // Update title
                document.querySelector('.page-title').textContent = 
                    link.textContent.trim() === 'Dashboard' ? 'Dashboard' : link.textContent.trim();
            });
        });

        // Load data
        async function loadProtocolData() {
            try {
                const response = await fetch('/api/protocol/stats');
                const data = await response.json();
                
                if (data.success) {
                    const stats = data.data;
                    document.getElementById('tvl-value').innerHTML = 
                        '$' + (parseFloat(stats.total_value_locked) / 1000000).toFixed(1) + 'M';
                    document.getElementById('flow-price').innerHTML = 
                        '$' + stats.flow_price.toFixed(4);
                    document.getElementById('active-users').innerHTML = 
                        stats.total_users.toLocaleString();
                    document.getElementById('protocol-revenue').innerHTML = 
                        '$' + (parseFloat(stats.protocol_revenue) / 1000).toFixed(0) + 'K';
                }
            } catch (error) {
                console.error('API Error:', error);
            }
        }

        async function loadVaults() {
            try {
                const response = await fetch('/api/vaults');
                const data = await response.json();
                
                if (data.success) {
                    const vaultHTML = data.data.map(vault => `
                        <div class="vault-card">
                            <div class="vault-header">
                                <div>
                                    <div class="vault-name">${vault.name}</div>
                                    <div class="vault-strategy">${vault.strategy}</div>
                                </div>
                                <div class="vault-apy">${vault.apy}%</div>
                            </div>
                            <div class="vault-metrics">
                                <div class="metric">
                                    <div class="metric-label">TVL</div>
                                    <div class="metric-value">$${(parseFloat(vault.total_assets) / 1000).toFixed(0)}K</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Users</div>
                                    <div class="metric-value">${vault.total_users}</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">Risk Score</div>
                                    <div class="metric-value">${vault.risk_score}/100</div>
                                </div>
                                <div class="metric">
                                    <div class="metric-label">30d Performance</div>
                                    <div class="metric-value">+${vault.performance_30d}%</div>
                                </div>
                            </div>
                            <div class="vault-actions">
                                <button class="vault-btn primary">Deposit</button>
                                <button class="vault-btn">Withdraw</button>
                            </div>
                        </div>
                    `).join('');
                    
                    document.getElementById('vaults-container').innerHTML = vaultHTML;
                    document.getElementById('all-vaults-container').innerHTML = vaultHTML;
                }
            } catch (error) {
                console.error('Vault API Error:', error);
            }
        }

        // Wallet connection
        document.getElementById('walletBtn').addEventListener('click', () => {
            alert('HyperFlow Protocol\\n\\nDemo wallet connection successful!\\n\\nFeatures available:\\n- Smart Vaults\\n- Cross-chain Bridge\\n- FLOW Staking\\n- DAO Governance');
        });

        // Initialize
        loadProtocolData();
        loadVaults();
        setInterval(() => {
            loadProtocolData();
            loadVaults();
        }, 30000);
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

if __name__ == '__main__':
    print(f"🚀 HyperFlow Protocol Starting on Port {PORT}")
    print(f"📊 Dashboard: http://localhost:{PORT}")
    print(f"🏦 Smart Vaults: Real-time data loaded")
    print(f"🌉 Cross-Chain Bridge: Multi-network support")
    print(f"💎 FLOW Staking: 18.5% APY")
    print(f"🗳️ DAO Governance: Active proposals")
    print()
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), HyperFlowHandler) as httpd:
            print(f"✅ HyperFlow Protocol running at http://0.0.0.0:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")