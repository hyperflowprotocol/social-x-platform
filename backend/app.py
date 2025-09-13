#!/usr/bin/env python3
"""
HyperFlow Protocol Backend API
Advanced DeFi infrastructure with real-time data, analytics, and smart contract integration
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
# from web3 import Web3  # Commented out since web3 is not installed
import json
import os
import time
import threading
from datetime import datetime, timedelta
import sqlite3
import requests
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
HYPEREVM_RPC = os.getenv('HYPEREVM_RPC', 'https://hyperevm-mainnet.rpc.url')  # Replace with actual RPC
FLOW_TOKEN_ADDRESS = os.getenv('FLOW_TOKEN_ADDRESS', '0x0000000000000000000000000000000000000000')
HYPE_TOKEN_ADDRESS = os.getenv('HYPE_TOKEN_ADDRESS', '0xd6e7bF33a21b56D5927bbF0101FE45FF92ecF9Ba')
PRESALE_CONTRACT_ADDRESS = os.getenv('PRESALE_CONTRACT_ADDRESS', '0x0000000000000000000000000000000000000000')

# Web3 connection (disabled for demo)
w3 = None  # Will be implemented when web3 package is available
logger.info("HyperEVM connection disabled for demo mode")

# Database setup
def init_database():
    """Initialize SQLite database for analytics and caching"""
    conn = sqlite3.connect('hyperflow.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_hash TEXT UNIQUE,
            block_number INTEGER,
            from_address TEXT,
            to_address TEXT,
            value TEXT,
            gas_used INTEGER,
            gas_price TEXT,
            timestamp INTEGER,
            tx_type TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vault_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vault_address TEXT,
            timestamp INTEGER,
            total_assets TEXT,
            share_price TEXT,
            apy REAL,
            total_users INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_address TEXT,
            total_deposited TEXT,
            current_balance TEXT,
            rewards_earned TEXT,
            last_activity INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_address TEXT,
            price_usd REAL,
            volume_24h REAL,
            market_cap REAL,
            timestamp INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

init_database()

class HyperFlowAnalytics:
    """Analytics and data processing for HyperFlow Protocol"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_cached_or_fetch(self, key: str, fetch_func, ttl: Optional[int] = None):
        """Generic caching mechanism"""
        current_time = time.time()
        ttl = ttl or self.cache_ttl
        
        if key in self.cache:
            data, timestamp = self.cache[key]
            if current_time - timestamp < ttl:
                return data
        
        try:
            data = fetch_func()
            self.cache[key] = (data, current_time)
            return data
        except Exception as e:
            logger.error(f"Failed to fetch data for {key}: {e}")
            return {}
    
    def get_protocol_stats(self) -> Dict:
        """Get overall protocol statistics"""
        return self.get_cached_or_fetch('protocol_stats', self._fetch_protocol_stats)
    
    def _fetch_protocol_stats(self) -> Dict:
        """Fetch protocol statistics from blockchain"""
        stats = {
            'total_value_locked': '0',
            'total_users': 0,
            'total_volume': '0',
            'flow_price': 0.0,
            'flow_market_cap': 0.0,
            'active_vaults': 0,
            'total_rewards_distributed': '0',
            'protocol_revenue': '0'
        }
        
        try:
            conn = sqlite3.connect('hyperflow.db')
            cursor = conn.cursor()
            
            # Get user count
            cursor.execute('SELECT COUNT(DISTINCT user_address) FROM user_analytics')
            stats['total_users'] = cursor.fetchone()[0] or 0
            
            # Get latest price data
            cursor.execute('''
                SELECT price_usd, market_cap, volume_24h 
                FROM price_data 
                WHERE token_address = ? 
                ORDER BY timestamp DESC LIMIT 1
            ''', (FLOW_TOKEN_ADDRESS,))
            
            price_data = cursor.fetchone()
            if price_data:
                stats['flow_price'] = price_data[0] or 0.0
                stats['flow_market_cap'] = price_data[1] or 0.0
                stats['total_volume'] = str(int(price_data[2] or 0))
            
            conn.close()
            
            # Simulate some realistic values for demo
            stats.update({
                'total_value_locked': '2450000',  # $2.45M
                'active_vaults': 4,
                'total_rewards_distributed': '125000',  # $125K
                'protocol_revenue': '85000'  # $85K
            })
            
        except Exception as e:
            logger.error(f"Error fetching protocol stats: {e}")
        
        return stats
    
    def get_vault_data(self, vault_address: str = None) -> List[Dict]:
        """Get vault performance data"""
        cache_key = f'vault_data_{vault_address or "all"}'
        return self.get_cached_or_fetch(cache_key, 
                                       lambda: self._fetch_vault_data(vault_address))
    
    def _fetch_vault_data(self, vault_address: str = None) -> List[Dict]:
        """Fetch vault data from database"""
        vaults = []
        
        # Simulate vault data for demo
        demo_vaults = [
            {
                'address': '0x1111111111111111111111111111111111111111',
                'name': 'Delta Neutral Vault',
                'strategy': 'Delta-neutral yield farming with automated rebalancing',
                'total_assets': '850000',
                'share_price': '1.0342',
                'apy': 12.5,
                'total_users': 234,
                'risk_score': 35,
                'inception_date': '2025-01-15',
                'performance_24h': 0.8,
                'performance_7d': 2.1,
                'performance_30d': 8.3
            },
            {
                'address': '0x2222222222222222222222222222222222222222',
                'name': 'Yield Optimizer Vault',
                'strategy': 'Multi-protocol yield optimization with compound farming',
                'total_assets': '620000',
                'share_price': '1.0187',
                'apy': 15.2,
                'total_users': 189,
                'risk_score': 42,
                'inception_date': '2025-01-20',
                'performance_24h': 1.2,
                'performance_7d': 2.8,
                'performance_30d': 11.1
            },
            {
                'address': '0x3333333333333333333333333333333333333333',
                'name': 'Cross-Protocol Aggregator',
                'strategy': 'Automated cross-DEX arbitrage and liquidity provision',
                'total_assets': '480000',
                'share_price': '1.0095',
                'apy': 9.8,
                'total_users': 156,
                'risk_score': 28,
                'inception_date': '2025-01-25',
                'performance_24h': 0.3,
                'performance_7d': 1.5,
                'performance_30d': 6.2
            },
            {
                'address': '0x4444444444444444444444444444444444444444',
                'name': 'Risk Parity Vault',
                'strategy': 'Risk-balanced portfolio with dynamic hedging strategies',
                'total_assets': '500000',
                'share_price': '1.0156',
                'apy': 11.7,
                'total_users': 178,
                'risk_score': 25,
                'inception_date': '2025-02-01',
                'performance_24h': 0.5,
                'performance_7d': 1.9,
                'performance_30d': 7.8
            }
        ]
        
        if vault_address and vault_address != "None":
            vaults = [v for v in demo_vaults if v['address'].lower() == vault_address.lower()]
        else:
            vaults = demo_vaults
            
        return vaults
    
    def get_price_history(self, token_address: str, days: int = 30) -> List[Dict]:
        """Get historical price data"""
        return self.get_cached_or_fetch(f'price_history_{token_address}_{days}',
                                       lambda: self._generate_price_history(days))
    
    def _generate_price_history(self, days: int) -> List[Dict]:
        """Generate realistic price history for demo"""
        import random
        import math
        
        history = []
        base_price = 0.0125  # $0.0125 starting price
        current_time = int(time.time())
        
        for i in range(days):
            timestamp = current_time - (days - i) * 86400  # 24 hours ago
            
            # Generate realistic price movement
            price_change = random.gauss(0, 0.05)  # Normal distribution with 5% volatility
            base_price *= (1 + price_change)
            base_price = max(0.001, base_price)  # Minimum price floor
            
            volume = random.uniform(50000, 200000)  # Daily volume
            
            history.append({
                'timestamp': timestamp,
                'price': round(base_price, 6),
                'volume': round(volume, 2),
                'high': round(base_price * random.uniform(1.02, 1.08), 6),
                'low': round(base_price * random.uniform(0.92, 0.98), 6)
            })
        
        return history

analytics = HyperFlowAnalytics()

# API Routes

@app.route('/')
def dashboard():
    """Main dashboard HTML"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HyperFlow Protocol - Live Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: #0f172a;
            color: white;
            min-height: 100vh;
        }
        
        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3rem;
        }
        
        .logo {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .status {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.4));
            border: 1px solid rgba(45, 212, 191, 0.2);
            border-radius: 15px;
            padding: 2rem;
        }
        
        .stat-label {
            color: #94a3b8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #2dd4bf;
            margin-bottom: 0.5rem;
        }
        
        .stat-change {
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .positive { color: #10b981; }
        .negative { color: #ef4444; }
        
        .charts-section {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .chart-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.4));
            border: 1px solid rgba(45, 212, 191, 0.2);
            border-radius: 15px;
            padding: 2rem;
        }
        
        .chart-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: white;
            margin-bottom: 1.5rem;
        }
        
        .vaults-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
        }
        
        .vault-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(51, 65, 85, 0.4));
            border: 1px solid rgba(45, 212, 191, 0.2);
            border-radius: 15px;
            padding: 2rem;
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
            margin-bottom: 0.5rem;
        }
        
        .vault-strategy {
            color: #94a3b8;
            font-size: 0.9rem;
        }
        
        .vault-apy {
            font-size: 2rem;
            font-weight: 700;
            color: #2dd4bf;
            text-align: right;
        }
        
        .vault-metrics {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-top: 1rem;
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
        
        .footer {
            text-align: center;
            padding: 2rem 0;
            border-top: 1px solid rgba(45, 212, 191, 0.1);
            margin-top: 3rem;
            color: #64748b;
        }
        
        @media (max-width: 768px) {
            .charts-section {
                grid-template-columns: 1fr;
            }
            .header {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <div class="logo">HyperFlow Protocol</div>
            <div class="status">
                <div class="status-indicator"></div>
                <span>Live Dashboard</span>
            </div>
        </div>

        <div class="stats-grid" id="statsGrid">
            <!-- Stats will be loaded here -->
        </div>

        <div class="charts-section">
            <div class="chart-card">
                <div class="chart-title">FLOW Price Chart (30 Days)</div>
                <canvas id="priceChart" height="300"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">Protocol Metrics</div>
                <canvas id="metricsChart" height="300"></canvas>
            </div>
        </div>

        <div class="vaults-grid" id="vaultsGrid">
            <!-- Vaults will be loaded here -->
        </div>

        <div class="footer">
            <p>HyperFlow Protocol © 2025 | Advanced DeFi Infrastructure for HyperEVM</p>
        </div>
    </div>

    <script>
        let priceChart, metricsChart;

        // Load dashboard data
        async function loadDashboardData() {
            try {
                // Load protocol stats
                const statsResponse = await fetch('/api/protocol/stats');
                const stats = await statsResponse.json();
                updateStatsGrid(stats);

                // Load vault data
                const vaultsResponse = await fetch('/api/vaults');
                const vaults = await vaultsResponse.json();
                updateVaultsGrid(vaults.data);

                // Load price chart
                const priceResponse = await fetch('/api/price/history?days=30');
                const priceData = await priceResponse.json();
                updatePriceChart(priceData.data);

                // Create metrics chart
                createMetricsChart(stats);

            } catch (error) {
                console.error('Error loading dashboard data:', error);
            }
        }

        function updateStatsGrid(stats) {
            const grid = document.getElementById('statsGrid');
            grid.innerHTML = `
                <div class="stat-card">
                    <div class="stat-label">Total Value Locked</div>
                    <div class="stat-value">$${formatNumber(stats.total_value_locked)}</div>
                    <div class="stat-change positive">↗ +12.5% (24h)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">FLOW Price</div>
                    <div class="stat-value">$${stats.flow_price.toFixed(4)}</div>
                    <div class="stat-change positive">↗ +8.2% (24h)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Total Users</div>
                    <div class="stat-value">${formatNumber(stats.total_users)}</div>
                    <div class="stat-change positive">↗ +156 (24h)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Protocol Revenue</div>
                    <div class="stat-value">$${formatNumber(stats.protocol_revenue)}</div>
                    <div class="stat-change positive">↗ +5.8% (24h)</div>
                </div>
            `;
        }

        function updateVaultsGrid(vaults) {
            const grid = document.getElementById('vaultsGrid');
            grid.innerHTML = vaults.map(vault => `
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
                            <div class="metric-value">$${formatNumber(vault.total_assets)}</div>
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
                </div>
            `).join('');
        }

        function updatePriceChart(priceData) {
            const ctx = document.getElementById('priceChart').getContext('2d');
            
            if (priceChart) priceChart.destroy();
            
            priceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: priceData.map(d => new Date(d.timestamp * 1000).toLocaleDateString()),
                    datasets: [{
                        label: 'FLOW Price',
                        data: priceData.map(d => d.price),
                        borderColor: '#2dd4bf',
                        backgroundColor: 'rgba(45, 212, 191, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { 
                            display: true,
                            grid: { color: 'rgba(148, 163, 184, 0.1)' },
                            ticks: { color: '#94a3b8' }
                        },
                        y: { 
                            display: true,
                            grid: { color: 'rgba(148, 163, 184, 0.1)' },
                            ticks: { color: '#94a3b8' }
                        }
                    }
                }
            });
        }

        function createMetricsChart(stats) {
            const ctx = document.getElementById('metricsChart').getContext('2d');
            
            if (metricsChart) metricsChart.destroy();
            
            metricsChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Staked', 'Liquid', 'Development', 'Treasury'],
                    datasets: [{
                        data: [35, 40, 15, 10],
                        backgroundColor: [
                            '#2dd4bf',
                            '#14b8a6',
                            '#0d9488',
                            '#0f766e'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#94a3b8' }
                        }
                    }
                }
            });
        }

        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
            return num.toString();
        }

        // Auto-refresh dashboard every 30 seconds
        setInterval(loadDashboardData, 30000);

        // Initial load
        loadDashboardData();
    </script>
</body>
</html>
    ''')

@app.route('/api/protocol/stats')
def get_protocol_stats():
    """Get overall protocol statistics"""
    try:
        stats = analytics.get_protocol_stats()
        return jsonify({
            'success': True,
            'data': stats,
            'timestamp': int(time.time())
        })
    except Exception as e:
        logger.error(f"Error getting protocol stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/vaults')
@app.route('/api/vaults/<vault_address>')
def get_vaults(vault_address=None):
    """Get vault information"""
    try:
        vaults = analytics.get_vault_data(vault_address)
        return jsonify({
            'success': True,
            'data': vaults,
            'count': len(vaults),
            'timestamp': int(time.time())
        })
    except Exception as e:
        logger.error(f"Error getting vault data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/price/history')
def get_price_history():
    """Get historical price data"""
    try:
        token_address = request.args.get('token', FLOW_TOKEN_ADDRESS)
        days = int(request.args.get('days', 30))
        
        history = analytics.get_price_history(token_address, days)
        
        return jsonify({
            'success': True,
            'data': history,
            'token': token_address,
            'days': days,
            'timestamp': int(time.time())
        })
    except Exception as e:
        logger.error(f"Error getting price history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/user/<address>')
def get_user_data(address):
    """Get user-specific data"""
    try:
        if not address or len(address) != 42 or not address.startswith('0x'):
            return jsonify({'success': False, 'error': 'Invalid address'}), 400
        
        # Simulate user data for demo
        user_data = {
            'address': address,
            'total_deposited': '5000',
            'current_balance': '5234.56',
            'rewards_earned': '234.56',
            'vaults_count': 2,
            'last_activity': int(time.time()) - 3600,
            'positions': [
                {
                    'vault': '0x1111111111111111111111111111111111111111',
                    'vault_name': 'Delta Neutral Vault',
                    'deposited': '3000',
                    'current_value': '3142.85',
                    'rewards': '142.85'
                },
                {
                    'vault': '0x2222222222222222222222222222222222222222',
                    'vault_name': 'Yield Optimizer Vault',
                    'deposited': '2000',
                    'current_value': '2091.71',
                    'rewards': '91.71'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': user_data,
            'timestamp': int(time.time())
        })
        
    except Exception as e:
        logger.error(f"Error getting user data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/presale/stats')
def get_presale_stats():
    """Get presale statistics"""
    try:
        # Simulate presale data
        presale_stats = {
            'total_hype_raised': '1847.5',
            'total_flow_sold': '46187500',
            'progress_percentage': 92.38,
            'buyers_count': 891,
            'time_remaining': 432000,  # 5 days in seconds
            'exchange_rate': 25000,
            'hard_cap': '2000',
            'min_purchase': '0.1',
            'max_purchase': '100',
            'is_active': True
        }
        
        return jsonify({
            'success': True,
            'data': presale_stats,
            'timestamp': int(time.time())
        })
        
    except Exception as e:
        logger.error(f"Error getting presale stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': int(time.time()),
        'hyperevm_connected': w3.is_connected() if w3 else False,
        'version': '1.0.0'
    })

if __name__ == '__main__':
    logger.info("Starting HyperFlow Protocol Backend API")
    app.run(host='0.0.0.0', port=5000, debug=True)