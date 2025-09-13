#!/usr/bin/env python3
"""
Test Web3 library for proper Ethereum wallet generation
"""

try:
    from web3 import Web3
    from eth_account import Account
    
    private_key = "0x2d8eb5f900225f88a731435cb44df94d894393a85fe1e586c5be681db4192026"
    
    # Method 1: Using eth_account (should match standard wallets)
    account = Account.from_key(private_key)
    
    print("WEB3 ETHEREUM WALLET GENERATION")
    print("=" * 50)
    print(f"Private Key: {private_key}")
    print(f"Web3 Address: {account.address}")
    print()
    print("Expected Addresses:")
    print(f"Bitget Wallet: 0xF82a348F5FeACfF637504B5EF38a016621B0d04e")
    print(f"X Wallet:      0x075e009fcfce39fa2813e778052ccb95d8fa17b1")
    print(f"Web3 Library:  {account.address}")
    print()
    
    # Check if it matches either expected address
    if account.address.lower() == "0xF82a348F5FeACfF637504B5EF38a016621B0d04e".lower():
        print("✅ MATCHES BITGET WALLET!")
    elif account.address.lower() == "0x075e009fcfce39fa2813e778052ccb95d8fa17b1".lower():
        print("✅ MATCHES X WALLET!")
    else:
        print("❌ DOES NOT MATCH EXPECTED ADDRESSES")
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Web3 library not available")