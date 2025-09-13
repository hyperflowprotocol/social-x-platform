#!/usr/bin/env python3
"""
Check wallet address from private key
"""
from eth_account import Account

def check_wallet(private_key):
    """Check what wallet address corresponds to this private key"""
    try:
        # Remove 0x prefix if present
        if private_key.startswith('0x'):
            private_key = private_key[2:]
        
        # Create account from private key
        account = Account.from_key(private_key)
        
        return {
            'address': account.address,
            'private_key': f"0x{private_key}",
            'valid': True
        }
    except Exception as e:
        return {
            'error': str(e),
            'valid': False
        }

# Check the provided private key
private_key = "0x2d8eb5f900225f88a731435cb44df94d894393a85fe1e586c5be681db4192026"
result = check_wallet(private_key)
print(f"Private Key: {private_key}")
print(f"Wallet Address: {result.get('address', 'INVALID')}")
print(f"Valid: {result.get('valid', False)}")

if 'error' in result:
    print(f"Error: {result['error']}")