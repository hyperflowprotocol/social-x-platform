#!/usr/bin/env python3
"""
Clean Art Viewer - Professional Naruto NFT Collection Display
Uses actual reference quality images and authentic character designs
"""

import http.server
import socketserver
import os
import base64
import json
import time

PORT = 5000

class CleanArtHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        print(f"Request: {self.path}")
        
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Find reference quality collection
            collection_folders = []
            for folder in os.listdir('.'):
                if folder.startswith('reference_quality_') and os.path.isdir(folder):
                    collection_folders.append(folder)
            
            if not collection_folders:
                self.wfile.write(b"No reference quality collections found")
                return
            
            # Use the latest collection
            collection_folder = sorted(collection_folders)[-1]
            images_dir = os.path.join(collection_folder, "images")
            
            print(f"Using collection: {collection_folder}")
            print(f"Images directory: {images_dir}")
            
            if not os.path.exists(images_dir):
                self.wfile.write(f"Images directory not found: {images_dir}".encode())
                return
            
            # Get all PNG images
            image_files = [f for f in os.listdir(images_dir) if f.lower().endswith('.png')]
            image_files.sort(key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else 0)
            
            print(f"Found {len(image_files)} images: {image_files[:5]}...")
            
            # Professional character data
            naruto_characters = [
                {"name": "Naruto Uzumaki", "village": "Leaf", "jutsu": "Rasengan", "element": "Wind", "rarity": "Legendary"},
                {"name": "Sasuke Uchiha", "village": "Leaf", "jutsu": "Chidori", "element": "Lightning", "rarity": "Legendary"},
                {"name": "Itachi Uchiha", "village": "Leaf", "jutsu": "Amaterasu", "element": "Fire", "rarity": "Mythic"},
                {"name": "Kakashi Hatake", "village": "Leaf", "jutsu": "Lightning Blade", "element": "Lightning", "rarity": "Epic"},
                {"name": "Sakura Haruno", "village": "Leaf", "jutsu": "Healing", "element": "Medical", "rarity": "Rare"},
                {"name": "Gaara", "village": "Sand", "jutsu": "Sand Prison", "element": "Earth", "rarity": "Epic"},
                {"name": "Rock Lee", "village": "Leaf", "jutsu": "Eight Gates", "element": "Taijutsu", "rarity": "Rare"},
                {"name": "Hinata Hyuga", "village": "Leaf", "jutsu": "Byakugan", "element": "Gentle Fist", "rarity": "Epic"},
                {"name": "Neji Hyuga", "village": "Leaf", "jutsu": "Rotation", "element": "Gentle Fist", "rarity": "Rare"},
                {"name": "Shikamaru Nara", "village": "Leaf", "jutsu": "Shadow Bind", "element": "Shadow", "rarity": "Uncommon"},
                {"name": "Choji Akimichi", "village": "Leaf", "jutsu": "Expansion", "element": "Yang", "rarity": "Uncommon"},
                {"name": "Ino Yamanaka", "village": "Leaf", "jutsu": "Mind Transfer", "element": "Yin", "rarity": "Uncommon"},
                {"name": "Kiba Inuzuka", "village": "Leaf", "jutsu": "Fang Over Fang", "element": "Beast", "rarity": "Common"},
                {"name": "Shino Aburame", "village": "Leaf", "jutsu": "Insect Control", "element": "Bugs", "rarity": "Common"},
                {"name": "Tenten", "village": "Leaf", "jutsu": "Weapon Summon", "element": "Tools", "rarity": "Common"},
                {"name": "Might Guy", "village": "Leaf", "jutsu": "Eight Gates", "element": "Taijutsu", "rarity": "Epic"},
                {"name": "Asuma Sarutobi", "village": "Leaf", "jutsu": "Wind Blade", "element": "Wind", "rarity": "Rare"},
                {"name": "Kurenai Yuhi", "village": "Leaf", "jutsu": "Genjutsu", "element": "Illusion", "rarity": "Rare"},
                {"name": "Jiraiya", "village": "Leaf", "jutsu": "Rasengan", "element": "Fire", "rarity": "Legendary"},
                {"name": "Tsunade", "village": "Leaf", "jutsu": "Hundred Healings", "element": "Medical", "rarity": "Legendary"}
            ]
            
            # Create NFT gallery
            gallery_html = ""
            loaded_count = 0
            
            for i, img_file in enumerate(image_files[:20], 1):
                try:
                    img_path = os.path.join(images_dir, img_file)
                    with open(img_path, 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode('utf-8')
                        
                        character = naruto_characters[(i-1) % len(naruto_characters)]
                        
                        # Calculate stats
                        power = 75 + (i * 3) % 25
                        speed = 70 + (i * 5) % 30  
                        chakra = 80 + (i * 7) % 20
                        
                        rarity_colors = {
                            "Common": "#9e9e9e",
                            "Uncommon": "#4caf50", 
                            "Rare": "#2196f3",
                            "Epic": "#9c27b0",
                            "Legendary": "#ff9800",
                            "Mythic": "#e91e63"
                        }
                        
                        rarity_color = rarity_colors.get(character["rarity"], "#9e9e9e")
                        
                        gallery_html += f'''
                        <div class="nft-card" data-rarity="{character['rarity'].lower()}">
                            <div class="card-header">
                                <span class="nft-id">#{i:03d}</span>
                                <div class="rarity-badge" style="background: {rarity_color};">
                                    {character["rarity"]}
                                </div>
                            </div>
                            
                            <div class="nft-image">
                                <img src="data:image/png;base64,{img_data}" alt="{character['name']}" loading="lazy">
                                <div class="image-overlay">
                                    <div class="village-badge">{character["village"]} Village</div>
                                </div>
                            </div>
                            
                            <div class="card-content">
                                <h3 class="character-name">{character['name']}</h3>
                                <p class="signature-jutsu">Signature: {character['jutsu']}</p>
                                <div class="element-tag" style="background: linear-gradient(45deg, {rarity_color}22, {rarity_color}44);">
                                    {character['element']} Style
                                </div>
                                
                                <div class="stats-grid">
                                    <div class="stat-item">
                                        <div class="stat-label">Power</div>
                                        <div class="stat-bar">
                                            <div class="stat-fill" style="width: {power}%; background: #ff4444;"></div>
                                        </div>
                                        <div class="stat-value">{power}</div>
                                    </div>
                                    <div class="stat-item">
                                        <div class="stat-label">Speed</div>
                                        <div class="stat-bar">
                                            <div class="stat-fill" style="width: {speed}%; background: #44ff44;"></div>
                                        </div>
                                        <div class="stat-value">{speed}</div>
                                    </div>
                                    <div class="stat-item">
                                        <div class="stat-label">Chakra</div>
                                        <div class="stat-bar">
                                            <div class="stat-fill" style="width: {chakra}%; background: #4444ff;"></div>
                                        </div>
                                        <div class="stat-value">{chakra}</div>
                                    </div>
                                </div>
                            </div>
                        </div>'''
                        
                        loaded_count += 1
                        print(f"Loaded #{i}: {character['name']}")
                        
                except Exception as e:
                    print(f"Error loading {img_file}: {e}")
            
            # Complete HTML page
            html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Professional Naruto NFT Collection</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(45deg, #ff6b35, #f7931e, #ffb347);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            color: #ccc;
            margin-bottom: 30px;
        }}
        
        .collection-stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
        }}
        
        .stat-box {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 15px;
            padding: 20px 30px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #ff6b35;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #aaa;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .nft-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
        }}
        
        .nft-card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
            border-color: rgba(255,107,53,0.5);
        }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            background: rgba(0,0,0,0.3);
        }}
        
        .nft-id {{
            font-weight: bold;
            color: #ff6b35;
            font-size: 1.1rem;
        }}
        
        .rarity-badge {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
            color: white;
        }}
        
        .nft-image {{
            position: relative;
            height: 300px;
            overflow: hidden;
        }}
        
        .nft-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s ease;
        }}
        
        .nft-card:hover .nft-image img {{
            transform: scale(1.1);
        }}
        
        .image-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            padding: 20px;
            display: flex;
            justify-content: flex-end;
        }}
        
        .village-badge {{
            background: rgba(255,107,53,0.8);
            color: white;
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        .card-content {{
            padding: 25px;
        }}
        
        .character-name {{
            font-size: 1.4rem;
            font-weight: bold;
            color: #fff;
            margin-bottom: 8px;
        }}
        
        .signature-jutsu {{
            color: #ff6b35;
            font-size: 0.95rem;
            margin-bottom: 15px;
            font-style: italic;
        }}
        
        .element-tag {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .stats-grid {{
            display: grid;
            gap: 12px;
        }}
        
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .stat-label {{
            font-size: 0.85rem;
            color: #ccc;
            width: 50px;
            text-align: right;
        }}
        
        .stat-bar {{
            flex: 1;
            height: 6px;
            background: rgba(255,255,255,0.2);
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .stat-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 0.8s ease;
        }}
        
        .stat-value {{
            font-weight: bold;
            color: #fff;
            width: 30px;
            text-align: center;
            font-size: 0.9rem;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 60px;
            padding: 30px;
            background: rgba(0,0,0,0.3);
            border-radius: 20px;
        }}
        
        .achievement {{
            color: #ff6b35;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        @media (max-width: 768px) {{
            .gallery {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .collection-stats {{
                gap: 20px;
            }}
            
            .stat-box {{
                padding: 15px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Professional Naruto NFT Collection</h1>
        <p class="subtitle">Authentic Anime Characters • Reference Quality Artwork</p>
        
        <div class="collection-stats">
            <div class="stat-box">
                <div class="stat-number">{loaded_count}</div>
                <div class="stat-label">NFTs Loaded</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(image_files)}</div>
                <div class="stat-label">Total Supply</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">Pro</div>
                <div class="stat-label">Quality Grade</div>
            </div>
        </div>
    </div>
    
    <div class="gallery">
        {gallery_html}
    </div>
    
    <div class="footer">
        <div class="achievement">Collection Complete!</div>
        <p>Professional Naruto NFT artwork with authentic character designs and stats</p>
    </div>
</body>
</html>'''
            
            self.wfile.write(html.encode('utf-8'))
            print(f"Served professional collection with {loaded_count} NFTs")
            
        else:
            self.send_error(404)

print("Professional Naruto NFT Collection")
print("=" * 50)
print(f"Starting clean art viewer on port {PORT}")
print(f"Access at: http://0.0.0.0:{PORT}")
print("=" * 50)

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), CleanArtHandler) as httpd:
        print(f"Clean Art Gallery running on port {PORT}")
        httpd.serve_forever()
except Exception as e:
    print(f"Error starting server: {e}")
    print("Trying alternative port 5010...")
    PORT = 5010
    with socketserver.TCPServer(("0.0.0.0", PORT), CleanArtHandler) as httpd:
        print(f"Clean Art Gallery running on port {PORT}")
        httpd.serve_forever()