#!/usr/bin/env python3
"""
Generate a sample HyperEVM NFT collection with detailed traits
"""

import sys
sys.path.append('.')
from hyperevm_nft_generator import HyperEVMNFTGenerator
import json

def main():
    generator = HyperEVMNFTGenerator()
    
    print("Creating sample HyperEVM NFT collection with 10 detailed NFTs...")
    
    # Generate small sample collection
    folder, metadata = generator.generate_collection(10, "Sample HyperEVM Collection")
    
    print(f"\nCollection created in: {folder}")
    print(f"Total NFTs: {metadata['total_supply']}")
    
    # Show sample metadata
    with open(f"{folder}/metadata/1", "r") as f:
        sample = json.load(f)
    
    print(f"\nSample NFT #1 Traits:")
    for attr in sample['attributes']:
        if 'rarity' in attr:
            print(f"  {attr['trait_type']}: {attr['value']} ({attr['rarity']})")
        else:
            print(f"  {attr['trait_type']}: {attr['value']}")
    
    print(f"\nRarity Distribution:")
    for rarity, count in metadata['rarity_distribution'].items():
        print(f"  {rarity}: {count} NFTs")
    
    print(f"\nFiles generated:")
    print(f"  Images: {folder}/images/ (SVG format)")
    print(f"  Metadata: {folder}/metadata/ (JSON format)")
    print(f"  Deploy script: {folder}/deploy.py")

if __name__ == "__main__":
    main()