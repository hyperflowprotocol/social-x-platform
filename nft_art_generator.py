#!/usr/bin/env python3
"""
NFT Art Generator - Creates unique digital artwork as SVG files
Generates procedural art with randomized traits for NFT collections
"""

import random
import json
import os
from datetime import datetime
import hashlib

class NFTArtGenerator:
    def __init__(self):
        self.colors = {
            'backgrounds': ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#7209b7'],
            'primary': ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'],
            'secondary': ['#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43'],
            'accent': ['#ffd93d', '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894']
        }
        
        self.shapes = ['circle', 'polygon', 'star', 'hexagon', 'diamond']
        self.patterns = ['gradient', 'stripes', 'dots', 'waves', 'geometric']
        self.effects = ['glow', 'shadow', 'blur', 'none']
        
    def generate_metadata(self, token_id):
        """Generate metadata for NFT"""
        background = random.choice(self.colors['backgrounds'])
        primary_color = random.choice(self.colors['primary'])
        secondary_color = random.choice(self.colors['secondary'])
        accent_color = random.choice(self.colors['accent'])
        
        shape = random.choice(self.shapes)
        pattern = random.choice(self.patterns)
        effect = random.choice(self.effects)
        
        complexity = random.randint(3, 8)
        size_variation = random.uniform(0.5, 2.0)
        
        metadata = {
            'name': f'Generated Art #{token_id}',
            'description': 'Unique procedurally generated digital artwork',
            'image': f'art_{token_id}.svg',
            'attributes': [
                {'trait_type': 'Background', 'value': background},
                {'trait_type': 'Primary Color', 'value': primary_color},
                {'trait_type': 'Secondary Color', 'value': secondary_color},
                {'trait_type': 'Accent Color', 'value': accent_color},
                {'trait_type': 'Shape Type', 'value': shape},
                {'trait_type': 'Pattern', 'value': pattern},
                {'trait_type': 'Effect', 'value': effect},
                {'trait_type': 'Complexity', 'value': complexity},
                {'trait_type': 'Size Variation', 'value': round(size_variation, 2)}
            ]
        }
        
        return metadata
    
    def create_gradient(self, color1, color2, gradient_id):
        """Create SVG gradient definition"""
        return f'''
        <defs>
            <linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
            </linearGradient>
        </defs>
        '''
    
    def create_circle(self, cx, cy, r, fill, opacity=1.0, effect=None):
        """Create SVG circle"""
        effect_attrs = ""
        if effect == "glow":
            effect_attrs = f'filter="url(#glow)"'
        elif effect == "shadow":
            effect_attrs = f'filter="url(#shadow)"'
        
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" opacity="{opacity}" {effect_attrs}/>'
    
    def create_polygon(self, points, fill, opacity=1.0):
        """Create SVG polygon"""
        points_str = " ".join([f"{x},{y}" for x, y in points])
        return f'<polygon points="{points_str}" fill="{fill}" opacity="{opacity}"/>'
    
    def create_star(self, cx, cy, size, fill, opacity=1.0):
        """Create SVG star shape"""
        points = []
        for i in range(10):
            angle = (i * 36) * (3.14159 / 180)
            radius = size if i % 2 == 0 else size * 0.5
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))
        
        return self.create_polygon(points, fill, opacity)
    
    def create_effects(self):
        """Create SVG filter effects"""
        return '''
        <defs>
            <filter id="glow">
                <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
            <filter id="shadow">
                <feDropShadow dx="4" dy="4" stdDeviation="3" flood-opacity="0.3"/>
            </filter>
        </defs>
        '''
    
    def generate_art(self, metadata):
        """Generate SVG art based on metadata"""
        width, height = 512, 512
        background = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Background')
        primary = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Primary Color')
        secondary = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Secondary Color')
        accent = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Accent Color')
        shape = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Shape Type')
        pattern = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Pattern')
        effect = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Effect')
        complexity = next(attr['value'] for attr in metadata['attributes'] if attr['trait_type'] == 'Complexity')
        
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
{self.create_effects()}
{self.create_gradient(primary, secondary, "mainGrad")}
{self.create_gradient(secondary, accent, "accentGrad")}
        
<!-- Background -->
<rect width="{width}" height="{height}" fill="{background}"/>
'''
        
        # Generate main shapes based on complexity
        for i in range(complexity):
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            size = random.randint(20, 100)
            opacity = random.uniform(0.3, 0.9)
            
            fill_color = random.choice([primary, secondary, accent, "url(#mainGrad)", "url(#accentGrad)"])
            
            if shape == 'circle':
                svg_content += self.create_circle(x, y, size, fill_color, opacity, effect if i == 0 else None)
            elif shape == 'polygon':
                # Create random polygon
                points = []
                for _ in range(random.randint(3, 8)):
                    px = x + random.randint(-size, size)
                    py = y + random.randint(-size, size)
                    points.append((px, py))
                svg_content += self.create_polygon(points, fill_color, opacity)
        
        # Add pattern overlay
        if pattern == 'dots':
            for _ in range(20):
                dot_x = random.randint(0, width)
                dot_y = random.randint(0, height)
                dot_size = random.randint(2, 8)
                svg_content += self.create_circle(dot_x, dot_y, dot_size, accent, 0.5)
        
        elif pattern == 'stripes':
            for i in range(0, width, 30):
                svg_content += f'<line x1="{i}" y1="0" x2="{i}" y2="{height}" stroke="{accent}" stroke-width="2" opacity="0.2"/>'
        
        svg_content += '</svg>'
        return svg_content
    
    def generate_collection(self, count=10):
        """Generate a collection of NFT artworks"""
        os.makedirs('nft_collection', exist_ok=True)
        os.makedirs('nft_collection/images', exist_ok=True)
        os.makedirs('nft_collection/metadata', exist_ok=True)
        
        collection_metadata = {
            'name': 'Generated Art Collection',
            'description': 'Unique procedurally generated digital artworks',
            'created_at': datetime.now().isoformat(),
            'total_supply': count,
            'items': []
        }
        
        for i in range(1, count + 1):
            # Generate metadata
            metadata = self.generate_metadata(i)
            
            # Generate artwork
            svg_art = self.generate_art(metadata)
            
            # Save files
            with open(f'nft_collection/images/art_{i}.svg', 'w') as f:
                f.write(svg_art)
            
            with open(f'nft_collection/metadata/{i}.json', 'w') as f:
                json.dump(metadata, f, indent=2)
            
            collection_metadata['items'].append({
                'token_id': i,
                'name': metadata['name'],
                'rarity_score': self.calculate_rarity(metadata)
            })
            
            print(f"Generated NFT #{i}: {metadata['name']}")
        
        # Save collection metadata
        with open('nft_collection/collection.json', 'w') as f:
            json.dump(collection_metadata, f, indent=2)
        
        return collection_metadata
    
    def calculate_rarity(self, metadata):
        """Calculate basic rarity score"""
        score = 0
        for attr in metadata['attributes']:
            if attr['trait_type'] == 'Complexity':
                score += attr['value'] * 10
            elif attr['trait_type'] == 'Effect' and attr['value'] != 'none':
                score += 20
        return score

if __name__ == "__main__":
    import math
    
    generator = NFTArtGenerator()
    
    print("🎨 NFT Art Generator")
    print("=" * 50)
    
    try:
        count = int(input("How many NFTs to generate? (1-100): ") or "10")
        count = max(1, min(count, 100))
    except ValueError:
        count = 10
    
    print(f"\nGenerating {count} unique NFT artworks...")
    
    collection = generator.generate_collection(count)
    
    print(f"\n✅ Collection Generated Successfully!")
    print(f"📁 Files saved in: ./nft_collection/")
    print(f"🖼️  Images: ./nft_collection/images/")
    print(f"📄 Metadata: ./nft_collection/metadata/")
    print(f"📊 Collection info: ./nft_collection/collection.json")
    
    # Display some stats
    rarities = [item['rarity_score'] for item in collection['items']]
    print(f"\n📈 Rarity Stats:")
    print(f"   Average rarity: {sum(rarities)/len(rarities):.1f}")
    print(f"   Highest rarity: {max(rarities)}")
    print(f"   Lowest rarity: {min(rarities)}")