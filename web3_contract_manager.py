#!/usr/bin/env python3
"""
Web3 Contract Manager for SocialX Platform
Handles interactions with deployed smart contracts on HyperEVM
"""

import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    from web3 import Web3
    WEB3_AVAILABLE = True
except ImportError:
    print("⚠️ Web3 not available, using mock responses")
    WEB3_AVAILABLE = False
    class Web3:
        @staticmethod
        def HTTPProvider(url):
            return None
        @staticmethod
        def to_checksum_address(addr):
            return addr
        class eth:
            @staticmethod
            def contract(address, abi):
                return MockContract()
            block_number = 123456
    
    class MockContract:
        def __init__(self):
            self.functions = MockFunctions()
    
    class MockFunctions:
        def getPlatformStats(self):
            return MockCall([0, 0, 0, 0, 0, False])
        def getAllTokenContracts(self, offset, limit):
            return MockCall([])
        def getTokenContract(self, handle):
            return MockCall('0x0000000000000000000000000000000000000000')
        def getSocialHandle(self, addr):
            return MockCall('')
        def getTotalTokensLaunched(self):
            return MockCall(0)
        def getCreatorTokens(self, creator):
            return MockCall([])
        def socialHandle(self):
            return MockCall('mock_handle')
        def accountName(self):
            return MockCall('Mock Account')
        def creator(self):
            return MockCall('0x0000000000000000000000000000000000000000')
        def getCurrentPrice(self):
            return MockCall(0)
        def hypePool(self):
            return MockCall(0)
        def circulatingSupply(self):
            return MockCall(0)
        def totalSupply(self):
            return MockCall(1000000000000000000000000000)
        def volume24h(self):
            return MockCall(0)
        def holderCount(self):
            return MockCall(0)
    
    class MockCall:
        def __init__(self, result):
            self.result = result
        def call(self):
            return self.result

class Web3ContractManager:
    def __init__(self):
        # HyperEVM Configuration
        self.rpc_url = "https://rpc.hyperliquid.xyz/evm"
        self.chain_id = 999
        
        # Real deployed contract addresses
        self.contracts = {
            'platform_fees': '0x6cef01075a2cdf548ba60ab69b3a2a2c8302172c',
            'token_factory': '0x7f3befd15d12bd7ec6796dc68f4f13ec41b96912',
            'whype_token': '0x5555555555555555555555555555555555555555',  # WHYPE token address
        }
        
        # Initialize Web3 connection
        if WEB3_AVAILABLE:
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        else:
            self.w3 = Web3()
        
        # Load canonical ABIs from compiled artifacts
        self.platform_fees_abi = self._load_platform_fees_abi()
        self.token_factory_abi = self._load_token_factory_abi()
        
        
        self.social_token_abi = [
            {
                "inputs": [],
                "name": "socialHandle",
                "outputs": [{"name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "accountName",
                "outputs": [{"name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "creator",
                "outputs": [{"name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getCurrentPrice",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "hypePool",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "circulatingSupply",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "volume24h",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "holderCount",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        # Use checksummed addresses for contract instances
        if WEB3_AVAILABLE:
            platform_fees_address = self.w3.to_checksum_address(self.contracts['platform_fees'])
            token_factory_address = self.w3.to_checksum_address(self.contracts['token_factory'])
        else:
            platform_fees_address = self.contracts['platform_fees']
            token_factory_address = self.contracts['token_factory']
        
        # Initialize contract instances
        self.platform_fees_contract = self.w3.eth.contract(
            address=platform_fees_address,
            abi=self.platform_fees_abi
        )
        
        self.token_factory_contract = self.w3.eth.contract(
            address=token_factory_address,
            abi=self.token_factory_abi
        )
        
        # Perform health check on initialization
        self._perform_health_check()
        
    def _load_platform_fees_abi(self) -> list:
        """Load canonical PlatformFees ABI from compiled artifacts"""
        try:
            with open('artifacts/contracts/PlatformFees.sol/PlatformFees.json', 'r') as f:
                artifact = json.load(f)
                return artifact['abi']
        except Exception as e:
            print(f"⚠️ Failed to load PlatformFees ABI: {e}")
            # Return minimal fallback ABI
            return [{
                "inputs": [],
                "name": "getPlatformStats",
                "outputs": [
                    {"internalType": "uint256", "name": "totalFees", "type": "uint256"},
                    {"internalType": "uint256", "name": "withdrawnFees", "type": "uint256"},
                    {"internalType": "uint256", "name": "availableBalance", "type": "uint256"},
                    {"internalType": "uint256", "name": "totalTokens", "type": "uint256"},
                    {"internalType": "uint256", "name": "emergencyTotal", "type": "uint256"},
                    {"internalType": "bool", "name": "isEmergencyMode", "type": "bool"}
                ],
                "stateMutability": "view",
                "type": "function"
            }]
    
    def _load_token_factory_abi(self) -> list:
        """Load canonical TokenFactory ABI from compiled artifacts"""
        try:
            with open('artifacts/contracts/TokenFactory.sol/TokenFactory.json', 'r') as f:
                artifact = json.load(f)
                return artifact['abi']
        except Exception as e:
            print(f"⚠️ Failed to load TokenFactory ABI: {e}")
            # Return minimal fallback ABI
            return [{
                "inputs": [{"internalType": "string", "name": "socialHandle", "type": "string"}],
                "name": "getTokenContract",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function"
            }]
    
    def _perform_health_check(self):
        """Perform health check on Web3 connection and contracts"""
        if not WEB3_AVAILABLE:
            print("⚠️ Web3 not available - running in mock mode")
            return
            
        try:
            # Check RPC connection
            block_number = self.w3.eth.block_number
            print(f"✅ Connected to HyperEVM. Latest block: {block_number}")
            
            # Verify chain ID
            chain_id = self.w3.eth.chain_id
            if chain_id != self.chain_id:
                print(f"⚠️ Chain ID mismatch: expected {self.chain_id}, got {chain_id}")
            else:
                print(f"✅ Chain ID verified: {chain_id}")
            
            # Test contract connectivity
            try:
                stats = self.platform_fees_contract.functions.getPlatformStats().call()
                print(f"✅ PlatformFees contract responsive")
            except Exception as e:
                print(f"❌ PlatformFees contract error: {e}")
            
            try:
                total_tokens = self.token_factory_contract.functions.getTotalTokensLaunched().call()
                print(f"✅ TokenFactory contract responsive, {total_tokens} tokens launched")
            except Exception as e:
                print(f"❌ TokenFactory contract error: {e}")
                
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    def check_connection(self) -> bool:
        """Check if Web3 connection is working"""
        if not WEB3_AVAILABLE:
            return False
            
        try:
            block_number = self.w3.eth.block_number
            chain_id = self.w3.eth.chain_id
            return block_number > 0 and chain_id == self.chain_id
        except Exception as e:
            print(f"❌ Connection check failed: {e}")
            return False
    
    def get_platform_stats(self) -> Dict:
        """Get platform-wide statistics from PlatformFees contract"""
        try:
            stats = self.platform_fees_contract.functions.getPlatformStats().call()
            return {
                'total_fees_collected': stats[0] / 1e18,  # Convert from wei
                'total_fees_withdrawn': stats[1] / 1e18,
                'available_balance': stats[2] / 1e18,
                'total_tokens': stats[3],
                'emergency_total': stats[4] / 1e18,
                'is_emergency_mode': stats[5]
            }
        except Exception as e:
            print(f"❌ Error getting platform stats: {e}")
            return {
                'total_fees_collected': 0,
                'total_fees_withdrawn': 0,
                'available_balance': 0,
                'total_tokens': 0,
                'emergency_total': 0,
                'is_emergency_mode': False
            }
    
    def get_all_token_addresses(self, offset: int = 0, limit: int = 100) -> List[str]:
        """Get all token contract addresses from TokenFactory"""
        try:
            addresses = self.token_factory_contract.functions.getAllTokenContracts(offset, limit).call()
            return [self.w3.to_checksum_address(addr) for addr in addresses]
        except Exception as e:
            print(f"❌ Error getting token addresses: {e}")
            return []
    
    def get_token_by_handle(self, handle: str) -> Optional[str]:
        """Get token contract address by social handle"""
        try:
            address = self.token_factory_contract.functions.getTokenContract(handle).call()
            if address == '0x0000000000000000000000000000000000000000':
                return None
            return self.w3.to_checksum_address(address)
        except Exception as e:
            print(f"❌ Error getting token by handle {handle}: {e}")
            return None
    
    def get_handle_by_token(self, token_address: str) -> Optional[str]:
        """Get social handle by token contract address"""
        try:
            handle = self.token_factory_contract.functions.getSocialHandle(token_address).call()
            return handle if handle else None
        except Exception as e:
            print(f"❌ Error getting handle by token {token_address}: {e}")
            return None
    
    def get_token_data(self, token_address: str) -> Dict:
        """Get comprehensive data for a specific token"""
        try:
            # Create contract instance for this token
            token_contract = self.w3.eth.contract(
                address=token_address,
                abi=self.social_token_abi
            )
            
            # Fetch all token data
            handle = token_contract.functions.socialHandle().call()
            name = token_contract.functions.accountName().call()
            creator = token_contract.functions.creator().call()
            current_price = token_contract.functions.getCurrentPrice().call()
            hype_pool = token_contract.functions.hypePool().call()
            circulating_supply = token_contract.functions.circulatingSupply().call()
            total_supply = token_contract.functions.totalSupply().call()
            volume_24h = token_contract.functions.volume24h().call()
            holder_count = token_contract.functions.holderCount().call()
            
            # Calculate market cap
            market_cap = (current_price * total_supply) / 1e36  # Adjust for decimals
            
            return {
                'address': token_address,
                'handle': handle,
                'name': name,
                'creator': creator,
                'current_price': current_price / 1e18,  # Convert from wei
                'hype_pool': hype_pool / 1e18,
                'circulating_supply': circulating_supply / 1e18,
                'total_supply': total_supply / 1e18,
                'market_cap': market_cap,
                'volume_24h': volume_24h / 1e18,
                'holder_count': holder_count,
                'chain_id': self.chain_id,
                'network': 'HyperEVM'
            }
        except Exception as e:
            print(f"❌ Error getting token data for {token_address}: {e}")
            return {}
    
    def get_trending_tokens(self, limit: int = 10) -> List[Dict]:
        """Get trending tokens based on volume"""
        try:
            # Get all token addresses
            token_addresses = self.get_all_token_addresses(0, 100)
            
            # Get data for each token
            tokens_data = []
            for address in token_addresses[:limit]:  # Limit to avoid too many calls
                token_data = self.get_token_data(address)
                if token_data:
                    tokens_data.append(token_data)
            
            # Sort by volume (descending)
            trending = sorted(tokens_data, key=lambda x: x.get('volume_24h', 0), reverse=True)
            return trending[:limit]
            
        except Exception as e:
            print(f"❌ Error getting trending tokens: {e}")
            return []
    
    def get_creator_tokens(self, creator_address: str) -> List[str]:
        """Get all token addresses created by a specific creator"""
        try:
            addresses = self.token_factory_contract.functions.getCreatorTokens(creator_address).call()
            return [self.w3.to_checksum_address(addr) for addr in addresses]
        except Exception as e:
            print(f"❌ Error getting creator tokens for {creator_address}: {e}")
            return []
    
    def get_total_tokens_launched(self) -> int:
        """Get total number of tokens launched on the platform"""
        try:
            return self.token_factory_contract.functions.getTotalTokensLaunched().call()
        except Exception as e:
            print(f"❌ Error getting total tokens launched: {e}")
            return 0
    
    def simulate_buy_price(self, token_address: str, hype_amount: float) -> Dict:
        """Simulate a buy transaction to get expected tokens and price impact"""
        try:
            # This would require a more complex calculation based on the bonding curve
            # For now, return a simple estimate
            token_data = self.get_token_data(token_address)
            if not token_data:
                return {'error': 'Token not found'}
            
            current_price = token_data['current_price']
            estimated_tokens = hype_amount / current_price
            
            return {
                'hype_amount': hype_amount,
                'estimated_tokens': estimated_tokens,
                'current_price': current_price,
                'price_impact': 0.0,  # Would need bonding curve calculation
                'slippage': 0.0
            }
        except Exception as e:
            print(f"❌ Error simulating buy price: {e}")
            return {'error': str(e)}
    
    def get_recent_transactions(self, token_address: str, limit: int = 10) -> List[Dict]:
        """Get recent transactions for a token (would need event filtering)"""
        # This would require filtering blockchain events
        # For now, return empty list - would need to implement event filtering
        return []

# Global instance
web3_manager = Web3ContractManager()