#!/usr/bin/env python3
"""
Debug wallet generation inconsistencies
"""

private_key = "0x2d8eb5f900225f88a731435cb44df94d894393a85fe1e586c5be681db4192026"

print("WALLET GENERATION DEBUG")
print("=" * 50)
print(f"Private Key: {private_key}")
print()

# Method 1: Our current system
from crypto_wallet import generate_ethereum_address_from_private_key
private_key_clean = private_key[2:] if private_key.startswith('0x') else private_key
our_address = generate_ethereum_address_from_private_key(private_key_clean)
print(f"Our System:     {our_address}")

# Expected addresses from external wallets
print(f"Bitget Wallet:  0xF82a348F5FeACfF637504B5EF38a016621B0d04e")
print(f"X Wallet:       0x075e009fcfce39fa2813e778052ccb95d8fa17b1")
print()

print("ISSUE IDENTIFIED:")
print("- Different wallet systems are generating different addresses from the same private key")
print("- This breaks interoperability and user expectations")
print("- Need to implement proper Ethereum cryptography standards")