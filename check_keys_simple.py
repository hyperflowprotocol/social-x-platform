#!/usr/bin/env python3
"""
Simple check for private key configuration
"""

import os

def check_keys():
    """Check what private keys are configured"""
    
    print("🔍 Checking private key configuration...")
    
    # Check all possible private key environment variables
    key_vars = ['WALLET_PRIVATE_KEY', 'PRIVATE_KEY', 'ETH_PRIVATE_KEY', 'HYPEREVM_PRIVATE_KEY']
    
    found_keys = {}
    
    for var in key_vars:
        value = os.getenv(var)
        if value:
            # Don't show the actual key, just confirm it exists and show length
            found_keys[var] = {
                'exists': True,
                'length': len(value),
                'starts_with_0x': value.startswith('0x') if value else False
            }
        else:
            found_keys[var] = {'exists': False}
    
    print("\n📋 Environment Variables Status:")
    for var, info in found_keys.items():
        if info['exists']:
            print(f"✅ {var}: Found (length: {info['length']}, has 0x prefix: {info['starts_with_0x']})")
        else:
            print(f"❌ {var}: Not found")
    
    # Find the primary key to use
    primary_key = None
    for var in key_vars:
        if found_keys[var]['exists']:
            primary_key = var
            break
    
    if primary_key:
        print(f"\n🎯 Primary key to use: {primary_key}")
        key_value = os.getenv(primary_key)
        
        # Basic validation without external dependencies
        if key_value:
            # Remove 0x prefix for length check
            clean_key = key_value[2:] if key_value.startswith('0x') else key_value
            
            if len(clean_key) == 64:
                print("✅ Key length is correct (64 hex characters)")
                # Show first and last 4 characters for identification
                print(f"🔑 Key preview: {clean_key[:4]}...{clean_key[-4:]}")
                return key_value
            else:
                print(f"⚠️  Key length is {len(clean_key)}, expected 64")
                return key_value
    else:
        print("\n❌ No private key found in environment")
        return None

if __name__ == "__main__":
    check_keys()