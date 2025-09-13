#!/usr/bin/env python3
"""
Naruto-themed NFT Collection Generator for HyperEVM
Detailed traits from the Naruto universe with village affiliations, jutsu, and character elements
"""

import random
import json
import os
from datetime import datetime

class NarutoNFTGenerator:
    def __init__(self):
        self.traits = {
            'Village': {
                'Hidden Leaf (Konoha)': {'weight': 35, 'color': '#228B22', 'symbol': '木'},
                'Hidden Sand (Suna)': {'weight': 15, 'color': '#DAA520', 'symbol': '砂'},
                'Hidden Mist (Kiri)': {'weight': 12, 'color': '#4682B4', 'symbol': '水'},
                'Hidden Cloud (Kumo)': {'weight': 10, 'color': '#708090', 'symbol': '雲'},
                'Hidden Stone (Iwa)': {'weight': 8, 'color': '#8B4513', 'symbol': '岩'},
                'Hidden Sound (Oto)': {'weight': 5, 'color': '#800080', 'symbol': '音'},
                'Akatsuki': {'weight': 3, 'color': '#DC143C', 'symbol': '暁'},
                'Rogue Ninja': {'weight': 12, 'color': '#2F2F2F', 'symbol': '叛'}
            },
            'Eyes': {
                'Mangekyo Sharingan': {'weight': 1, 'color': '#FF0000', 'pattern': 'complex'},
                'Eternal Mangekyo': {'weight': 2, 'color': '#8B0000', 'pattern': 'eternal'},
                'Rinnegan': {'weight': 1, 'color': '#9370DB', 'pattern': 'ripple'},
                'Tenseigan': {'weight': 1, 'color': '#00CED1', 'pattern': 'celestial'},
                'Sharingan (3-Tomoe)': {'weight': 3, 'color': '#FF4500', 'pattern': 'tomoe3'},
                'Sharingan (2-Tomoe)': {'weight': 5, 'color': '#FF6347', 'pattern': 'tomoe2'},
                'Sharingan (1-Tomoe)': {'weight': 8, 'color': '#FF7F50', 'pattern': 'tomoe1'},
                'Byakugan': {'weight': 5, 'color': '#F8F8FF', 'pattern': 'veins'},
                'Nine-Tails Eyes': {'weight': 4, 'color': '#FF8C00', 'pattern': 'slit'},
                'Sage Mode Eyes': {'weight': 6, 'color': '#FFD700', 'pattern': 'toad'},
                'Standard Shinobi Eyes': {'weight': 64, 'color': '#000000', 'pattern': 'normal'}
            },
            'Headband': {
                'Leaf Village Headband': {'weight': 30, 'village': 'Konoha'},
                'Sand Village Headband': {'weight': 15, 'village': 'Suna'},
                'Mist Village Headband': {'weight': 10, 'village': 'Kiri'},
                'Cloud Village Headband': {'weight': 8, 'village': 'Kumo'},
                'Stone Village Headband': {'weight': 7, 'village': 'Iwa'},
                'Sound Village Headband': {'weight': 5, 'village': 'Oto'},
                'Scratched Headband': {'weight': 10, 'village': 'Rogue'},
                'Akatsuki Headband': {'weight': 2, 'village': 'Akatsuki'},
                'No Headband': {'weight': 13, 'village': 'None'}
            },
            'Hair Style': {
                'Naruto Spiky Blonde': {'weight': 8, 'color': '#FFD700'},
                'Sasuke Black Hair': {'weight': 8, 'color': '#000000'},
                'Sakura Pink Hair': {'weight': 8, 'color': '#FFB6C1'},
                'Kakashi Silver Hair': {'weight': 6, 'color': '#C0C0C0'},
                'Gaara Red Hair': {'weight': 5, 'color': '#DC143C'},
                'Hinata Dark Blue Hair': {'weight': 5, 'color': '#191970'},
                'Ino Blonde Hair': {'weight': 5, 'color': '#FFFF00'},
                'Neji Brown Hair': {'weight': 5, 'color': '#8B4513'},
                'Shikamaru Black Ponytail': {'weight': 4, 'color': '#2F2F2F'},
                'Orochimaru Black Long Hair': {'weight': 3, 'color': '#1C1C1C'},
                'Jiraiya White Spiky Hair': {'weight': 3, 'color': '#FFFFFF'},
                'Standard Black Hair': {'weight': 40, 'color': '#000000'}
            },
            'Jutsu Aura': {
                'Nine-Tails Chakra Mode': {'weight': 1, 'color': '#FFD700', 'effect': 'golden_flames'},
                'Susanoo': {'weight': 2, 'color': '#4169E1', 'effect': 'armor'},
                'Chidori': {'weight': 3, 'color': '#87CEEB', 'effect': 'lightning'},
                'Rasengan': {'weight': 4, 'color': '#ADD8E6', 'effect': 'spiral'},
                'Shadow Clone': {'weight': 5, 'color': '#696969', 'effect': 'shadows'},
                'Fire Release': {'weight': 8, 'color': '#FF4500', 'effect': 'flames'},
                'Water Release': {'weight': 8, 'color': '#4682B4', 'effect': 'water'},
                'Lightning Release': {'weight': 8, 'color': '#FFFF00', 'effect': 'lightning'},
                'Earth Release': {'weight': 8, 'color': '#8B4513', 'effect': 'earth'},
                'Wind Release': {'weight': 8, 'color': '#87CEEB', 'effect': 'wind'},
                'Byakugan Chakra': {'weight': 6, 'color': '#F0F8FF', 'effect': 'gentle_fist'},
                'Sage Mode Chakra': {'weight': 4, 'color': '#FFA500', 'effect': 'nature_energy'},
                'None': {'weight': 35, 'color': 'none', 'effect': 'none'}
            },
            'Rank': {
                'Hokage': {'weight': 1, 'level': 10},
                'Sannin': {'weight': 2, 'level': 9},
                'S-Rank Missing-nin': {'weight': 3, 'level': 8},
                'Kage Level': {'weight': 4, 'level': 8},
                'Jounin': {'weight': 8, 'level': 7},
                'Special Jounin': {'weight': 10, 'level': 6},
                'Chunin': {'weight': 20, 'level': 5},
                'Genin': {'weight': 35, 'level': 4},
                'Academy Student': {'weight': 17, 'level': 1}
            },
            'Weapon': {
                'Sword of Kusanagi': {'weight': 1, 'type': 'legendary'},
                'Samehada': {'weight': 1, 'type': 'legendary'},
                'Executioners Blade': {'weight': 2, 'type': 'legendary'},
                'Twin Fangs': {'weight': 3, 'type': 'rare'},
                'Asuma Chakra Blades': {'weight': 4, 'type': 'rare'},
                'Sasuke Chokuto': {'weight': 5, 'type': 'rare'},
                'Standard Katana': {'weight': 15, 'type': 'common'},
                'Kunai Set': {'weight': 25, 'type': 'common'},
                'Shuriken Pouch': {'weight': 20, 'type': 'common'},
                'Paper Bombs': {'weight': 12, 'type': 'common'},
                'None': {'weight': 12, 'type': 'none'}
            }
        }
        
        self.contract_address = "0x63eb9d77D083cA10C304E28d5191321977fd0Bfb"
        self.chain_id = 999
        
    def weighted_choice(self, trait_dict):
        """Select trait based on rarity weights"""
        total_weight = sum(item['weight'] for item in trait_dict.values())
        choice = random.randint(1, total_weight)
        
        current_weight = 0
        for trait_name, trait_data in trait_dict.items():
            current_weight += trait_data['weight']
            if choice <= current_weight:
                return trait_name, trait_data
        
        return list(trait_dict.items())[0]
    
    def calculate_power_level(self, traits):
        """Calculate ninja power level based on traits"""
        base_power = 1000
        
        # Rank multiplier
        rank_multiplier = traits['rank'][1].get('level', 1)
        base_power *= rank_multiplier
        
        # Eye power bonus
        eye_bonuses = {
            'Mangekyo Sharingan': 5000,
            'Eternal Mangekyo': 8000,
            'Rinnegan': 10000,
            'Tenseigan': 10000,
            'Sharingan (3-Tomoe)': 2000,
            'Byakugan': 1500,
            'Nine-Tails Eyes': 4000,
            'Sage Mode Eyes': 3000
        }
        base_power += eye_bonuses.get(traits['eyes'][0], 0)
        
        # Jutsu power bonus
        jutsu_bonuses = {
            'Nine-Tails Chakra Mode': 8000,
            'Susanoo': 6000,
            'Chidori': 2000,
            'Rasengan': 2500,
            'Sage Mode Chakra': 3000
        }
        base_power += jutsu_bonuses.get(traits['jutsu_aura'][0], 0)
        
        # Weapon bonus
        weapon_bonuses = {
            'legendary': 2000,
            'rare': 1000,
            'common': 200
        }
        base_power += weapon_bonuses.get(traits['weapon'][1].get('type'), 0)
        
        return min(base_power, 50000)  # Cap at 50k
    
    def generate_metadata(self, token_id):
        """Generate comprehensive Naruto NFT metadata"""
        # Select traits
        village_name, village_data = self.weighted_choice(self.traits['Village'])
        eyes_name, eyes_data = self.weighted_choice(self.traits['Eyes'])
        headband_name, headband_data = self.weighted_choice(self.traits['Headband'])
        hair_name, hair_data = self.weighted_choice(self.traits['Hair Style'])
        jutsu_name, jutsu_data = self.weighted_choice(self.traits['Jutsu Aura'])
        rank_name, rank_data = self.weighted_choice(self.traits['Rank'])
        weapon_name, weapon_data = self.weighted_choice(self.traits['Weapon'])
        
        # Store trait data
        selected_traits = {
            'village': (village_name, village_data),
            'eyes': (eyes_name, eyes_data),
            'headband': (headband_name, headband_data),
            'hair': (hair_name, hair_data),
            'jutsu_aura': (jutsu_name, jutsu_data),
            'rank': (rank_name, rank_data),
            'weapon': (weapon_name, weapon_data)
        }
        
        # Calculate power level
        power_level = self.calculate_power_level(selected_traits)
        
        # Calculate rarity score
        rarity_score = sum([
            100 / self.traits['Village'][village_name]['weight'],
            100 / self.traits['Eyes'][eyes_name]['weight'],
            100 / self.traits['Headband'][headband_name]['weight'],
            100 / self.traits['Hair Style'][hair_name]['weight'],
            100 / self.traits['Jutsu Aura'][jutsu_name]['weight'],
            100 / self.traits['Rank'][rank_name]['weight'],
            100 / self.traits['Weapon'][weapon_name]['weight']
        ]) * rank_data['level']
        
        metadata = {
            'name': f'Shinobi #{token_id}',
            'description': f'Elite ninja from the Hidden Villages. Power Level: {power_level:,} | Rarity: {rarity_score:.1f}',
            'image': f'https://naruto-nft.hyperevm.xyz/api/image/{token_id}',
            'external_url': f'https://naruto-nft.hyperevm.xyz/shinobi/{token_id}',
            'attributes': [
                {
                    'trait_type': 'Village',
                    'value': village_name,
                    'rarity': f'{(self.traits["Village"][village_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Eyes',
                    'value': eyes_name,
                    'rarity': f'{(self.traits["Eyes"][eyes_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Headband',
                    'value': headband_name,
                    'rarity': f'{(self.traits["Headband"][headband_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Hair Style',
                    'value': hair_name,
                    'rarity': f'{(self.traits["Hair Style"][hair_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Jutsu Aura',
                    'value': jutsu_name,
                    'rarity': f'{(self.traits["Jutsu Aura"][jutsu_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Ninja Rank',
                    'value': rank_name,
                    'rarity': f'{(self.traits["Rank"][rank_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Weapon',
                    'value': weapon_name,
                    'rarity': f'{(self.traits["Weapon"][weapon_name]["weight"]/100)*100:.1f}%'
                },
                {
                    'trait_type': 'Power Level',
                    'value': power_level,
                    'display_type': 'number'
                },
                {
                    'trait_type': 'Rarity Score',
                    'value': round(rarity_score, 2),
                    'display_type': 'number'
                }
            ],
            'blockchain': 'HyperEVM',
            'chain_id': self.chain_id,
            'contract_address': self.contract_address,
            '_trait_data': selected_traits
        }
        
        return metadata
    
    def create_naruto_svg(self, metadata):
        """Generate detailed Naruto-style SVG artwork"""
        width, height = 512, 512
        traits = metadata['_trait_data']
        
        village_name, village_data = traits['village']
        eyes_name, eyes_data = traits['eyes']
        hair_name, hair_data = traits['hair']
        jutsu_name, jutsu_data = traits['jutsu_aura']
        
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<defs>
    <radialGradient id="chakra" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{jutsu_data.get('color', '#ADD8E6')}" stop-opacity="0.8"/>
        <stop offset="100%" stop-color="{jutsu_data.get('color', '#ADD8E6')}" stop-opacity="0.2"/>
    </radialGradient>
</defs>

<!-- Village Background -->
<rect width="{width}" height="{height}" fill="{village_data['color']}" opacity="0.3"/>
<circle cx="256" cy="256" r="200" fill="none" stroke="{village_data['color']}" stroke-width="3" opacity="0.5"/>

<!-- Village Symbol -->
<text x="50" y="80" font-family="serif" font-size="40" fill="{village_data['color']}" opacity="0.7">{village_data['symbol']}</text>

<!-- Body -->
<ellipse cx="256" cy="300" rx="70" ry="100" fill="#FDBCB4" stroke="#000" stroke-width="2"/>

<!-- Head -->
<circle cx="256" cy="180" r="50" fill="#FDBCB4" stroke="#000" stroke-width="2"/>

<!-- Hair -->
<ellipse cx="256" cy="150" rx="55" ry="35" fill="{hair_data['color']}" stroke="#000" stroke-width="1"/>
'''
        
        # Add specific eye patterns
        if 'Sharingan' in eyes_name:
            if 'Mangekyo' in eyes_name:
                svg_content += '''
<!-- Mangekyo Sharingan -->
<circle cx="240" cy="170" r="12" fill="#FF0000"/>
<polygon points="240,158 245,175 235,175" fill="#000" transform="rotate(0 240 170)"/>
<polygon points="240,158 245,175 235,175" fill="#000" transform="rotate(120 240 170)"/>
<polygon points="240,158 245,175 235,175" fill="#000" transform="rotate(240 240 170)"/>
<circle cx="272" cy="170" r="12" fill="#FF0000"/>
<polygon points="272,158 277,175 267,175" fill="#000" transform="rotate(0 272 170)"/>
<polygon points="272,158 277,175 267,175" fill="#000" transform="rotate(120 272 170)"/>
<polygon points="272,158 277,175 267,175" fill="#000" transform="rotate(240 272 170)"/>
'''
            else:
                tomoe_count = 1 if '1-Tomoe' in eyes_name else (2 if '2-Tomoe' in eyes_name else 3)
                svg_content += f'''
<!-- Sharingan ({tomoe_count}-Tomoe) -->
<circle cx="240" cy="170" r="10" fill="{eyes_data['color']}"/>
<circle cx="272" cy="170" r="10" fill="{eyes_data['color']}"/>
'''
                for i in range(tomoe_count):
                    angle = i * 120
                    svg_content += f'''
<circle cx="240" cy="170" r="2" fill="#000" transform="translate(6 0) rotate({angle} 240 170)"/>
<circle cx="272" cy="170" r="2" fill="#000" transform="translate(6 0) rotate({angle} 272 170)"/>
'''
        elif eyes_name == 'Byakugan':
            svg_content += '''
<!-- Byakugan -->
<ellipse cx="240" cy="170" rx="10" ry="8" fill="#F8F8FF"/>
<ellipse cx="272" cy="170" rx="10" ry="8" fill="#F8F8FF"/>
<line x1="235" y1="170" x2="245" y2="170" stroke="#DDD" stroke-width="1"/>
<line x1="267" y1="170" x2="277" y2="170" stroke="#DDD" stroke-width="1"/>
'''
        elif eyes_name == 'Rinnegan':
            svg_content += '''
<!-- Rinnegan -->
<circle cx="240" cy="170" r="10" fill="#9370DB"/>
<circle cx="272" cy="170" r="10" fill="#9370DB"/>
'''
            for i in range(6):
                radius = 3 + i * 1.5
                svg_content += f'''
<circle cx="240" cy="170" r="{radius}" fill="none" stroke="#000" stroke-width="0.5"/>
<circle cx="272" cy="170" r="{radius}" fill="none" stroke="#000" stroke-width="0.5"/>
'''
        else:
            svg_content += f'''
<!-- Standard Eyes -->
<ellipse cx="240" cy="170" rx="6" ry="8" fill="{eyes_data['color']}"/>
<ellipse cx="272" cy="170" rx="6" ry="8" fill="{eyes_data['color']}"/>
'''
        
        # Add jutsu effects
        if jutsu_name == 'Nine-Tails Chakra Mode':
            svg_content += '''
<!-- Nine-Tails Chakra -->
<circle cx="256" cy="256" r="150" fill="url(#chakra)" opacity="0.6"/>
<path d="M 256 106 Q 226 126 256 156 Q 286 126 256 106" fill="#FFD700" opacity="0.8"/>
'''
        elif jutsu_name == 'Susanoo':
            svg_content += '''
<!-- Susanoo Armor -->
<rect x="206" y="130" width="100" height="200" fill="#4169E1" opacity="0.4" rx="10"/>
<rect x="216" y="140" width="80" height="180" fill="none" stroke="#4169E1" stroke-width="3"/>
'''
        elif jutsu_name == 'Rasengan':
            svg_content += '''
<!-- Rasengan -->
<circle cx="180" cy="280" r="20" fill="#ADD8E6" opacity="0.8"/>
<circle cx="180" cy="280" r="15" fill="#87CEEB" opacity="0.9"/>
<circle cx="180" cy="280" r="10" fill="#4682B4" opacity="0.7"/>
'''
        
        # Add headband
        headband_name, headband_data = traits['headband']
        if 'Headband' in headband_name and headband_name != 'No Headband':
            village_symbol = village_data['symbol'] if headband_data['village'] != 'Rogue' else '×'
            svg_content += f'''
<!-- Ninja Headband -->
<rect x="216" y="140" width="80" height="15" fill="#000080" stroke="#000" stroke-width="1"/>
<rect x="235" y="142" width="42" height="11" fill="#C0C0C0" stroke="#000" stroke-width="1"/>
<text x="256" y="151" font-family="serif" font-size="10" fill="#000" text-anchor="middle">{village_symbol}</text>
'''
        
        # Add weapon
        weapon_name, weapon_data = traits['weapon']
        if weapon_name != 'None':
            if 'Sword' in weapon_name or 'Blade' in weapon_name:
                svg_content += '''
<!-- Sword -->
<line x1="320" y1="280" x2="360" y2="320" stroke="#C0C0C0" stroke-width="4"/>
<rect x="355" y="315" width="8" height="20" fill="#8B4513"/>
'''
            elif 'Kunai' in weapon_name:
                svg_content += '''
<!-- Kunai -->
<polygon points="350,290 360,285 365,295 355,300" fill="#C0C0C0"/>
<rect x="350" y="295" width="2" height="15" fill="#8B4513"/>
'''
        
        # Power level indicator
        power_level = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Power Level')
        bar_width = min((power_level / 50000) * 100, 100)
        bar_color = '#FF0000' if power_level > 30000 else '#FFA500' if power_level > 15000 else '#00FF00'
        
        svg_content += f'''
<!-- Power Level Bar -->
<rect x="20" y="450" width="100" height="8" fill="#333" stroke="#000" stroke-width="1"/>
<rect x="20" y="450" width="{bar_width}" height="8" fill="{bar_color}"/>
<text x="20" y="470" font-family="Arial" font-size="10" fill="#000">Power: {power_level:,}</text>

<!-- HyperEVM Signature -->
<text x="10" y="500" fill="#666" font-family="Arial" font-size="8">Naruto NFT - HyperEVM</text>
</svg>'''
        
        return svg_content
    
    def generate_collection(self, size=1000, name="Shinobi Warriors"):
        """Generate Naruto NFT collection"""
        folder = f'naruto_collection_{int(datetime.now().timestamp())}'
        os.makedirs(f'{folder}/images', exist_ok=True)
        os.makedirs(f'{folder}/metadata', exist_ok=True)
        
        collection_stats = {
            'total_power': 0,
            'hokage_count': 0,
            'legendary_eyes': 0,
            'village_distribution': {},
            'rarity_distribution': {}
        }
        
        print(f"Generating {size} Naruto-themed NFTs...")
        
        for token_id in range(1, size + 1):
            metadata = self.generate_metadata(token_id)
            svg_content = self.create_naruto_svg(metadata)
            
            # Save files
            with open(f'{folder}/images/{token_id}.svg', 'w') as f:
                f.write(svg_content)
            
            clean_metadata = {k: v for k, v in metadata.items() if not k.startswith('_')}
            with open(f'{folder}/metadata/{token_id}', 'w') as f:
                json.dump(clean_metadata, f, indent=2)
            
            # Track stats
            power = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Power Level')
            village = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Village')
            rank = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Ninja Rank')
            
            collection_stats['total_power'] += power
            collection_stats['village_distribution'][village] = collection_stats['village_distribution'].get(village, 0) + 1
            collection_stats['rarity_distribution'][rank] = collection_stats['rarity_distribution'].get(rank, 0) + 1
            
            if rank == 'Hokage':
                collection_stats['hokage_count'] += 1
            
            if token_id % 100 == 0:
                print(f"Generated {token_id}/{size} shinobi...")
        
        # Save collection info
        collection_info = {
            'name': name,
            'description': 'Elite shinobi collection featuring detailed Naruto universe traits, village affiliations, and power systems',
            'total_supply': size,
            'blockchain': 'HyperEVM',
            'contract_address': self.contract_address,
            'statistics': collection_stats,
            'average_power': collection_stats['total_power'] // size
        }
        
        with open(f'{folder}/collection.json', 'w') as f:
            json.dump(collection_info, f, indent=2)
        
        return folder, collection_info

if __name__ == "__main__":
    generator = NarutoNFTGenerator()
    
    print("🍥 Naruto NFT Collection Generator")
    print("=" * 50)
    
    # Generate sample collection
    folder, info = generator.generate_collection(20, "Hidden Village Shinobi")
    
    print(f"\n✅ Collection '{info['name']}' generated!")
    print(f"📁 Location: {folder}/")
    print(f"⚡ Average Power Level: {info['average_power']:,}")
    print(f"🏛️ Total Hokage: {info['statistics']['hokage_count']}")
    
    print(f"\n🏘️ Village Distribution:")
    for village, count in sorted(info['statistics']['village_distribution'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / info['total_supply']) * 100
        print(f"   {village}: {count} ({percentage:.1f}%)")