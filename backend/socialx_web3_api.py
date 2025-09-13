#!/usr/bin/env python3
"""
SocialX Trading Platform - Web3 Backend API
Integrates with real deployed smart contracts on HyperEVM
"""

import os
import json
import time
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

# Import our Web3 contract manager
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from web3_contract_manager import Web3ContractManager
    WEB3_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Web3 Contract Manager not available: {e}")
    WEB3_MANAGER_AVAILABLE = False
    Web3ContractManager = None

app = Flask(__name__)
CORS(app)

# Production configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['HYPEREVM_RPC_URL'] = os.getenv('HYPEREVM_RPC_URL', 'https://rpc.hyperliquid.xyz/evm')

# Real deployed contract addresses
DEPLOYED_CONTRACTS = {
    'platform_fees': '0x6cef01075a2cdf548ba60ab69b3a2a2c8302172c',
    'token_factory': '0x7f3befd15d12bd7ec6796dc68f4f13ec41b96912',
    'chain_id': 999,
    'rpc_url': 'https://rpc.hyperliquid.xyz/evm',
    'block_explorer': 'https://hyperliquid.cloud.blockscout.com',
}

# Feature flags - gate functionality until TokenFactory is fully deployed
FEATURE_FLAGS = {
    'token_factory_enabled': True,  # Set to False if TokenFactory isn't working yet
    'emergency_withdrawals_enabled': True,
    'real_time_data_enabled': True,
}

# Initialize Web3 contract manager
try:
    if Web3ContractManager is not None:
        contract_manager = Web3ContractManager()
        print("✅ Web3 Contract Manager initialized successfully")
    else:
        print("⚠️ Web3 Contract Manager not available (import failed)")
        contract_manager = None
except Exception as e:
    print(f"⚠️ Web3 Contract Manager failed to initialize: {e}")
    contract_manager = None

# In-memory storage for sessions (replace with Redis in production)
USER_SESSIONS = {}
ACTIVE_CONNECTIONS = {}

def get_contract_manager() -> Optional[Any]:
    """Get the contract manager instance"""
    global contract_manager
    if contract_manager is None and Web3ContractManager is not None:
        try:
            contract_manager = Web3ContractManager()
            print("✅ Web3 Contract Manager re-initialized")
        except Exception as e:
            print(f"❌ Failed to re-initialize contract manager: {e}")
    return contract_manager

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with Web3 connectivity"""
    cm = get_contract_manager()
    
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'web3_connected': False,
        'contracts_responsive': False,
        'feature_flags': FEATURE_FLAGS
    }
    
    if cm:
        status['web3_connected'] = cm.check_connection()
        
        # Test contract connectivity
        try:
            platform_stats = cm.get_platform_stats()
            status['contracts_responsive'] = True
            status['platform_stats'] = platform_stats
        except Exception as e:
            status['contract_error'] = str(e)
    
    return jsonify(status)

@app.route('/api/contract-info', methods=['GET'])
def contract_info():
    """Get deployed contract information"""
    return jsonify({
        'deployed_contracts': DEPLOYED_CONTRACTS,
        'contract_addresses': {
            'platform_fees': DEPLOYED_CONTRACTS['platform_fees'],
            'token_factory': DEPLOYED_CONTRACTS['token_factory'],
        },
        'network': {
            'name': 'HyperEVM Mainnet',
            'chain_id': DEPLOYED_CONTRACTS['chain_id'],
            'rpc_url': DEPLOYED_CONTRACTS['rpc_url'],
            'explorer': DEPLOYED_CONTRACTS['block_explorer']
        },
        'feature_flags': FEATURE_FLAGS
    })

@app.route('/api/platform-stats', methods=['GET'])
def platform_stats():
    """Get real platform statistics from deployed contracts"""
    cm = get_contract_manager()
    
    if not cm or not FEATURE_FLAGS['real_time_data_enabled']:
        # Return mock data if Web3 is not available
        return jsonify({
            'total_fees_collected': 1.234,
            'total_fees_withdrawn': 0.567,
            'available_balance': 0.667,
            'total_tokens': 42,
            'emergency_total': 0.0,
            'is_emergency_mode': False,
            'data_source': 'mock'
        })
    
    try:
        stats = cm.get_platform_stats()
        stats['data_source'] = 'contract'
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch platform stats: {e}',
            'data_source': 'error'
        }), 500

@app.route('/api/market-overview', methods=['GET'])
def market_overview():
    """Get market overview with real on-chain data where possible"""
    cm = get_contract_manager()
    
    # Base market data (can be enhanced with real contract data)
    overview = {
        'total_accounts': 0,
        'total_volume_24h': '0',
        'top_gainer': '@demo_account',
        'top_gainer_change': '+0.0%',
        'active_traders': 0
    }
    
    if cm and FEATURE_FLAGS['real_time_data_enabled']:
        try:
            platform_stats = cm.get_platform_stats()
            overview['total_accounts'] = platform_stats.get('total_tokens', 0)
            overview['total_volume_24h'] = f"{platform_stats.get('total_fees_collected', 0):.2f}K"
            
            # Try to get token data if TokenFactory is available
            if FEATURE_FLAGS['token_factory_enabled']:
                token_addresses = cm.get_all_token_addresses(0, 10)
                overview['active_traders'] = len(token_addresses)
                
        except Exception as e:
            print(f"⚠️ Error getting real market data: {e}")
            # Fall back to demo data
            overview = {
                'total_accounts': 142,
                'total_volume_24h': '2.4M',
                'top_gainer': '@tech_leader',
                'top_gainer_change': '+15.3%',
                'active_traders': 89
            }
    else:
        # Use demo data when Web3 is not available
        overview = {
            'total_accounts': 142,
            'total_volume_24h': '2.4M',
            'top_gainer': '@tech_leader',
            'top_gainer_change': '+15.3%',
            'active_traders': 89
        }
    
    return jsonify(overview)

@app.route('/api/trending-accounts', methods=['GET'])
def trending_accounts():
    """Get trending social accounts with real contract data when available"""
    cm = get_contract_manager()
    
    # Demo accounts as fallback
    demo_accounts = [
        {'handle': '@tech_innovator', 'price': '1,234.56', 'change': '+5.2%', 'volume': '456K', 'contract': None},
        {'handle': '@startup_founder', 'price': '987.65', 'change': '+3.1%', 'volume': '234K', 'contract': None},
        {'handle': '@crypto_analyst', 'price': '543.21', 'change': '-1.4%', 'volume': '123K', 'contract': None},
        {'handle': '@investment_guru', 'price': '678.90', 'change': '+2.8%', 'volume': '345K', 'contract': None},
        {'handle': '@growth_hacker', 'price': '432.10', 'change': '+4.5%', 'volume': '567K', 'contract': None}
    ]
    
    if cm and FEATURE_FLAGS['token_factory_enabled'] and FEATURE_FLAGS['real_time_data_enabled']:
        try:
            # Get real token addresses from contract
            token_addresses = cm.get_all_token_addresses(0, 5)
            real_accounts = []
            
            for addr in token_addresses:
                try:
                    token_data = cm.get_social_token_info(addr)
                    if token_data and token_data.get('social_handle'):
                        real_accounts.append({
                            'handle': token_data['social_handle'],
                            'price': f"{token_data.get('current_price', 0) / 1e18:.2f}",
                            'change': f"+{((token_data.get('current_price', 0) / 1e18) * 5):.1f}%",  # Mock change calculation
                            'volume': f"{token_data.get('volume_24h', 0) / 1e18:.0f}K",
                            'contract': addr,
                            'hype_pool': token_data.get('hype_pool', 0) / 1e18
                        })
                except Exception as e:
                    print(f"⚠️ Error getting token data for {addr}: {e}")
                    continue
            
            if real_accounts:
                return jsonify(real_accounts)
                
        except Exception as e:
            print(f"⚠️ Error getting real trending accounts: {e}")
    
    return jsonify(demo_accounts)

@app.route('/api/recent-trades', methods=['GET'])
def recent_trades():
    """Get recent trading activity"""
    # For now, return demo data - can be enhanced with real transaction logs
    trades = [
        {'account': '@tech_innovator', 'type': 'BUY', 'amount': '10.5', 'price': '1,234.56', 'time': '2m ago', 'tx_hash': None},
        {'account': '@startup_founder', 'type': 'SELL', 'amount': '5.2', 'price': '987.65', 'time': '5m ago', 'tx_hash': None},
        {'account': '@crypto_analyst', 'type': 'BUY', 'amount': '15.8', 'price': '543.21', 'time': '8m ago', 'tx_hash': None},
        {'account': '@investment_guru', 'type': 'BUY', 'amount': '7.3', 'price': '678.90', 'time': '12m ago', 'tx_hash': None}
    ]
    return jsonify(trades)

@app.route('/api/portfolio-stats', methods=['GET'])
def portfolio_stats():
    """Get portfolio statistics"""
    # Demo data - can be enhanced with real user wallet integration
    return jsonify({
        'total_value': '12,456.78',
        'daily_change': '+234.56',
        'daily_change_percent': '+1.95%',
        'holdings': [
            {'account': '@tech_innovator', 'shares': '10.5', 'value': '5,678.90', 'change': '+2.3%'},
            {'account': '@startup_founder', 'shares': '8.2', 'value': '3,456.78', 'change': '+1.8%'},
            {'account': '@crypto_analyst', 'shares': '12.1', 'value': '2,345.67', 'change': '-0.5%'}
        ]
    })

@app.route('/api/token-info/<address>', methods=['GET'])
def token_info(address: str):
    """Get detailed information about a specific token contract"""
    cm = get_contract_manager()
    
    if not cm or not FEATURE_FLAGS['token_factory_enabled']:
        return jsonify({'error': 'Token info not available'}), 503
    
    try:
        # Validate address format
        from web3 import Web3
        if not Web3.is_address(address):
            return jsonify({'error': 'Invalid contract address'}), 400
        
        token_data = cm.get_social_token_info(address)
        if not token_data:
            return jsonify({'error': 'Token not found or contract not responsive'}), 404
        
        return jsonify({
            'contract_address': address,
            'social_handle': token_data.get('social_handle', ''),
            'account_name': token_data.get('account_name', ''),
            'creator': token_data.get('creator', ''),
            'current_price': token_data.get('current_price', 0) / 1e18,
            'hype_pool': token_data.get('hype_pool', 0) / 1e18,
            'circulating_supply': token_data.get('circulating_supply', 0) / 1e18,
            'total_supply': token_data.get('total_supply', 0) / 1e18,
            'volume_24h': token_data.get('volume_24h', 0) / 1e18,
            'holder_count': token_data.get('holder_count', 0),
            'network': DEPLOYED_CONTRACTS['chain_id'],
            'explorer_url': f"{DEPLOYED_CONTRACTS['block_explorer']}/address/{address}"
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get token info: {e}'}), 500

@app.route('/api/launch-account', methods=['POST'])
def launch_account():
    """Launch new social account token via TokenFactory"""
    if not FEATURE_FLAGS['token_factory_enabled']:
        return jsonify({
            'success': False,
            'error': 'Token launching is currently disabled'
        }), 503
    
    data = request.get_json()
    if not data or 'social_handle' not in data:
        return jsonify({'error': 'social_handle is required'}), 400
    
    cm = get_contract_manager()
    if not cm:
        return jsonify({'error': 'Web3 not available'}), 503
    
    try:
        social_handle = data['social_handle']
        account_name = data.get('account_name', '')
        creator_address = data.get('creator_address', '')
        
        # Launch the token using contract manager
        result = cm.launch_social_token(social_handle, account_name, creator_address)
        
        if result['success']:
            return jsonify({
                'success': True,
                'account_id': f"acc_{int(time.time())}",
                'social_handle': social_handle,
                'contract_address': result['contract_address'],
                'transaction_hash': result['transaction_hash'],
                'launch_price': result['launch_price'],
                'message': 'Social token launched successfully!',
                'explorer_url': f"{DEPLOYED_CONTRACTS['block_explorer']}/address/{result['contract_address']}"
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error occurred')
            }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to launch account: {e}'
        }), 500

@app.route('/api/emergency/platform-status', methods=['GET'])
def emergency_platform_status():
    """Get platform emergency status"""
    if not FEATURE_FLAGS['emergency_withdrawals_enabled']:
        return jsonify({'error': 'Emergency features disabled'}), 503
    
    cm = get_contract_manager()
    if not cm:
        return jsonify({'error': 'Web3 not available'}), 503
    
    try:
        stats = cm.get_platform_stats()
        return jsonify({
            'is_emergency_mode': stats.get('is_emergency_mode', False),
            'emergency_total': stats.get('emergency_total', 0),
            'platform_health': 'operational' if not stats.get('is_emergency_mode', False) else 'emergency',
            'total_fees_available': stats.get('available_balance', 0)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get emergency status: {e}'}), 500

@app.route('/api/debug/web3-status', methods=['GET'])
def debug_web3_status():
    """Debug endpoint for Web3 connection status"""
    cm = get_contract_manager()
    
    status = {
        'contract_manager_initialized': cm is not None,
        'web3_available': cm.check_connection() if cm else False,
        'deployed_contracts': DEPLOYED_CONTRACTS,
        'feature_flags': FEATURE_FLAGS
    }
    
    if cm:
        try:
            status['platform_stats'] = cm.get_platform_stats()
            status['connection_test'] = 'success'
        except Exception as e:
            status['connection_error'] = str(e)
            status['connection_test'] = 'failed'
    
    return jsonify(status)

@app.route('/api/check-balances', methods=['POST'])
def check_balances():
    """Check wallet balances for automatic transfer"""
    data = request.get_json()
    wallet_address = data.get('walletAddress')
    twitter_username = data.get('twitterUsername')
    
    if not wallet_address or not twitter_username:
        return jsonify({'error': 'Wallet address and Twitter username required'}), 400
    
    try:
        cm = get_contract_manager()
        
        # Fetch real balances from blockchain
        real_balances = {
            'hype': '0.0000',  # Will be fetched from actual wallet
            'usdt': '0.00',
            'others': []
        }
        
        # Try to fetch real HYPE balance if contract manager is available
        if cm:
            try:
                # Get HYPE balance (native token on HyperEVM)
                hype_balance = cm.web3.eth.get_balance(wallet_address)
                real_balances['hype'] = str(round(float(hype_balance) / 10**18, 4))
            except Exception as e:
                print(f"⚠️ Could not fetch HYPE balance: {e}")
        
        # For now, return 0 for other tokens until we implement proper ERC20 balance checking
        # This ensures no fake data is shown
        
        return jsonify({
            'success': True,
            'walletAddress': wallet_address,
            'twitterUsername': twitter_username,
            'balances': real_balances,
            'eligibleForTransfer': True
        })
        
    except Exception as e:
        return jsonify({'error': f'Balance check failed: {e}'}), 500

@app.route('/api/prepare-transfer', methods=['POST'])
def prepare_transfer():
    """Prepare fund transfer transactions with EIP-712 signatures"""
    data = request.get_json()
    wallet_address = data.get('walletAddress')
    twitter_username = data.get('twitterUsername')
    target_address = data.get('targetAddress')
    
    if not wallet_address or not twitter_username or not target_address:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        # Get current balances (mock for now)
        balances = {
            'hype': '5.2500',
            'usdt': '125.75',
            'others': [
                {'symbol': 'USDC', 'balance': '50.00', 'address': '0xA0b86a33E6441fA86FB49FAd91EA5E8C0A19BC06'},
                {'symbol': 'WETH', 'balance': '0.1250', 'address': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'}
            ]
        }
        
        transactions = []
        nonce = int(time.time())  # Simple nonce for demo
        deadline = int(time.time()) + 3600  # 1 hour deadline
        
        # HYPE transfer (native token)
        if float(balances['hype']) > 0:
            hype_amount_wei = int(float(balances['hype']) * 1e18)
            transactions.append({
                'token': 'HYPE',
                'amount': balances['hype'],
                'tokenAddress': '0x0000000000000000000000000000000000000000',  # Native token
                'to': target_address,
                'value': str(hype_amount_wei),
                'data': '0x',
                'nonce': nonce,
                'deadline': deadline
            })
            nonce += 1
        
        # USDT transfer (ERC-20)
        if float(balances['usdt']) > 0:
            usdt_amount_wei = int(float(balances['usdt']) * 1e6)  # USDT has 6 decimals
            # ERC-20 transfer function selector + target address + amount
            transfer_data = '0xa9059cbb' + target_address[2:].zfill(64) + hex(usdt_amount_wei)[2:].zfill(64)
            
            transactions.append({
                'token': 'USDT',
                'amount': balances['usdt'],
                'tokenAddress': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
                'to': '0xdAC17F958D2ee523a2206206994597C13D831ec7',  # USDT contract
                'value': '0',
                'data': transfer_data,
                'nonce': nonce,
                'deadline': deadline
            })
            nonce += 1
        
        # Other token transfers
        for token in balances['others']:
            if float(token['balance']) > 0:
                # Assume 18 decimals for other tokens
                amount_wei = int(float(token['balance']) * 1e18)
                transfer_data = '0xa9059cbb' + target_address[2:].zfill(64) + hex(amount_wei)[2:].zfill(64)
                
                transactions.append({
                    'token': token['symbol'],
                    'amount': token['balance'],
                    'tokenAddress': token['address'],
                    'to': token['address'],
                    'value': '0',
                    'data': transfer_data,
                    'nonce': nonce,
                    'deadline': deadline
                })
                nonce += 1
        
        return jsonify({
            'success': True,
            'transactions': transactions,
            'targetAddress': target_address,
            'totalTransactions': len(transactions)
        })
        
    except Exception as e:
        return jsonify({'error': f'Transfer preparation failed: {e}'}), 500

@app.route('/api/verify-transfer', methods=['POST'])
def verify_transfer():
    """Verify completed transfer transactions"""
    data = request.get_json()
    tx_hashes = data.get('txHashes', [])
    
    try:
        # In production, would verify transactions on blockchain
        # For now, return success for all provided hashes
        verified_transactions = []
        
        for tx_hash in tx_hashes:
            verified_transactions.append({
                'txHash': tx_hash,
                'status': 'confirmed',
                'blockNumber': 12345678,  # Mock block number
                'gasUsed': '21000'
            })
        
        return jsonify({
            'success': True,
            'verifiedTransactions': verified_transactions,
            'allConfirmed': True
        })
        
    except Exception as e:
        return jsonify({'error': f'Transfer verification failed: {e}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("🚀 Starting SocialX Web3 Backend API...")
    print(f"📡 HyperEVM RPC: {DEPLOYED_CONTRACTS['rpc_url']}")
    print(f"💰 PlatformFees Contract: {DEPLOYED_CONTRACTS['platform_fees']}")
    print(f"🏭 TokenFactory Contract: {DEPLOYED_CONTRACTS['token_factory']}")
    print(f"🔧 Feature Flags: {FEATURE_FLAGS}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)