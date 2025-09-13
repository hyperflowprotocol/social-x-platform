#!/usr/bin/env python3

# Quick test to verify the wallet persistence fix works
import sys
import os
sys.path.append('.')

# Import the wallet function
from social_trading_platform import get_or_create_nodejs_wallet, USER_WALLETS, load_user_wallets

def test_wallet_persistence():
    print("Testing wallet persistence fix...")
    
    # Load existing wallets
    USER_WALLETS.update(load_user_wallets())
    print(f"Loaded {len(USER_WALLETS)} existing wallets")
    
    # Test user ID from your screenshots
    test_user_id = "1903146272535744513"
    
    print(f"\n=== Testing wallet lookup for user {test_user_id} ===")
    
    # This should find the existing wallet, not create a new one
    wallet = get_or_create_nodejs_wallet(test_user_id)
    
    print(f"\nResult:")
    print(f"Address: {wallet['address']}")
    print(f"Has private key: {'private_key' in wallet}")
    
    # Expected address from your screenshots: should be consistent
    expected_address = "0x0B66D7F8cAc45D025d8674C3227433D98b2d6458"
    
    if wallet['address'] == expected_address:
        print("✅ SUCCESS: Wallet persistence is working!")
        print("The same wallet address is being returned consistently.")
    else:
        print(f"❌ ISSUE: Expected {expected_address}, got {wallet['address']}")
        print("Wallet persistence may still have issues.")
    
    return wallet

if __name__ == "__main__":
    test_wallet_persistence()