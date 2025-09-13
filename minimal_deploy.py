#!/usr/bin/env python3
"""
Minimal HyperEVM Deployment Script
"""

import os
import json
import urllib.request

# Get private key
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
WALLET_ADDRESS = "0xbfc06de2711abee4d1d9f370cde09773ddde7048"

def rpc_call(method, params=None):
    """Make RPC call to HyperEVM"""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or [],
        "id": 1
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request("https://rpc.hyperliquid.xyz/evm", data=data)
    req.add_header('Content-Type', 'application/json')
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
    
    return result.get('result')

def main():
    """Main deployment function"""
    print("🚀 DEPLOYING TO HYPEREVM")
    
    if not PRIVATE_KEY:
        print("❌ PRIVATE_KEY not found")
        return
    
    print(f"🔑 Key: {PRIVATE_KEY[:10]}...{PRIVATE_KEY[-8:]}")
    print(f"📍 Wallet: {WALLET_ADDRESS}")
    
    # Check connection
    block = rpc_call("eth_blockNumber")
    if block:
        print(f"🌐 Block: {int(block, 16):,}")
    else:
        print("❌ Connection failed")
        return
    
    # Check balance
    balance_hex = rpc_call("eth_getBalance", [WALLET_ADDRESS, "latest"])
    if balance_hex:
        balance = int(balance_hex, 16) / 1e18
        print(f"💰 Balance: {balance:.8f} HYPE")
        if balance < 0.0005:
            print("❌ Insufficient balance")
            return
    else:
        print("❌ Balance check failed")
        return
    
    # Get nonce
    nonce_hex = rpc_call("eth_getTransactionCount", [WALLET_ADDRESS, "latest"])
    if nonce_hex:
        nonce = int(nonce_hex, 16)
        print(f"🔢 Nonce: {nonce}")
    else:
        print("❌ Nonce failed")
        return
    
    print("✅ Ready for deployment")
    print("💡 Use eth_account + web3 for real transaction signing")
    print("🔗 Transaction will appear on https://hyperevmscan.io/")
    
    return {
        "wallet": WALLET_ADDRESS,
        "balance": balance,
        "nonce": nonce,
        "ready": True
    }

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2) if result else "Failed")