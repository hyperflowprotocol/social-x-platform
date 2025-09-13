#!/usr/bin/env python3
"""
Metadata Fetcher for Token Platform
Automatically fetches token logos, metadata, and additional information
"""

import json
import base64
import hashlib
from urllib.parse import urlparse
from typing import Dict, Any, Optional, List
import re
import time
import urllib.request
import urllib.error

class TokenMetadataFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'HYPE-Platform/1.0 (Token Metadata Fetcher)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Common token registry APIs
        self.token_registries = [
            "https://tokens.coingecko.com/uniswap/all.json",
            "https://gateway.ipfs.io/ipns/tokens.uniswap.org",
            "https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/ethereum/tokenlist.json"
        ]
        
        # IPFS gateways for metadata fetching
        self.ipfs_gateways = [
            "https://gateway.ipfs.io/ipfs/",
            "https://ipfs.io/ipfs/",
            "https://cloudflare-ipfs.com/ipfs/",
            "https://dweb.link/ipfs/"
        ]

    def fetch_token_metadata(self, contract_address: str, chain_id: int = 999) -> Dict[str, Any]:
        """Fetch comprehensive token metadata"""
        metadata = {
            'address': contract_address,
            'chain_id': chain_id,
            'name': None,
            'symbol': None,
            'decimals': None,
            'total_supply': None,
            'logo_uri': None,
            'description': None,
            'website': None,
            'social_links': {},
            'verified': False,
            'tags': [],
            'fetched_at': int(time.time())
        }
        
        # Fetch on-chain data
        on_chain_data = self.fetch_on_chain_data(contract_address, chain_id)
        if on_chain_data:
            metadata.update(on_chain_data)
        
        # Try to fetch from token registries
        registry_data = self.fetch_from_registries(contract_address)
        if registry_data:
            metadata.update(registry_data)
        
        # Try to fetch IPFS metadata
        if metadata.get('logo_uri') and 'ipfs://' in metadata['logo_uri']:
            ipfs_data = self.fetch_ipfs_metadata(metadata['logo_uri'])
            if ipfs_data:
                metadata.update(ipfs_data)
        
        # Fetch social media and website data
        website = metadata.get('website')
        if website:
            social_data = self.fetch_social_data(website)
            if social_data:
                metadata['social_links'].update(social_data)
        
        return metadata

    def fetch_on_chain_data(self, contract_address: str, chain_id: int) -> Optional[Dict[str, Any]]:
        """Fetch token data directly from blockchain"""
        try:
            rpc_url = self.get_rpc_url(chain_id)
            if not rpc_url:
                return None
            
            # ERC20 function signatures
            functions = {
                'name': '0x06fdde03',
                'symbol': '0x95d89b41', 
                'decimals': '0x313ce567',
                'totalSupply': '0x18160ddd'
            }
            
            data = {}
            
            for func_name, signature in functions.items():
                try:
                    payload = json.dumps({
                        "jsonrpc": "2.0",
                        "method": "eth_call",
                        "params": [{
                            "to": contract_address,
                            "data": signature
                        }, "latest"],
                        "id": 1
                    }).encode('utf-8')
                    
                    req = urllib.request.Request(rpc_url, data=payload, headers=self.headers)
                    with urllib.request.urlopen(req, timeout=10) as response:
                        if response.status == 200:
                            result_data = json.loads(response.read().decode('utf-8'))
                            result = result_data.get('result')
                            if result and result != '0x':
                                decoded = self.decode_eth_response(result, func_name)
                                if decoded:
                                    data[func_name.lower()] = decoded
                                
                except Exception as e:
                    print(f"Error fetching {func_name}: {e}")
                    continue
            
            return data if data else None
            
        except Exception as e:
            print(f"Error fetching on-chain data: {e}")
            return None

    def decode_eth_response(self, hex_response: str, func_name: str) -> Any:
        """Decode Ethereum response based on function type"""
        try:
            if not hex_response or hex_response == '0x':
                return None
                
            # Remove 0x prefix
            hex_data = hex_response[2:] if hex_response.startswith('0x') else hex_response
            
            if func_name in ['name', 'symbol']:
                # String response - skip first 64 chars (offset + length), then decode
                if len(hex_data) > 128:
                    # Get length
                    length = int(hex_data[64:128], 16) * 2
                    if length > 0 and len(hex_data) >= 128 + length:
                        string_hex = hex_data[128:128 + length]
                        return bytes.fromhex(string_hex).decode('utf-8', errors='ignore').strip('\x00')
                        
            elif func_name in ['decimals', 'totalSupply']:
                # Uint256 response
                return str(int(hex_data, 16))
                
        except Exception as e:
            print(f"Error decoding {func_name}: {e}")
            
        return None

    def get_rpc_url(self, chain_id: int) -> Optional[str]:
        """Get RPC URL for chain"""
        rpc_urls = {
            1: "https://eth.llamarpc.com",
            999: "https://rpc.hyperliquid.xyz/evm",
            56: "https://bsc-dataseed1.binance.org",
            137: "https://polygon-rpc.com"
        }
        return rpc_urls.get(chain_id)

    def fetch_from_registries(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """Fetch token data from token registries"""
        for registry_url in self.token_registries:
            try:
                response = self.session.get(registry_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Search for token in registry
                    tokens = data.get('tokens', [])
                    for token in tokens:
                        if token.get('address', '').lower() == contract_address.lower():
                            return {
                                'logo_uri': token.get('logoURI'),
                                'verified': True,
                                'tags': token.get('tags', []),
                                'description': token.get('description'),
                                'website': token.get('website')
                            }
                            
            except Exception as e:
                print(f"Error fetching from registry {registry_url}: {e}")
                continue
                
        return None

    def fetch_ipfs_metadata(self, ipfs_uri: str) -> Optional[Dict[str, Any]]:
        """Fetch metadata from IPFS"""
        try:
            # Convert ipfs:// to http gateway URL
            if ipfs_uri.startswith('ipfs://'):
                ipfs_hash = ipfs_uri[7:]
            else:
                return None
            
            for gateway in self.ipfs_gateways:
                try:
                    url = f"{gateway}{ipfs_hash}"
                    response = self.session.get(url, timeout=15)
                    
                    if response.status_code == 200:
                        # Try to parse as JSON first
                        try:
                            metadata = response.json()
                            return {
                                'description': metadata.get('description'),
                                'logo_uri': self.resolve_ipfs_url(metadata.get('image')),
                                'website': metadata.get('external_url'),
                                'attributes': metadata.get('attributes', [])
                            }
                        except:
                            # If not JSON, might be an image
                            if response.headers.get('content-type', '').startswith('image/'):
                                return {'logo_uri': url}
                                
                except Exception as e:
                    print(f"Error fetching from IPFS gateway {gateway}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error processing IPFS URI: {e}")
            
        return None

    def resolve_ipfs_url(self, url: str) -> Optional[str]:
        """Resolve IPFS URL to HTTP gateway URL"""
        if not url:
            return None
            
        if url.startswith('ipfs://'):
            ipfs_hash = url[7:]
            return f"{self.ipfs_gateways[0]}{ipfs_hash}"
        
        return url

    def fetch_social_data(self, website: str) -> Optional[Dict[str, str]]:
        """Fetch social media links from website"""
        if not website:
            return None
            
        try:
            response = self.session.get(website, timeout=10)
            if response.status_code == 200:
                content = response.text
                
                social_patterns = {
                    'twitter': r'https?://(?:www\.)?twitter\.com/([a-zA-Z0-9_]+)',
                    'telegram': r'https?://(?:www\.)?(?:t\.me|telegram\.me)/([a-zA-Z0-9_]+)',
                    'discord': r'https?://(?:www\.)?discord\.gg/([a-zA-Z0-9_]+)',
                    'github': r'https?://(?:www\.)?github\.com/([a-zA-Z0-9_-]+)',
                    'medium': r'https?://(?:www\.)?medium\.com/@?([a-zA-Z0-9_-]+)'
                }
                
                social_links = {}
                for platform, pattern in social_patterns.items():
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        social_links[platform] = matches[0]
                
                return social_links if social_links else None
                
        except Exception as e:
            print(f"Error fetching social data: {e}")
            
        return None

    def download_and_encode_image(self, image_url: str) -> Optional[str]:
        """Download image and encode as base64"""
        try:
            response = self.session.get(image_url, timeout=15)
            if response.status_code == 200 and len(response.content) < 5 * 1024 * 1024:  # Max 5MB
                content_type = response.headers.get('content-type', 'image/png')
                encoded = base64.b64encode(response.content).decode('utf-8')
                return f"data:{content_type};base64,{encoded}"
        except Exception as e:
            print(f"Error downloading image: {e}")
            
        return None

    def get_token_price(self, contract_address: str, chain_id: int = 999) -> Optional[Dict[str, Any]]:
        """Get token price from various APIs"""
        # This would integrate with price APIs like CoinGecko, CoinMarketCap, etc.
        # For now, return None as prices require API keys
        return None

    def batch_fetch_metadata(self, token_addresses: List[str], chain_id: int = 999) -> Dict[str, Dict[str, Any]]:
        """Fetch metadata for multiple tokens"""
        results = {}
        
        for address in token_addresses:
            print(f"Fetching metadata for {address}...")
            try:
                metadata = self.fetch_token_metadata(address, chain_id)
                results[address] = metadata
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"Error fetching metadata for {address}: {e}")
                results[address] = {'error': str(e)}
                
        return results

def main():
    """Test the metadata fetcher"""
    fetcher = TokenMetadataFetcher()
    
    # Test with known tokens
    test_tokens = [
        "0xb747b4b456eac8f92e4d3e73562402f52103c8b0",  # HYPE
        "0x63eb9d77D083cA10C304E28d5191321977fd0Bfb"   # Hypio
    ]
    
    print("🔍 Testing Token Metadata Fetcher")
    print("="*50)
    
    for token in test_tokens:
        print(f"\n📊 Fetching metadata for {token}")
        metadata = fetcher.fetch_token_metadata(token)
        
        print(f"Name: {metadata.get('name', 'Unknown')}")
        print(f"Symbol: {metadata.get('symbol', 'Unknown')}")
        print(f"Total Supply: {metadata.get('total_supply', 'Unknown')}")
        print(f"Logo URI: {metadata.get('logo_uri', 'None')}")
        print(f"Verified: {metadata.get('verified', False)}")
        print("-" * 40)

if __name__ == "__main__":
    main()