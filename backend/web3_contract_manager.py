#!/usr/bin/env python3
"""
Web3 Contract Manager for SocialX Trading Platform
Handles smart contract interactions and fallback data management
"""

import os
import time
import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

try:
    from web3 import Web3
    from web3.middleware import geth_poa_middleware
    WEB3_AVAILABLE = True
except ImportError:
    print("⚠️ Web3.py not available. Install with: pip install web3")
    WEB3_AVAILABLE = False
    Web3 = None

class Web3ContractManager:
    """
    Manages Web3 contract interactions with fallback to in-memory storage
    """
    
    def __init__(self):
        self.rpc_url = os.getenv('HYPEREVM_RPC_URL', 'https://rpc.hyperliquid.xyz/evm')
        self.chain_id = 999
        self.web3 = None
        self.is_connected = False
        
        # Contract addresses
        self.platform_fees_address = '0x6cef01075a2cdf548ba60ab69b3a2a2c8302172c'
        self.token_factory_address = '0x7f3befd15d12bd7ec6796dc68f4f13ec41b96912'
        
        # In-memory storage for launched tokens (temporary solution)
        self.launched_tokens = {}
        self.token_counter = 0
        self.platform_stats_cache = {
            'total_fees_collected': 2.458,
            'total_fees_withdrawn': 1.123,
            'available_balance': 1.335,
            'total_tokens': 0,
            'emergency_total': 0.0,
            'is_emergency_mode': False,
            'last_updated': time.time()
        }
        
        # Initialize Web3 connection
        self._initialize_web3()
        
        # Load demo tokens for testing
        self._load_demo_tokens()
    
    def _initialize_web3(self):
        """Initialize Web3 connection to HyperEVM"""
        if not WEB3_AVAILABLE:
            print("⚠️ Web3 not available, using fallback mode")
            return
        
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
            
            # Add PoA middleware for compatibility
            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Test connection
            if self.web3.is_connected():
                latest_block = self.web3.eth.block_number
                self.is_connected = True
                print(f"✅ Connected to HyperEVM (block: {latest_block})")
            else:
                print("⚠️ Web3 connection failed, using fallback mode")
                
        except Exception as e:
            print(f"⚠️ Web3 initialization failed: {e}")
            self.web3 = None
            self.is_connected = False
    
    def _load_demo_tokens(self):
        """Load some demo tokens for testing"""
        demo_tokens = [
            {
                'social_handle': '@tech_innovator',
                'account_name': 'Tech Innovator',
                'creator': '0x742d35Cc6635C0532925a3b8D5c5d8e6b8C3e6E7',
                'hype_pool': int(1234.56 * 1e18),
                'current_price': int(1.2345 * 1e18),
                'volume_24h': int(456.78 * 1e18)
            },
            {
                'social_handle': '@startup_founder',
                'account_name': 'Startup Founder', 
                'creator': '0x8f9A7B2C1D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A',
                'hype_pool': int(987.65 * 1e18),
                'current_price': int(0.9876 * 1e18),
                'volume_24h': int(234.56 * 1e18)
            },
            {
                'social_handle': '@crypto_analyst',
                'account_name': 'Crypto Analyst',
                'creator': '0x1A2B3C4D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B',
                'hype_pool': int(543.21 * 1e18),
                'current_price': int(0.5432 * 1e18),
                'volume_24h': int(123.45 * 1e18)
            }
        ]
        
        for i, token_data in enumerate(demo_tokens):
            address = self._generate_mock_address(token_data['social_handle'])
            self.launched_tokens[address] = {
                **token_data,
                'contract_address': address,
                'circulating_supply': int(1000000 * 1e18),
                'total_supply': int(1000000 * 1e18),
                'holder_count': 50 + i * 20,
                'launch_time': time.time() - (i * 86400),  # Launched i days ago
                'launch_price': int(0.1 * 1e18)
            }
        
        self.token_counter = len(demo_tokens)
        self.platform_stats_cache['total_tokens'] = len(self.launched_tokens)
        print(f"📦 Loaded {len(demo_tokens)} demo tokens")
    
    def _generate_mock_address(self, social_handle: str) -> str:
        """Generate a consistent mock address for a social handle"""
        hash_input = f"socialx_token_{social_handle}_{self.chain_id}"
        hash_hex = hashlib.sha256(hash_input.encode()).hexdigest()
        return f"0x{hash_hex[:40]}"
    
    def check_connection(self) -> bool:
        """Check if Web3 connection is active"""
        if not self.web3:
            return False
        
        try:
            # Test with a simple call
            self.web3.eth.block_number
            self.is_connected = True
            return True
        except Exception as e:
            print(f"⚠️ Web3 connection test failed: {e}")
            self.is_connected = False
            return False
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get platform statistics (from cache or contracts)"""
        try:
            # Update total tokens count
            self.platform_stats_cache['total_tokens'] = len(self.launched_tokens)
            self.platform_stats_cache['last_updated'] = time.time()
            
            # If Web3 is available, try to get real fee data
            if self.is_connected and self.web3:
                try:
                    # In a real implementation, would call contract methods here
                    # For now, just simulate slight variations
                    time_factor = time.time() % 100
                    self.platform_stats_cache['total_fees_collected'] += time_factor * 0.001
                    
                except Exception as e:
                    print(f"⚠️ Could not fetch real platform stats: {e}")
            
            return self.platform_stats_cache.copy()
            
        except Exception as e:
            print(f"❌ Error getting platform stats: {e}")
            return {
                'total_fees_collected': 0.0,
                'total_fees_withdrawn': 0.0,
                'available_balance': 0.0,
                'total_tokens': 0,
                'emergency_total': 0.0,
                'is_emergency_mode': False,
                'error': str(e)
            }
    
    def get_all_token_addresses(self, start: int = 0, limit: int = 10) -> List[str]:
        """Get all launched token addresses"""
        try:
            addresses = list(self.launched_tokens.keys())
            
            # Sort by launch time (newest first)
            addresses.sort(key=lambda addr: self.launched_tokens[addr].get('launch_time', 0), reverse=True)
            
            # Apply pagination
            end = start + limit
            return addresses[start:end]
            
        except Exception as e:
            print(f"❌ Error getting token addresses: {e}")
            return []
    
    def get_social_token_info(self, address: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a social token"""
        try:
            if address not in self.launched_tokens:
                return None
            
            token_data = self.launched_tokens[address].copy()
            
            # Add calculated fields
            launch_time = token_data.get('launch_time', time.time())
            time_since_launch = time.time() - launch_time
            
            # Simulate price appreciation over time (mock data)
            launch_price = token_data.get('launch_price', int(0.1 * 1e18))
            appreciation_factor = 1 + (time_since_launch / 86400) * 0.1  # 10% per day
            token_data['current_price'] = int(launch_price * appreciation_factor)
            
            # Simulate volume based on time
            base_volume = token_data.get('volume_24h', int(100 * 1e18))
            volume_factor = 1 + (time_since_launch / 3600) * 0.05  # Increases with time
            token_data['volume_24h'] = int(base_volume * volume_factor)
            
            return token_data
            
        except Exception as e:
            print(f"❌ Error getting token info for {address}: {e}")
            return None
    
    def launch_social_token(self, social_handle: str, account_name: str = "", creator_address: str = "") -> Dict[str, Any]:
        """Launch a new social token (adds to in-memory storage)"""
        try:
            # Generate a consistent address for this social handle
            contract_address = self._generate_mock_address(social_handle)
            
            # Check if already exists
            if contract_address in self.launched_tokens:
                return {
                    'success': False,
                    'error': f'Token for {social_handle} already exists',
                    'existing_address': contract_address
                }
            
            # Create new token data
            launch_price = int(0.1 * 1e18)  # 0.1 HYPE launch price
            initial_supply = int(1000000 * 1e18)  # 1M tokens
            
            token_data = {
                'contract_address': contract_address,
                'social_handle': social_handle,
                'account_name': account_name or social_handle.replace('@', '').title(),
                'creator': creator_address or f"0x{hashlib.sha256(social_handle.encode()).hexdigest()[:40]}",
                'launch_time': time.time(),
                'launch_price': launch_price,
                'current_price': launch_price,
                'hype_pool': int(100 * 1e18),  # Initial 100 HYPE in pool
                'circulating_supply': initial_supply,
                'total_supply': initial_supply,
                'volume_24h': 0,
                'holder_count': 1,  # Creator starts with tokens
            }
            
            # Store in memory
            self.launched_tokens[contract_address] = token_data
            self.token_counter += 1
            
            # Update platform stats
            self.platform_stats_cache['total_tokens'] = len(self.launched_tokens)
            
            print(f"🚀 Launched token for {social_handle} at {contract_address}")
            
            return {
                'success': True,
                'contract_address': contract_address,
                'social_handle': social_handle,
                'account_name': token_data['account_name'],
                'launch_price': launch_price / 1e18,
                'transaction_hash': f"0x{hashlib.sha256(f'{social_handle}_{time.time()}'.encode()).hexdigest()}",
                'block_number': 12345678 + self.token_counter,
                'gas_used': '152000'
            }
            
        except Exception as e:
            print(f"❌ Error launching token for {social_handle}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_token_by_handle(self, social_handle: str) -> Optional[Dict[str, Any]]:
        """Get token information by social handle"""
        try:
            for address, token_data in self.launched_tokens.items():
                if token_data.get('social_handle', '').lower() == social_handle.lower():
                    return self.get_social_token_info(address)
            return None
        except Exception as e:
            print(f"❌ Error getting token by handle {social_handle}: {e}")
            return None
    
    def simulate_trading_activity(self):
        """Simulate some trading activity for demo purposes"""
        try:
            for address, token_data in self.launched_tokens.items():
                # Simulate random price movements
                current_price = token_data.get('current_price', int(0.1 * 1e18))
                price_change = int(current_price * 0.01 * (0.5 - time.time() % 1))  # ±1% random walk
                new_price = max(int(0.01 * 1e18), current_price + price_change)  # Min 0.01 HYPE
                
                # Update price and volume
                self.launched_tokens[address]['current_price'] = new_price
                self.launched_tokens[address]['volume_24h'] += int(abs(price_change) * 10)
                
        except Exception as e:
            print(f"⚠️ Error simulating trading activity: {e}")
    
    def get_user_portfolio(self, user_address: str) -> Dict[str, Any]:
        """Get user's token portfolio (mock data for now)"""
        try:
            # In a real implementation, would query token balances for user
            # For demo, return some holdings in launched tokens
            
            portfolio = {
                'total_value_hype': 0,
                'holdings': [],
                'total_tokens': 0
            }
            
            # Mock some holdings in the first few tokens
            token_addresses = list(self.launched_tokens.keys())[:3]
            
            for i, address in enumerate(token_addresses):
                token_data = self.launched_tokens[address]
                balance = (10 - i * 2) * 1e18  # Mock decreasing holdings
                value = balance * token_data['current_price'] / 1e18
                
                portfolio['holdings'].append({
                    'token_address': address,
                    'social_handle': token_data['social_handle'],
                    'balance': balance / 1e18,
                    'value_hype': value / 1e18,
                    'price': token_data['current_price'] / 1e18
                })
                
                portfolio['total_value_hype'] += value / 1e18
                portfolio['total_tokens'] += 1
            
            return portfolio
            
        except Exception as e:
            print(f"❌ Error getting user portfolio: {e}")
            return {'total_value_hype': 0, 'holdings': [], 'total_tokens': 0}

    def emergency_withdraw_all(self) -> Dict[str, Any]:
        """Emergency withdrawal simulation"""
        try:
            if not FEATURE_FLAGS.get('emergency_withdrawals_enabled', False):
                return {'success': False, 'error': 'Emergency withdrawals disabled'}
            
            total_withdrawn = self.platform_stats_cache.get('available_balance', 0)
            
            # Simulate withdrawal
            self.platform_stats_cache['emergency_total'] = total_withdrawn
            self.platform_stats_cache['available_balance'] = 0
            self.platform_stats_cache['is_emergency_mode'] = True
            
            return {
                'success': True,
                'amount_withdrawn': total_withdrawn,
                'transaction_hash': f"0x{hashlib.sha256(f'emergency_{time.time()}'.encode()).hexdigest()}",
                'emergency_mode_activated': True
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Global feature flags (can be imported by other modules)
FEATURE_FLAGS = {
    'token_factory_enabled': True,
    'emergency_withdrawals_enabled': True,
    'real_time_data_enabled': True,
    'trading_enabled': True,
    'portfolio_tracking_enabled': True
}

def get_feature_flags() -> Dict[str, bool]:
    """Get current feature flags"""
    return FEATURE_FLAGS.copy()

if __name__ == "__main__":
    # Test the contract manager
    print("🔧 Testing Web3ContractManager...")
    
    manager = Web3ContractManager()
    
    # Test connection
    print(f"Connection status: {manager.check_connection()}")
    
    # Test platform stats
    stats = manager.get_platform_stats()
    print(f"Platform stats: {stats}")
    
    # Test token listing
    addresses = manager.get_all_token_addresses(0, 5)
    print(f"Token addresses: {addresses}")
    
    # Test token info
    if addresses:
        info = manager.get_social_token_info(addresses[0])
        print(f"Token info: {info}")
    
    # Test token launch
    result = manager.launch_social_token('@test_user', 'Test User')
    print(f"Launch result: {result}")
    
    print("✅ Web3ContractManager test completed")