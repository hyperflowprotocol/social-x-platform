#!/usr/bin/env python3
"""
Working Art Display - Shows existing reference quality Naruto character images
"""

import http.server
import socketserver
import os
import base64
import json

PORT = 5000

# Professional character database
NARUTO_CHARACTERS = [
    {"name": "Naruto Uzumaki", "village": "Hidden Leaf", "jutsu": "Rasengan", "element": "Wind Release", "rarity": "Legendary", "description": "The Seventh Hokage with Nine-Tails chakra"},
    {"name": "Sasuke Uchiha", "village": "Hidden Leaf", "jutsu": "Chidori", "element": "Lightning Release", "rarity": "Legendary", "description": "Last Uchiha with Sharingan and Rinnegan"},
    {"name": "Itachi Uchiha", "village": "Hidden Leaf", "jutsu": "Amaterasu", "element": "Fire Release", "rarity": "Mythic", "description": "Prodigy with Mangekyou Sharingan"},
    {"name": "Kakashi Hatake", "village": "Hidden Leaf", "jutsu": "Lightning Blade", "element": "Lightning Release", "rarity": "Epic", "description": "Copy Ninja with 1000+ jutsu"},
    {"name": "Sakura Haruno", "village": "Hidden Leaf", "jutsu": "Healing Palm", "element": "Medical Ninjutsu", "rarity": "Epic", "description": "Tsunade's student with super strength"},
    {"name": "Gaara", "village": "Hidden Sand", "jutsu": "Sand Prison", "element": "Earth Release", "rarity": "Epic", "description": "Fifth Kazekage with sand control"},
    {"name": "Rock Lee", "village": "Hidden Leaf", "jutsu": "Eight Gates", "element": "Taijutsu", "rarity": "Rare", "description": "Master of taijutsu"},
    {"name": "Hinata Hyuga", "village": "Hidden Leaf", "jutsu": "Byakugan", "element": "Gentle Fist", "rarity": "Epic", "description": "Heiress with all-seeing eyes"},
    {"name": "Neji Hyuga", "village": "Hidden Leaf", "jutsu": "Rotation", "element": "Gentle Fist", "rarity": "Rare", "description": "Branch family prodigy"},
    {"name": "Shikamaru Nara", "village": "Hidden Leaf", "jutsu": "Shadow Bind", "element": "Shadow Release", "rarity": "Uncommon", "description": "Genius strategist"},
    {"name": "Choji Akimichi", "village": "Hidden Leaf", "jutsu": "Expansion", "element": "Yang Release", "rarity": "Uncommon", "description": "Size manipulation expert"},
    {"name": "Ino Yamanaka", "village": "Hidden Leaf", "jutsu": "Mind Transfer", "element": "Yin Release", "rarity": "Uncommon", "description": "Mind control specialist"},
    {"name": "Kiba Inuzuka", "village": "Hidden Leaf", "jutsu": "Fang Over Fang", "element": "Beast Style", "rarity": "Common", "description": "Animal partner fighter"},
    {"name": "Shino Aburame", "village": "Hidden Leaf", "jutsu": "Insect Control", "element": "Bug Style", "rarity": "Common", "description": "Insect user"},
    {"name": "Tenten", "village": "Hidden Leaf", "jutsu": "Weapon Summon", "element": "Tool Style", "rarity": "Common", "description": "Weapons specialist"},
    {"name": "Might Guy", "village": "Hidden Leaf", "jutsu": "Eight Gates", "element": "Taijutsu", "rarity": "Epic", "description": "Green Beast of Konoha"},
    {"name": "Asuma Sarutobi", "village": "Hidden Leaf", "jutsu": "Wind Blade", "element": "Wind Release", "rarity": "Rare", "description": "Wind chakra blades"},
    {"name": "Kurenai Yuhi", "village": "Hidden Leaf", "jutsu": "Genjutsu", "element": "Illusion Style", "rarity": "Rare", "description": "Genjutsu master"},
    {"name": "Jiraiya", "village": "Hidden Leaf", "jutsu": "Summoning", "element": "Fire Release", "rarity": "Legendary", "description": "Legendary Sannin"},
    {"name": "Tsunade", "village": "Hidden Leaf", "jutsu": "Hundred Healings", "element": "Medical Ninjutsu", "rarity": "Legendary", "description": "Fifth Hokage"}
]

class WorkingArtHandler(http.server.BaseHTTPRequestHandler):
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
            
            # Find authentic character collection first, then reference quality as fallback
            collection_folders = [f for f in os.listdir('.') if f.startswith('authentic_naruto_') and os.path.isdir(f)]
            if not collection_folders:
                collection_folders = [f for f in os.listdir('.') if f.startswith('reference_quality_') and os.path.isdir(f)]
            
            if not collection_folders:
                self.wfile.write(b"No reference quality collections found")
                return
            
            print(f"Found folders: {collection_folders}")
            
            # Use the latest folder
            collection_folder = sorted(collection_folders)[-1]
            print(f"Using folder: {collection_folder}")
            
            images_dir = os.path.join(collection_folder, "images")
            print(f"Images dir: {images_dir}")
            
            if not os.path.exists(images_dir):
                self.wfile.write(f"Images directory not found: {images_dir}".encode())
                return
            
            image_files = [f for f in os.listdir(images_dir) if f.lower().endswith('.png')]
            image_files.sort(key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else 0)
            
            print(f"Found {len(image_files)} images: {image_files[:3]}...")
            
            # Generate NFT gallery
            gallery_html = ""
            loaded_count = 0
            
            for i, img_file in enumerate(image_files[:20], 1):
                try:
                    img_path = os.path.join(images_dir, img_file)
                    with open(img_path, 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode('utf-8')
                    
                    character = NARUTO_CHARACTERS[(i-1) % len(NARUTO_CHARACTERS)]
                    
                    # Generate stats
                    base_power = {"Legendary": 95, "Mythic": 99, "Epic": 88, "Rare": 75, "Uncommon": 65, "Common": 50}
                    power = base_power.get(character["rarity"], 70) + (i % 10)
                    speed = power - 10 + (i * 3 % 15) 
                    chakra = power - 5 + (i * 7 % 12)
                    
                    # Rarity styling
                    rarity_styles = {
                        "Legendary": {"color": "#FFD700", "glow": "#FFD700"},
                        "Mythic": {"color": "#FF1493", "glow": "#FF69B4"},
                        "Epic": {"color": "#9932CC", "glow": "#DA70D6"}, 
                        "Rare": {"color": "#4169E1", "glow": "#6495ED"},
                        "Uncommon": {"color": "#32CD32", "glow": "#90EE90"},
                        "Common": {"color": "#808080", "glow": "#A9A9A9"}
                    }
                    
                    style = rarity_styles.get(character["rarity"], {"color": "#888", "glow": "#AAA"})
                    
                    gallery_html += f'''
                    <div class="nft-card" data-rarity="{character['rarity'].lower()}">
                        <div class="card-glow" style="background: radial-gradient(circle, {style['glow']}22 0%, transparent 70%);"></div>
                        
                        <div class="card-header">
                            <div class="nft-number">#{i:03d}</div>
                            <div class="rarity-badge" style="background: {style['color']}; box-shadow: 0 0 20px {style['glow']};">
                                {character['rarity']}
                            </div>
                        </div>
                        
                        <div class="nft-image-container">
                            <img src="data:image/png;base64,{img_data}" alt="{character['name']}" loading="lazy">
                            <div class="image-gradient"></div>
                            <div class="village-tag">{character['village']}</div>
                        </div>
                        
                        <div class="card-content">
                            <h2 class="character-name">{character['name']}</h2>
                            <p class="character-description">{character['description']}</p>
                            
                            <div class="jutsu-section">
                                <div class="jutsu-name">Signature: {character['jutsu']}</div>
                                <div class="element-type">{character['element']}</div>
                            </div>
                            
                            <div class="stats-section">
                                <h4>Combat Stats</h4>
                                <div class="stat-row">
                                    <span class="stat-label">Power</span>
                                    <div class="stat-bar">
                                        <div class="stat-fill power" style="width: {power}%"></div>
                                    </div>
                                    <span class="stat-value">{power}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label">Speed</span>
                                    <div class="stat-bar">
                                        <div class="stat-fill speed" style="width: {speed}%"></div>
                                    </div>
                                    <span class="stat-value">{speed}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label">Chakra</span>
                                    <div class="stat-bar">
                                        <div class="stat-fill chakra" style="width: {chakra}%"></div>
                                    </div>
                                    <span class="stat-value">{chakra}</span>
                                </div>
                            </div>
                        </div>
                    </div>'''
                    
                    loaded_count += 1
                    print(f"Loaded NFT #{i}: {character['name']}")
                    
                except Exception as e:
                    print(f"Error loading {img_file}: {e}")
            
            # Create complete HTML page
            html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Professional Naruto Character Collection</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 25%, #16213e 50%, #0f3460 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            padding: 50px 20px;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 900;
            background: linear-gradient(45deg, #ff6b35, #f7931e, #ffb347, #ff6b35);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            animation: gradientShift 3s ease-in-out infinite;
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            color: #ccc;
            margin-bottom: 30px;
        }}
        
        .collection-stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-bottom: 40px;
        }}
        
        .stat-box {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 15px;
            padding: 20px 30px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #ff6b35;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #aaa;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .nft-card {{
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(30px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            overflow: hidden;
            position: relative;
            transition: all 0.4s ease;
        }}
        
        .nft-card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
            border-color: rgba(255,107,53,0.4);
        }}
        
        .card-glow {{
            position: absolute;
            top: -50%;
            left: -50%;
            right: -50%;
            bottom: -50%;
            opacity: 0;
            transition: opacity 0.4s ease;
        }}
        
        .nft-card:hover .card-glow {{ opacity: 1; }}
        
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            background: rgba(0,0,0,0.4);
        }}
        
        .nft-number {{
            font-size: 1.1rem;
            font-weight: bold;
            color: #ff6b35;
        }}
        
        .rarity-badge {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
            color: white;
        }}
        
        .nft-image-container {{
            position: relative;
            height: 300px;
            overflow: hidden;
        }}
        
        .nft-image-container img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s ease;
        }}
        
        .nft-card:hover .nft-image-container img {{
            transform: scale(1.05);
        }}
        
        .image-gradient {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 40%;
            background: linear-gradient(transparent 0%, rgba(0,0,0,0.7) 100%);
        }}
        
        .village-tag {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.8);
            color: #ff6b35;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .card-content {{ padding: 25px; }}
        
        .character-name {{
            font-size: 1.4rem;
            font-weight: bold;
            color: #fff;
            margin-bottom: 10px;
        }}
        
        .character-description {{
            color: #ddd;
            line-height: 1.4;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }}
        
        .jutsu-section {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding: 12px;
            background: rgba(255,107,53,0.1);
            border-radius: 10px;
            border: 1px solid rgba(255,107,53,0.2);
        }}
        
        .jutsu-name {{
            color: #ff6b35;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        
        .element-type {{
            color: #ccc;
            font-size: 0.8rem;
            font-style: italic;
        }}
        
        .stats-section h4 {{
            color: #ff6b35;
            margin-bottom: 12px;
            font-size: 1rem;
        }}
        
        .stat-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: #ccc;
            font-size: 0.85rem;
            width: 55px;
            text-align: right;
        }}
        
        .stat-bar {{
            flex: 1;
            height: 7px;
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .stat-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 1s ease-out;
        }}
        
        .stat-fill.power {{ background: linear-gradient(90deg, #ff4444, #ff6666); }}
        .stat-fill.speed {{ background: linear-gradient(90deg, #44ff44, #66ff66); }}
        .stat-fill.chakra {{ background: linear-gradient(90deg, #4444ff, #6666ff); }}
        
        .stat-value {{
            color: #fff;
            font-weight: bold;
            width: 30px;
            text-align: center;
            font-size: 0.85rem;
        }}
        
        @media (max-width: 768px) {{
            .gallery {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .collection-stats {{ gap: 20px; }}
            .stat-box {{ padding: 15px 20px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Professional Naruto Collection</h1>
        <p class="subtitle">Authentic Character Artwork • Professional Quality</p>
        
        <div class="collection-stats">
            <div class="stat-box">
                <div class="stat-number">{loaded_count}</div>
                <div class="stat-label">Characters</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(image_files)}</div>
                <div class="stat-label">Total Supply</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">HD</div>
                <div class="stat-label">Quality</div>
            </div>
        </div>
    </div>
    
    <div class="gallery">
        {gallery_html}
    </div>
</body>
</html>'''
            
            self.wfile.write(html.encode('utf-8'))
            print(f"Served page with {loaded_count} NFTs")
            
        else:
            self.send_error(404)

print("Working Art Display - Professional Naruto Collection")
print("=" * 50)
print(f"Starting gallery on port {PORT}")
print("Displaying existing reference quality character artwork")
print("=" * 50)

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), WorkingArtHandler) as httpd:
        print(f"Gallery running on port {PORT}")
        httpd.serve_forever()
except Exception as e:
    print(f"Error starting server: {e}")
    # Try alternative port
    PORT = 5025
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), WorkingArtHandler) as httpd:
            print(f"Gallery running on port {PORT}")
            httpd.serve_forever()
    except Exception as e2:
        print(f"Failed on backup port: {e2}")