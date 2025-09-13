#!/usr/bin/env python3
"""
Test fresh wallet generation for the authenticated user
"""
from crypto_wallet import CryptoWallet

# Initialize wallet system
wallet_system = CryptoWallet()

# Generate fresh wallet for the authenticated user
user_id = "1903146272535744513"  # From the OAuth logs
fresh_wallet = wallet_system.generate_wallet(f"user_{user_id}")

print("FRESH WALLET FOR X RESTART")
print("=" * 60)
print(f"User ID: {user_id}")
print(f"Private Key: {fresh_wallet['private_key']}")
print(f"Wallet Address: {fresh_wallet['address']}")
print(f"Network: {fresh_wallet['network']} (Chain ID: {fresh_wallet['chain_id']})")
print(f"HYPE Balance: {fresh_wallet['hype_balance']}")
print()
print("NEXT STEPS:")
print("1. Import this private key into your X Wallet")
print("2. Verify the address matches what's shown in X Wallet")
print("3. If addresses don't match, we'll need to implement proper secp256k1 cryptography")
print("4. Once verified, you can use this wallet for trading on the platform")