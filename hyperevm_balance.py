"""
Real HyperEVM blockchain balance checking
Fetches authentic HYPE token balances from HyperEVM network using direct RPC calls
"""

import urllib.request
import urllib.parse
import json

# HyperEVM Network Configuration
HYPEREVM_RPC = "https://rpc.hyperliquid.xyz/evm"
CHAIN_ID = 999

# HYPE Token Addresses
NATIVE_HYPE = "0x0000000000000000000000000000000000000000"  # Native HYPE
WHYPE_TOKEN = "0x5555555555555555555555555555555555555555"  # Wrapped HYPE

def hex_to_decimal(hex_str):
    """Convert hex string to decimal"""
    if hex_str.startswith('0x'):
        return int(hex_str, 16)
    return int(hex_str, 16)

def wei_to_ether(wei_amount):
    """Convert Wei to Ether (18 decimals)"""
    return wei_amount / (10 ** 18)

class HyperEVMBalanceChecker:
    def __init__(self):
        self.rpc_url = HYPEREVM_RPC
        self.headers = {'Content-Type': 'application/json'}
    
    def make_rpc_call(self, method, params=None):
        """Make JSON-RPC call to HyperEVM using urllib"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1
        }
        
        try:
            # Prepare request
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(self.rpc_url, data=data)
            req.add_header('Content-Type', 'application/json')
            
            # Make request with timeout
            with urllib.request.urlopen(req, timeout=10) as response:
                result_data = response.read().decode('utf-8')
                result = json.loads(result_data)
            
            if 'error' in result:
                print(f"RPC Error: {result['error']}")
                return None
                
            return result.get('result')
            
        except Exception as e:
            print(f"RPC call failed: {e}")
            return None
    
    def get_native_hype_balance(self, address):
        """Get native HYPE balance from HyperEVM"""
        try:
            # Ensure address has proper format
            if not address.startswith('0x'):
                address = f'0x{address}'
            
            # Get balance using eth_getBalance
            balance_hex = self.make_rpc_call("eth_getBalance", [address, "latest"])
            
            if balance_hex is None:
                return 0.0
                
            # Convert hex to decimal then to HYPE
            balance_wei = hex_to_decimal(balance_hex)
            balance_hype = wei_to_ether(balance_wei)
            
            return balance_hype
            
        except Exception as e:
            print(f"Error fetching native HYPE balance for {address}: {e}")
            return 0.0
    
    def get_whype_balance(self, address):
        """Get wrapped HYPE (WHYPE) balance using ERC20 balanceOf"""
        try:
            # Ensure address has proper format
            if not address.startswith('0x'):
                address = f'0x{address}'
            
            # ERC20 balanceOf function signature: balanceOf(address) -> 0x70a08231
            # Encode the function call
            function_sig = "0x70a08231"  # balanceOf(address)
            address_param = address[2:].lower().zfill(64)  # Remove 0x and pad to 64 chars
            data = function_sig + address_param
            
            # Make eth_call to WHYPE contract
            call_data = {
                "to": WHYPE_TOKEN,
                "data": data
            }
            
            balance_hex = self.make_rpc_call("eth_call", [call_data, "latest"])
            
            if balance_hex is None or balance_hex == "0x":
                return 0.0
                
            # Convert hex result to decimal then to WHYPE
            balance_wei = hex_to_decimal(balance_hex)
            balance_whype = wei_to_ether(balance_wei)
            
            return balance_whype
            
        except Exception as e:
            print(f"Error fetching WHYPE balance for {address}: {e}")
            return 0.0
    
    def get_total_hype_balance(self, address):
        """Get total HYPE balance (native + wrapped)"""
        try:
            native_balance = self.get_native_hype_balance(address)
            whype_balance = self.get_whype_balance(address)
            
            total_balance = native_balance + whype_balance
            
            print(f"Real balance check for {address}:")
            print(f"  Native HYPE: {native_balance}")
            print(f"  Wrapped HYPE: {whype_balance}")
            print(f"  Total: {total_balance}")
            
            return {
                'native_hype': native_balance,
                'whype': whype_balance,
                'total': total_balance,
                'network': 'HyperEVM Mainnet',
                'chain_id': CHAIN_ID,
                'rpc_url': HYPEREVM_RPC
            }
            
        except Exception as e:
            print(f"Error fetching total HYPE balance: {e}")
            return {
                'native_hype': 0.0,
                'whype': 0.0,
                'total': 0.0,
                'network': 'HyperEVM Mainnet',
                'chain_id': CHAIN_ID,
                'error': str(e)
            }

# Global balance checker instance
balance_checker = HyperEVMBalanceChecker()

def get_real_hype_balance(address):
    """Get real HYPE balance from blockchain"""
    return balance_checker.get_total_hype_balance(address)

if __name__ == "__main__":
    # Test balance checking
    test_address = "0x1234567890123456789012345678901234567890"
    print("Testing HyperEVM balance checker...")
    
    result = get_real_hype_balance(test_address)
    print(f"Balance result: {result}")