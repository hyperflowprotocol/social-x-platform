#!/usr/bin/env python3
"""
HyperEVM NFT Generator - Creates detailed NFT collections with complex traits
Similar to Hypio collection with multiple layers and rarity system
"""

import random
import json
import os
from datetime import datetime
import hashlib

class HyperEVMNFTGenerator:
    def __init__(self):
        # Detailed trait system like Hypio
        self.traits = {
            'Background': {
                'Cosmic Purple': {'weight': 5, 'color': '#4A148C'},
                'Deep Space': {'weight': 10, 'color': '#1A1A2E'},
                'Neon City': {'weight': 15, 'color': '#0F3460'},
                'Electric Blue': {'weight': 20, 'color': '#16213E'},
                'Cyber Green': {'weight': 25, 'color': '#1B5E20'},
                'Golden Hour': {'weight': 15, 'color': '#FF8F00'},
                'Midnight Black': {'weight': 10, 'color': '#000000'}
            },
            'Body': {
                'Diamond Body': {'weight': 1, 'color': '#E1F5FE'},
                'Golden Body': {'weight': 3, 'color': '#FFD700'},
                'Silver Body': {'weight': 5, 'color': '#C0C0C0'},
                'Crystal Body': {'weight': 8, 'color': '#BBDEFB'},
                'Neon Body': {'weight': 12, 'color': '#00E676'},
                'Electric Body': {'weight': 15, 'color': '#00BCD4'},
                'Plasma Body': {'weight': 20, 'color': '#7C4DFF'},
                'Standard Body': {'weight': 36, 'color': '#90CAF9'}
            },
            'Eyes': {
                'Sharingan Eyes': {'weight': 1, 'color': '#FF1744', 'anime': 'Naruto'},
                'Byakugan Eyes': {'weight': 2, 'color': '#E8EAF6', 'anime': 'Naruto'},
                'Saiyan Eyes': {'weight': 3, 'color': '#4CAF50', 'anime': 'Dragon Ball'},
                'Demon Slayer Eyes': {'weight': 5, 'color': '#FF9800', 'anime': 'Demon Slayer'},
                'Geass Eyes': {'weight': 8, 'color': '#E91E63', 'anime': 'Code Geass'},
                'Shinigami Eyes': {'weight': 10, 'color': '#F44336', 'anime': 'Death Note'},
                'All Might Eyes': {'weight': 12, 'color': '#2196F3', 'anime': 'My Hero Academia'},
                'Jotaro Eyes': {'weight': 15, 'color': '#00BCD4', 'anime': 'JoJo'},
                'Pikachu Eyes': {'weight': 20, 'color': '#FFEB3B', 'anime': 'Pokemon'},
                'Kawaii Eyes': {'weight': 24, 'color': '#E91E63', 'anime': 'Generic Anime'}
            },
            'Mouth': {
                'Diamond Grill': {'weight': 1, 'shape': 'rect', 'color': '#E8F5E8'},
                'Gold Teeth': {'weight': 5, 'shape': 'rect', 'color': '#FFD700'},
                'Laser Mouth': {'weight': 8, 'shape': 'ellipse', 'color': '#FF1744'},
                'Cyber Smile': {'weight': 12, 'shape': 'path', 'color': '#00E676'},
                'Electric Grin': {'weight': 15, 'shape': 'ellipse', 'color': '#FFEB3B'},
                'Plasma Mouth': {'weight': 20, 'shape': 'ellipse', 'color': '#7C4DFF'},
                'Standard Smile': {'weight': 39, 'shape': 'ellipse', 'color': '#FF69B4'}
            },
            'Head Accessory': {
                'Hokage Hat': {'weight': 1, 'type': 'hokage_hat', 'anime': 'Naruto'},
                'Saiyan Hair': {'weight': 2, 'type': 'saiyan_hair', 'anime': 'Dragon Ball'},
                'Straw Hat': {'weight': 3, 'type': 'straw_hat', 'anime': 'One Piece'},
                'Survey Corps Badge': {'weight': 5, 'type': 'survey_badge', 'anime': 'Attack on Titan'},
                'Demon Slayer Headband': {'weight': 8, 'type': 'demon_headband', 'anime': 'Demon Slayer'},
                'UA School Badge': {'weight': 10, 'type': 'ua_badge', 'anime': 'My Hero Academia'},
                'Ichigo Headband': {'weight': 12, 'type': 'ichigo_headband', 'anime': 'Bleach'},
                'Anime Cat Ears': {'weight': 15, 'type': 'cat_ears', 'anime': 'Neko Anime'},
                'Sailor Moon Tiara': {'weight': 18, 'type': 'sailor_tiara', 'anime': 'Sailor Moon'},
                'None': {'weight': 26, 'type': 'none'}
            },
            'Special Effect': {
                'Kamehameha Wave': {'weight': 1, 'effect': 'kamehameha', 'anime': 'Dragon Ball'},
                'Rasengan Orb': {'weight': 2, 'effect': 'rasengan', 'anime': 'Naruto'},
                'Thunder Breathing': {'weight': 3, 'effect': 'thunder_breathing', 'anime': 'Demon Slayer'},
                'Stand Power': {'weight': 5, 'effect': 'stand_power', 'anime': 'JoJo'},
                'Titan Steam': {'weight': 8, 'effect': 'titan_steam', 'anime': 'Attack on Titan'},
                'Quirk Manifestation': {'weight': 10, 'effect': 'quirk', 'anime': 'My Hero Academia'},
                'Spirit Bomb Aura': {'weight': 12, 'effect': 'spirit_bomb', 'anime': 'Dragon Ball'},
                'Chakra Flow': {'weight': 15, 'effect': 'chakra', 'anime': 'Naruto'},
                'Anime Sparkles': {'weight': 20, 'effect': 'sparkles', 'anime': 'Shoujo Anime'},
                'None': {'weight': 24, 'effect': 'none'}
            },
            'Rarity Level': {
                'Legendary': {'weight': 1, 'multiplier': 10},
                'Epic': {'weight': 4, 'multiplier': 5},
                'Rare': {'weight': 15, 'multiplier': 3},
                'Uncommon': {'weight': 30, 'multiplier': 2},
                'Common': {'weight': 50, 'multiplier': 1}
            }
        }
        
        self.contract_address = "0x63eb9d77D083cA10C304E28d5191321977fd0Bfb"  # HyperEVM contract
        self.chain_id = 999  # HyperEVM
        
    def weighted_choice(self, trait_dict):
        """Select trait based on weights (rarer traits have lower weights)"""
        total_weight = sum(item['weight'] for item in trait_dict.values())
        choice = random.randint(1, total_weight)
        
        current_weight = 0
        for trait_name, trait_data in trait_dict.items():
            current_weight += trait_data['weight']
            if choice <= current_weight:
                return trait_name, trait_data
        
        return list(trait_dict.items())[0]  # Fallback
    
    def generate_metadata(self, token_id):
        """Generate detailed metadata with trait rarity"""
        # Select traits
        background_name, background_data = self.weighted_choice(self.traits['Background'])
        body_name, body_data = self.weighted_choice(self.traits['Body'])
        eyes_name, eyes_data = self.weighted_choice(self.traits['Eyes'])
        mouth_name, mouth_data = self.weighted_choice(self.traits['Mouth'])
        head_acc_name, head_acc_data = self.weighted_choice(self.traits['Head Accessory'])
        effect_name, effect_data = self.weighted_choice(self.traits['Special Effect'])
        rarity_name, rarity_data = self.weighted_choice(self.traits['Rarity Level'])
        
        # Calculate rarity score
        rarity_score = (
            (100 / self.traits['Background'][background_name]['weight']) +
            (100 / self.traits['Body'][body_name]['weight']) +
            (100 / self.traits['Eyes'][eyes_name]['weight']) +
            (100 / self.traits['Mouth'][mouth_name]['weight']) +
            (100 / self.traits['Head Accessory'][head_acc_name]['weight']) +
            (100 / self.traits['Special Effect'][effect_name]['weight'])
        ) * rarity_data['multiplier']
        
        metadata = {
            'name': f'HyperEVM NFT #{token_id}',
            'description': f'Unique digital collectible on HyperEVM blockchain. Rarity Score: {rarity_score:.2f}',
            'image': f'https://hypernft.art/api/image/{token_id}',
            'external_url': f'https://hypernft.art/token/{token_id}',
            'animation_url': f'https://hypernft.art/api/animation/{token_id}',
            'attributes': [
                {
                    'trait_type': 'Background',
                    'value': background_name,
                    'rarity': f'{(self.traits["Background"][background_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Body',
                    'value': body_name,
                    'rarity': f'{(self.traits["Body"][body_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Eyes',
                    'value': eyes_name,
                    'rarity': f'{(self.traits["Eyes"][eyes_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Mouth',
                    'value': mouth_name,
                    'rarity': f'{(self.traits["Mouth"][mouth_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Head Accessory',
                    'value': head_acc_name,
                    'rarity': f'{(self.traits["Head Accessory"][head_acc_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Special Effect',
                    'value': effect_name,
                    'rarity': f'{(self.traits["Special Effect"][effect_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Rarity Level',
                    'value': rarity_name,
                    'rarity': f'{(self.traits["Rarity Level"][rarity_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Rarity Score',
                    'value': round(rarity_score, 2),
                    'display_type': 'number'
                },
                {
                    'trait_type': 'Generation',
                    'value': 1,
                    'display_type': 'number'
                }
            ],
            'blockchain': 'HyperEVM',
            'chain_id': self.chain_id,
            'contract_address': self.contract_address
        }
        
        # Store trait data for SVG generation
        metadata['_trait_data'] = {
            'background': (background_name, background_data),
            'body': (body_name, body_data),
            'eyes': (eyes_name, eyes_data),
            'mouth': (mouth_name, mouth_data),
            'head_accessory': (head_acc_name, head_acc_data),
            'special_effect': (effect_name, effect_data),
            'rarity': (rarity_name, rarity_data)
        }
        
        return metadata
    
    def create_advanced_effects(self, effect_type):
        """Create complex SVG effects"""
        if effect_type == 'rainbow':
            return '''
            <defs>
                <linearGradient id="rainbow" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FF0000"/>
                    <stop offset="16.66%" stop-color="#FF8000"/>
                    <stop offset="33.33%" stop-color="#FFFF00"/>
                    <stop offset="50%" stop-color="#00FF00"/>
                    <stop offset="66.66%" stop-color="#0080FF"/>
                    <stop offset="83.33%" stop-color="#8000FF"/>
                    <stop offset="100%" stop-color="#FF0080"/>
                </linearGradient>
                <filter id="rainbowGlow">
                    <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
                    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
            </defs>
            '''
        elif effect_type == 'lightning':
            return '''
            <defs>
                <filter id="lightning">
                    <feGaussianBlur stdDeviation="3" result="lightBlur"/>
                    <feColorMatrix in="lightBlur" values="1 0 0 0 1  0 0 1 0 1  0 0 0 1 0  0 0 0 1 0"/>
                </filter>
            </defs>
            '''
        elif effect_type == 'glow':
            return '''
            <defs>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
                    <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
            </defs>
            '''
        return ''
    
    def generate_detailed_svg(self, metadata):
        """Generate complex SVG artwork with multiple layers"""
        width, height = 512, 512
        trait_data = metadata['_trait_data']
        
        bg_name, bg_data = trait_data['background']
        body_name, body_data = trait_data['body']
        eyes_name, eyes_data = trait_data['eyes']
        mouth_name, mouth_data = trait_data['mouth']
        head_name, head_data = trait_data['head_accessory']
        effect_name, effect_data = trait_data['special_effect']
        
        # Start SVG
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
{self.create_advanced_effects(effect_data.get('effect', 'none'))}

<!-- Background Layer -->
<rect width="{width}" height="{height}" fill="{bg_data['color']}"/>

<!-- Background Pattern -->
<circle cx="256" cy="256" r="200" fill="none" stroke="{bg_data['color']}" stroke-width="2" opacity="0.3"/>
<circle cx="256" cy="256" r="150" fill="none" stroke="{bg_data['color']}" stroke-width="1" opacity="0.2"/>

<!-- Body (Main Character) -->
<ellipse cx="256" cy="280" rx="80" ry="120" fill="{body_data['color']}" stroke="#333" stroke-width="3"/>

<!-- Head -->
<circle cx="256" cy="180" r="60" fill="{body_data['color']}" stroke="#333" stroke-width="3"/>

<!-- Eyes -->
<ellipse cx="235" cy="165" rx="8" ry="12" fill="{eyes_data['color']}" />
<ellipse cx="277" cy="165" rx="8" ry="12" fill="{eyes_data['color']}" />

<!-- Eye highlights -->
<circle cx="238" cy="162" r="3" fill="white" opacity="0.8"/>
<circle cx="280" cy="162" r="3" fill="white" opacity="0.8"/>

<!-- Mouth -->
<ellipse cx="256" cy="190" rx="12" ry="6" fill="{mouth_data['color']}" />

<!-- Arms -->
<ellipse cx="200" cy="260" rx="25" ry="60" fill="{body_data['color']}" stroke="#333" stroke-width="2"/>
<ellipse cx="312" cy="260" rx="25" ry="60" fill="{body_data['color']}" stroke="#333" stroke-width="2"/>

<!-- Legs -->
<ellipse cx="230" cy="380" rx="20" ry="50" fill="{body_data['color']}" stroke="#333" stroke-width="2"/>
<ellipse cx="282" cy="380" rx="20" ry="50" fill="{body_data['color']}" stroke="#333" stroke-width="2"/>
'''
        
        # Add anime head accessories
        if head_data['type'] == 'hokage_hat':
            svg_content += '''
<!-- Hokage Hat -->
<ellipse cx="256" cy="115" rx="45" ry="15" fill="#FF6B35"/>
<polygon points="256,100 240,120 272,120" fill="#FF6B35"/>
<text x="256" y="118" font-family="Arial" font-size="12" fill="white" text-anchor="middle">火</text>
'''
        elif head_data['type'] == 'saiyan_hair':
            svg_content += '''
<!-- Saiyan Spiky Hair -->
<polygon points="256,120 240,90 250,80 256,70 262,80 272,90" fill="#FFD700"/>
<polygon points="220,130 210,100 225,95 235,110" fill="#FFD700"/>
<polygon points="292,130 302,100 287,95 277,110" fill="#FFD700"/>
'''
        elif head_data['type'] == 'straw_hat':
            svg_content += '''
<!-- Straw Hat -->
<ellipse cx="256" cy="110" rx="50" ry="12" fill="#D2691E"/>
<circle cx="256" cy="115" r="35" fill="none" stroke="#8B4513" stroke-width="3"/>
<rect x="251" y="108" width="10" height="6" fill="#FF0000"/>
'''
        elif head_data['type'] == 'cat_ears':
            svg_content += '''
<!-- Anime Cat Ears -->
<polygon points="230,120 220,95 240,110" fill="#FFB6C1"/>
<polygon points="282,120 292,95 272,110" fill="#FFB6C1"/>
<polygon points="230,115 225,100 235,108" fill="#FF69B4"/>
<polygon points="282,115 287,100 277,108" fill="#FF69B4"/>
'''
        elif head_data['type'] == 'sailor_tiara':
            svg_content += '''
<!-- Sailor Moon Tiara -->
<ellipse cx="256" cy="125" rx="25" ry="5" fill="#FFD700"/>
<circle cx="256" cy="125" r="4" fill="#FF1493"/>
<polygon points="256,120 252,115 260,115" fill="#FFD700"/>
'''
        
        # Add anime special effects
        if effect_data.get('effect') == 'kamehameha':
            svg_content += '''
<!-- Kamehameha Wave -->
<ellipse cx="200" cy="260" rx="15" ry="40" fill="#00BFFF" opacity="0.8"/>
<ellipse cx="180" cy="260" rx="20" ry="50" fill="#87CEEB" opacity="0.6"/>
<ellipse cx="160" cy="260" rx="25" ry="60" fill="#ADD8E6" opacity="0.4"/>
'''
        elif effect_data.get('effect') == 'rasengan':
            svg_content += '''
<!-- Rasengan Orb -->
<circle cx="200" cy="260" r="25" fill="#00BFFF" opacity="0.8"/>
<circle cx="200" cy="260" r="20" fill="#87CEEB" opacity="0.6"/>
<circle cx="200" cy="260" r="15" fill="#ADD8E6" opacity="0.8"/>
<circle cx="200" cy="260" r="10" fill="white" opacity="0.9"/>
'''
        elif effect_data.get('effect') == 'thunder_breathing':
            svg_content += '''
<!-- Thunder Breathing -->
<path d="M 200 150 L 180 180 L 200 180 L 180 210" stroke="#FFD700" stroke-width="4" fill="none"/>
<path d="M 312 150 L 332 180 L 312 180 L 332 210" stroke="#FFD700" stroke-width="4" fill="none"/>
<circle cx="256" cy="256" r="180" fill="none" stroke="#FFEB3B" stroke-width="2" opacity="0.5"/>
'''
        elif effect_data.get('effect') == 'stand_power':
            svg_content += '''
<!-- Stand Power -->
<rect x="240" y="240" width="32" height="80" fill="#9C27B0" opacity="0.3"/>
<rect x="245" y="245" width="22" height="70" fill="#E91E63" opacity="0.5"/>
<circle cx="256" cy="220" r="15" fill="#9C27B0" opacity="0.4"/>
'''
        elif effect_data.get('effect') == 'sparkles':
            svg_content += '''
<!-- Anime Sparkles -->
<polygon points="100,100 102,108 110,110 102,112 100,120 98,112 90,110 98,108" fill="#FFB6C1"/>
<polygon points="400,150 402,158 410,160 402,162 400,170 398,162 390,160 398,158" fill="#FF69B4"/>
<polygon points="150,350 152,358 160,360 152,362 150,370 148,362 140,360 148,358" fill="#FFB6C1"/>
<polygon points="350,320 352,328 360,330 352,332 350,340 348,332 340,330 348,328" fill="#FF69B4"/>
'''
        
        # Add signature
        svg_content += '''
<!-- HyperEVM Signature -->
<text x="10" y="500" fill="white" font-family="Arial" font-size="10" opacity="0.6">HyperEVM NFT</text>
</svg>'''
        
        return svg_content
    
    def generate_collection(self, collection_size=10000, collection_name="HyperEVM NFT Collection"):
        """Generate large NFT collection with rarity distribution"""
        # Create directories
        base_dir = f'hyperevm_collection_{int(datetime.now().timestamp())}'
        os.makedirs(f'{base_dir}/images', exist_ok=True)
        os.makedirs(f'{base_dir}/metadata', exist_ok=True)
        
        collection_metadata = {
            'name': collection_name,
            'description': 'Detailed NFT collection on HyperEVM blockchain with complex trait system and rarity mechanics',
            'image': f'https://hypernft.art/collection-banner.png',
            'external_link': 'https://hypernft.art',
            'seller_fee_basis_points': 500,  # 5% royalty
            'fee_recipient': self.contract_address,
            'blockchain': 'HyperEVM',
            'chain_id': self.chain_id,
            'contract_address': self.contract_address,
            'total_supply': collection_size,
            'created_at': datetime.now().isoformat(),
            'traits_summary': {},
            'rarity_distribution': {}
        }
        
        # Generate NFTs
        rarity_counts = {}
        trait_counts = {trait_type: {} for trait_type in self.traits.keys()}
        
        print(f"Generating {collection_size} HyperEVM NFTs with detailed traits...")
        
        for token_id in range(1, collection_size + 1):
            # Generate metadata
            metadata = self.generate_metadata(token_id)
            
            # Generate artwork
            svg_content = self.generate_detailed_svg(metadata)
            
            # Save files
            with open(f'{base_dir}/images/{token_id}.svg', 'w') as f:
                f.write(svg_content)
            
            # Clean metadata for JSON (remove internal trait data)
            clean_metadata = {k: v for k, v in metadata.items() if not k.startswith('_')}
            
            with open(f'{base_dir}/metadata/{token_id}', 'w') as f:  # No .json extension for OpenSea compatibility
                json.dump(clean_metadata, f, indent=2)
            
            # Track statistics
            rarity_level = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Rarity Level')
            rarity_counts[rarity_level] = rarity_counts.get(rarity_level, 0) + 1
            
            for attr in metadata['attributes']:
                trait_type = attr['trait_type']
                trait_value = attr['value']
                if trait_type in trait_counts:
                    trait_counts[trait_type][trait_value] = trait_counts[trait_type].get(trait_value, 0) + 1
            
            if token_id % 100 == 0:
                print(f"Generated {token_id}/{collection_size} NFTs...")
        
        # Update collection metadata with statistics
        collection_metadata['traits_summary'] = trait_counts
        collection_metadata['rarity_distribution'] = rarity_counts
        
        # Save collection metadata
        with open(f'{base_dir}/collection.json', 'w') as f:
            json.dump(collection_metadata, f, indent=2)
        
        # Generate deployment script
        self.generate_deployment_script(base_dir, collection_metadata)
        
        return base_dir, collection_metadata
    
    def generate_deployment_script(self, base_dir, metadata):
        """Generate HyperEVM deployment script"""
        contract_addr = metadata['contract_address']
        collection_name = metadata['name']
        total_supply = metadata['total_supply']
        rarity_dist = metadata['rarity_distribution']
        
        script_content = f'''#!/usr/bin/env python3
"""
HyperEVM NFT Collection Deployment Script
Collection: {collection_name}
Total Supply: {total_supply}
"""

from web3 import Web3
import json
import os

# HyperEVM Configuration
RPC_URL = "https://rpc.hyperliquid.xyz/evm"
CHAIN_ID = 999
CONTRACT_ADDRESS = "{contract_addr}"

# Connect to HyperEVM
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def deploy_metadata():
    """Deploy metadata to IPFS and update contract"""
    print("🚀 Deploying {collection_name} to HyperEVM")
    print(f"📊 Total Supply: {total_supply}")
    print(f"🔗 Contract: {{CONTRACT_ADDRESS}}")
    print(f"⛓️  Chain ID: {{CHAIN_ID}}")
    
    # Check connection
    if not w3.is_connected():
        print("❌ Failed to connect to HyperEVM RPC")
        return
    
    print("✅ Connected to HyperEVM")
    print(f"🏗️  Latest Block: {{w3.eth.block_number}}")
    
    # TODO: Add IPFS upload logic
    # TODO: Add contract interaction logic
    
    print("\\n📈 Collection Statistics:")
    for rarity, count in {rarity_dist}.items():
        percentage = (count / {total_supply}) * 100
        print(f"   {{rarity}}: {{count}} NFTs ({{percentage:.1f}}%)")

if __name__ == "__main__":
    deploy_metadata()
'''
        
        with open(f'{base_dir}/deploy.py', 'w') as f:
            f.write(script_content)
        
        os.chmod(f'{base_dir}/deploy.py', 0o755)

if __name__ == "__main__":
    generator = HyperEVMNFTGenerator()
    
    print("🎨 HyperEVM NFT Collection Generator")
    print("=" * 60)
    print("Creates detailed NFT collections with complex trait systems")
    print("Similar to Hypio with multiple rarity layers and effects")
    print()
    
    try:
        collection_size = int(input("Collection size (1-10000): ") or "100")
        collection_size = max(1, min(collection_size, 10000))
    except ValueError:
        collection_size = 100
    
    try:
        collection_name = input("Collection name: ") or "HyperEVM NFT Collection"
    except:
        collection_name = "HyperEVM NFT Collection"
    
    print(f"\n🚀 Generating '{collection_name}' with {collection_size} NFTs...")
    
    folder, metadata = generator.generate_collection(collection_size, collection_name)
    
    print(f"\n✅ Collection Generated Successfully!")
    print(f"📁 Folder: ./{folder}/")
    print(f"🖼️  Images: ./{folder}/images/ ({collection_size} SVG files)")
    print(f"📄 Metadata: ./{folder}/metadata/ (OpenSea compatible)")
    print(f"🚀 Deployment: ./{folder}/deploy.py")
    
    # Show rarity statistics
    print(f"\n📊 Rarity Distribution:")
    total = sum(metadata['rarity_distribution'].values())
    for rarity, count in sorted(metadata['rarity_distribution'].items(), 
                               key=lambda x: generator.traits['Rarity Level'][x[0]]['weight']):
        percentage = (count / total) * 100
        print(f"   {rarity}: {count} NFTs ({percentage:.1f}%)")
    
    print(f"\n💎 Most Rare Combinations:")
    print(f"   Diamond Body + Laser Eyes + Diamond Crown = Ultra Rare")
    print(f"   Golden Body + Galaxy Eyes + Golden Halo = Legendary")
    print(f"   Any Rainbow Aura combination = Mythical")