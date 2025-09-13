#!/usr/bin/env python3
"""
Real Contract Scanner for HyperEVM NFTs
Scans authentic smart contracts for real NFT data
"""

import urllib.request
import urllib.parse
import json
import time

class HyperEVMScanner:
    def __init__(self):
        self.rpc_url = "https://rpc.hyperliquid.xyz/evm"
        self.explorer_api = "https://hyperliquid.cloud.blockscout.com/api"
        self.contracts = {
            "wealthy-hypio-babies": "0x63eb9d77D083cA10C304E28d5191321977fd0Bfb",
            "pip-friends": "0x7be8f48894d9EC0528Ca70d9151CF2831C377bE0"
        }
        
    def scan_contract_nfts(self, contract_address, limit=20, offset=0):
        """Scan real NFTs from contract"""
        nfts = []
        try:
            # Get token transfers from Blockscout API
            url = f"{self.explorer_api}/v2/tokens/{contract_address}/instances"
            params = {
                'limit': limit,
                'offset': offset
            }
            
            print(f"🔍 Scanning contract {contract_address}...")
            
            # Build URL with parameters
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            with urllib.request.urlopen(full_url, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    
                    for item in data.get('items', []):
                        nft_data = {
                            'token_id': item.get('id'),
                            'contract_address': contract_address,
                            'metadata_url': item.get('metadata', {}).get('image'),
                            'name': item.get('metadata', {}).get('name', f"NFT #{item.get('id')}"),
                            'description': item.get('metadata', {}).get('description', ''),
                            'attributes': item.get('metadata', {}).get('attributes', []),
                            'owner': item.get('owner', {}).get('hash') if item.get('owner') else None,
                            'is_authentic': True
                        }
                        nfts.append(nft_data)
                    
                    print(f"✅ Found {len(nfts)} authentic NFTs from contract")
                else:
                    print(f"❌ API request failed: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error scanning contract: {e}")
            
        return nfts
    
    def get_contract_stats(self, contract_address):
        """Get real contract statistics"""
        try:
            url = f"{self.explorer_api}/v2/tokens/{contract_address}"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    stats = {
                        'name': data.get('name', 'Unknown Collection'),
                        'symbol': data.get('symbol', ''),
                        'total_supply': data.get('total_supply', '0'),
                        'holders_count': data.get('holders_count', 0),
                        'verified': data.get('verified', False),
                        'contract_address': contract_address
                    }
                    return stats
                else:
                    print(f"❌ Stats request failed: {response.status}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error getting contract stats: {e}")
            return None
    
    def scan_all_collections(self):
        """Scan all configured collections"""
        collections_data = {}
        
        for collection_name, contract_address in self.contracts.items():
            print(f"🔄 Scanning {collection_name}...")
            
            # Get contract stats
            stats = self.get_contract_stats(contract_address)
            
            # Get NFTs
            nfts = self.scan_contract_nfts(contract_address, limit=50)
            
            collections_data[collection_name] = {
                'stats': stats,
                'nfts': nfts,
                'contract_address': contract_address
            }
            
            # Rate limiting
            time.sleep(1)
        
        return collections_data

if __name__ == "__main__":
    scanner = HyperEVMScanner()
    print("🚀 Starting HyperEVM Contract Scanner...")
    
    # Scan Wealthy Hypio Babies
    print("\n📊 Scanning Wealthy Hypio Babies...")
    nfts = scanner.scan_contract_nfts("0x63eb9d77D083cA10C304E28d5191321977fd0Bfb", limit=10)
    print(f"Found {len(nfts)} NFTs")
    
    # Scan PiP & Friends  
    print("\n📊 Scanning PiP & Friends...")
    nfts2 = scanner.scan_contract_nfts("0x7be8f48894d9EC0528Ca70d9151CF2831C377bE0", limit=10)
    print(f"Found {len(nfts2)} NFTs")
    
    print("\n✅ Contract scanning complete")