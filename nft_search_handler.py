#!/usr/bin/env python3
"""
NFT Search and Filtering Handler
Enhanced search capabilities for the complete NFT collection
"""

import json
import random
from typing import Dict, List, Optional
from bulk_nft_fetcher import BulkNFTFetcher

class NFTSearchHandler:
    def __init__(self):
        self.bulk_fetcher = BulkNFTFetcher()
        self._full_collection = None
        
    def get_full_collection(self) -> List[Dict]:
        """Get complete collection data for all 5,555 NFTs"""
        if self._full_collection is None:
            print("Generating complete NFT collection data...")
            self._full_collection = self.bulk_fetcher.generate_all_nft_data()
            print(f"Loaded {len(self._full_collection)} NFTs into collection")
        return self._full_collection
    
    def get_random_nfts(self, count: int = 20) -> List[Dict]:
        """Get random NFTs from the complete collection"""
        collection = self.get_full_collection()
        return random.sample(collection, min(count, len(collection)))
    
    def get_trending_nfts(self, count: int = 20) -> List[Dict]:
        """Get trending NFTs (high rarity, recent sales)"""
        collection = self.get_full_collection()
        
        # Sort by rarity rank (lower is better) and recent activity
        sorted_nfts = sorted(collection, key=lambda x: (
            x.get("rarity_rank", 999999),
            -float(x.get("last_sale_price", "0"))
        ))
        
        return sorted_nfts[:count]
    
    def search_nfts(self, query: str, trait_filters: Dict = None, count: int = 20) -> List[Dict]:
        """Search NFTs by name, traits, or token ID"""
        collection = self.get_full_collection()
        results = []
        
        # Search by token ID if query is numeric
        if query.isdigit():
            token_id = int(query)
            for nft in collection:
                if nft.get("token_id") == token_id:
                    results.append(nft)
                    break
        else:
            # Text search in name and traits
            query_lower = query.lower()
            for nft in collection:
                # Search in name
                if query_lower in nft.get("name", "").lower():
                    results.append(nft)
                    continue
                    
                # Search in traits
                for trait in nft.get("traits", []):
                    trait_type = trait.get("trait_type", "").lower()
                    trait_value = trait.get("value", "").lower()
                    if query_lower in trait_type or query_lower in trait_value:
                        results.append(nft)
                        break
        
        # Apply trait filters
        if trait_filters is not None:
            filtered_results = []
            for nft in results:
                matches_filters = True
                for filter_trait, filter_value in trait_filters.items():
                    nft_has_trait = False
                    for trait in nft.get("traits", []):
                        if (trait.get("trait_type", "").lower() == filter_trait.lower() and 
                            trait.get("value", "").lower() == filter_value.lower()):
                            nft_has_trait = True
                            break
                    if not nft_has_trait:
                        matches_filters = False
                        break
                if matches_filters:
                    filtered_results.append(nft)
            results = filtered_results
        
        return results[:count]
    
    def get_nft_by_id(self, token_id: int) -> Optional[Dict]:
        """Get specific NFT by token ID"""
        collection = self.get_full_collection()
        for nft in collection:
            if nft.get("token_id") == token_id:
                return nft
        return None
    
    def get_collection_traits(self) -> Dict[str, List[str]]:
        """Get all unique traits in the collection"""
        collection = self.get_full_collection()
        traits_dict = {}
        
        for nft in collection:
            for trait in nft.get("traits", []):
                trait_type = trait.get("trait_type")
                trait_value = trait.get("value")
                
                if trait_type and trait_value:
                    if trait_type not in traits_dict:
                        traits_dict[trait_type] = set()
                    traits_dict[trait_type].add(trait_value)
        
        # Convert sets to sorted lists
        return {k: sorted(list(v)) for k, v in traits_dict.items()}

if __name__ == "__main__":
    # Test the search handler
    handler = NFTSearchHandler()
    
    # Test random NFTs
    random_nfts = handler.get_random_nfts(5)
    print(f"Random NFTs: {len(random_nfts)}")
    
    # Test trending NFTs
    trending = handler.get_trending_nfts(3)
    print(f"Trending NFTs: {len(trending)}")
    
    # Test search
    search_results = handler.search_nfts("Baby")
    print(f"Search results for 'Baby': {len(search_results)}")
    
    # Test specific NFT
    nft = handler.get_nft_by_id(4801)
    print(f"NFT #4801: {nft['name'] if nft else 'Not found'}")