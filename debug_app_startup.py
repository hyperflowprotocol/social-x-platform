#!/usr/bin/env python3
"""
Debug script to isolate the app startup issue
"""

import sys
import traceback

def test_core_imports():
    """Test all core imports one by one"""
    try:
        print("Testing core imports...")
        
        print("1. Testing standard library imports...")
        import hashlib, http.server, socketserver, json, random, time, urllib.parse, urllib.request
        from datetime import datetime, timedelta
        print("   ✅ Standard library imports OK")
        
        print("2. Testing twitter_oauth import...")
        import twitter_oauth
        print("   ✅ twitter_oauth import OK")
        
        print("3. Testing crypto_wallet import...")
        from crypto_wallet import crypto_wallet
        print("   ✅ crypto_wallet import OK")
        
        print("4. Testing hyperliquid_config import...")
        from hyperliquid_config import HYPERLIQUID_CONFIG, get_chain_config, get_deposit_instructions
        print("   ✅ hyperliquid_config import OK")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_platform_initialization():
    """Test platform class initialization"""
    try:
        print("\nTesting platform initialization...")
        
        # Import the main module
        import social_trading_platform
        print("   ✅ social_trading_platform module imported")
        
        # Test creating platform instance
        platform = social_trading_platform.SocialTradingPlatform()
        print("   ✅ SocialTradingPlatform instance created")
        
        # Test handler class
        handler_class = social_trading_platform.SocialTradingHandler
        print("   ✅ SocialTradingHandler class accessible")
        
        return True
    except Exception as e:
        print(f"❌ Platform initialization error: {e}")
        traceback.print_exc()
        return False

def test_wallet_operations():
    """Test wallet-related operations"""
    try:
        print("\nTesting wallet operations...")
        
        # Test wallet loading
        import social_trading_platform
        wallets = social_trading_platform.load_user_wallets()
        print(f"   ✅ Loaded {len(wallets)} wallets")
        
        # Test nodejs bridge
        from nodejs_wallet_bridge import NodeJSWalletBridge
        bridge = NodeJSWalletBridge()
        print("   ✅ NodeJS bridge created")
        
        return True
    except Exception as e:
        print(f"❌ Wallet operations error: {e}")
        traceback.print_exc()
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🔍 Starting comprehensive app startup debug")
    print("=" * 50)
    
    tests = [
        ("Core Imports", test_core_imports),
        ("Platform Initialization", test_platform_initialization), 
        ("Wallet Operations", test_wallet_operations)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"   ✅ {test_name} PASSED")
            else:
                print(f"   ❌ {test_name} FAILED")
        except Exception as e:
            print(f"   ❌ {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    print(f"\n📊 TEST SUMMARY")
    print("=" * 50)
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n✅ All tests passed - app startup components are working correctly")
    else:
        print("\n❌ Some tests failed - this may explain the app startup issue")

if __name__ == "__main__":
    run_comprehensive_test()