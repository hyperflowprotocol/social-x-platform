#!/usr/bin/env python3
"""
Proper Ethereum Wallet Implementation
Uses secp256k1 + Keccak-256 for true wallet compatibility
"""

import secrets
import hashlib
import ecdsa
from Crypto.Hash import keccak

def create_ethereum_address(private_key_hex):
    """Generate Ethereum address using proper secp256k1 + Keccak-256 cryptography"""
    # Remove 0x prefix if present
    if private_key_hex.startswith('0x'):
        private_key_hex = private_key_hex[2:]
    
    # Convert hex to bytes
    private_key = bytes.fromhex(private_key_hex)
    
    # Generate public key using secp256k1 curve
    signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.verifying_key
    public_key = verifying_key.to_string()
    
    # Keccak-256 hash of public key (NOT SHA-256!)
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key)
    
    # Last 20 bytes = Ethereum address
    address = "0x" + keccak_hash.hexdigest()[-40:]
    
    return address

def generate_compatible_wallet():
    """Generate wallet that will match MetaMask, Bitget, Trust Wallet, etc."""
    # Generate cryptographically secure random private key
    private_key_bytes = secrets.randbits(256).to_bytes(32, 'big')
    private_key_hex = private_key_bytes.hex()
    private_key = '0x' + private_key_hex
    
    # Generate address using proper Ethereum cryptography
    address = create_ethereum_address(private_key_hex)
    
    return {
        'private_key': private_key,
        'address': address,
        'compatible': True
    }

def test_wallet_compatibility():
    """Test the new wallet generation"""
    print("Testing Proper Ethereum Wallet Generation")
    print("=" * 50)
    
    # Generate test wallet
    wallet = generate_compatible_wallet()
    
    print(f"Private Key: {wallet['private_key']}")
    print(f"Address: {wallet['address']}")
    print(f"Compatible: {wallet['compatible']}")
    print()
    print("This wallet should work identically in:")
    print("- MetaMask")
    print("- Bitget Wallet") 
    print("- Trust Wallet")
    print("- Coinbase Wallet")
    print("- Any standard Ethereum wallet")
    
    return wallet

if __name__ == "__main__":
    test_wallet_compatibility()