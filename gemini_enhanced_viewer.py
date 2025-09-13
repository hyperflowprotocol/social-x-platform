#!/usr/bin/env python3
"""
Gemini Enhanced Viewer - Displays AI-generated professional Naruto artwork
"""

import http.server
import socketserver
import os
import json
import base64

PORT = 5000

class GeminiEnhancedHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            print("Request: /")
            
            # Find AI-generated collections
            collection_folders = [f for f in os.listdir('.') if f.startswith('gemini_naruto_') and os.path.isdir(f)]
            if not collection_folders:
                # Fallback to professional collections
                collection_folders = [f for f in os.listdir('.') if f.startswith('professional_naruto_') and os.path.isdir(f)]
            if not collection_folders:
                # Final fallback to reference quality
                collection_folders = [f for f in os.listdir('.') if f.startswith('reference_quality_') and os.path.isdir(f)]
            
            if not collection_folders:
                self.wfile.write(b"<h1>No AI collection found</h1>")
                return
                
            collection_folder = collection_folders[0]
            images_dir = os.path.join(collection_folder, "images")
            metadata_dir = os.path.join(collection_folder, "metadata")
            
            if not os.path.exists(images_dir):
                self.wfile.write(b"<h1>Images directory not found</h1>")
                return
                
            gallery_html = ""
            image_files = sorted([f for f in os.listdir(images_dir) if f.endswith('.png')])
            
            print(f"Found {len(image_files)} professional images")
            
            for image_file in image_files[:20]:  # Show all 20
                try:
                    image_path = os.path.join(images_dir, image_file)
                    metadata_path = os.path.join(metadata_dir, image_file.replace('.png', '.json'))
                    
                    # Load metadata
                    character_info = {"name": "AI Naruto Character", "description": "Professional AI artwork"}
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                            character_name = None
                            village = "Hidden Leaf"
                            rarity = "Epic"
                            jutsu = "Unknown"
                            
                            for attr in metadata.get('attributes', []):
                                if attr['trait_type'] == 'Character':
                                    character_name = attr['value']
                                elif attr['trait_type'] == 'Village':
                                    village = attr['value'] 
                                elif attr['trait_type'] == 'Rarity':
                                    rarity = attr['value']
                                elif attr['trait_type'] == 'Signature Jutsu':
                                    jutsu = attr['value']
                                    
                            character_info = {
                                "name": character_name or "AI Naruto Character",
                                "village": village,
                                "rarity": rarity,
                                "jutsu": jutsu,
                                "description": metadata.get('description', 'Professional AI artwork')
                            }
                            
                            print(f"Enhanced #{image_file.replace('.png', '')}: {character_info['name']} ({character_info['rarity']})")
                    
                    # Convert image to base64
                    with open(image_path, 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode('utf-8')
                    
                    nft_id = image_file.replace('.png', '')
                    rarity_colors = {
                        "Legendary": "#FFD700", 
                        "Mythic": "#FF69B4", 
                        "Epic": "#9932CC", 
                        "Rare": "#4169E1", 
                        "Uncommon": "#32CD32"
                    }
                    rarity_color = rarity_colors.get(character_info["rarity"], "#808080")
                    
                    gallery_html += f'''
                    <div class="nft-card">
                        <div class="card-header">
                            <span class="nft-number">#{nft_id.zfill(3)}</span>
                            <span class="rarity-badge" style="background: {rarity_color};">{character_info["rarity"]}</span>
                        </div>
                        <div class="image-container">
                            <img src="data:image/png;base64,{img_data}" alt="{character_info['name']}">
                            <div class="ai-badge">🤖 AI Generated</div>
                        </div>
                        <div class="card-info">
                            <h3>{character_info['name']}</h3>
                            <p><strong>Village:</strong> {character_info['village']}</p>
                            <p><strong>Jutsu:</strong> {character_info['jutsu']}</p>
                            <p class="ai-label">Gemini AI Professional Art</p>
                            <p class="quality-label">High-Quality 3D Style</p>
                        </div>
                    </div>'''
                    
                except Exception as e:
                    print(f"Error loading {image_file}: {e}")
            
            collection_type = "AI-Generated Professional" if "gemini" in collection_folder else "Reference Quality"
            
            html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Gemini AI Naruto Collection</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0f23, #1a1a2e, #16213e, #0f3460);
            color: white;
            padding: 20px;
            min-height: 100vh;
        }}
        .header {{
            text-align: center;
            padding: 40px;
            margin-bottom: 40px;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .header h1 {{
            font-size: 3.5rem;
            background: linear-gradient(45deg, #ff6b35, #f7931e, #ffdd00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            font-weight: 800;
        }}
        .header p {{
            font-size: 1.3rem;
            color: #ccc;
            margin-bottom: 10px;
        }}
        .ai-badge-header {{
            display: inline-block;
            padding: 12px 25px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.1rem;
            margin-top: 15px;
            border: 2px solid #66BB6A;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            max-width: 1600px;
            margin: 0 auto;
        }}
        .nft-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 20px;
            overflow: hidden;
            transition: all 0.4s ease;
            border: 1px solid rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            position: relative;
        }}
        .nft-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 60px rgba(255,107,53,0.3);
            border-color: rgba(76, 175, 80, 0.6);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(0,0,0,0.4);
            backdrop-filter: blur(5px);
        }}
        .nft-number {{
            font-weight: bold;
            font-size: 1.1rem;
            color: #4CAF50;
        }}
        .rarity-badge {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            color: white;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }}
        .image-container {{
            padding: 0;
            background: #f8f9fa;
            position: relative;
            overflow: hidden;
        }}
        .ai-badge {{
            position: absolute;
            top: 10px;
            left: 10px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
            border: 2px solid #66BB6A;
            z-index: 2;
        }}
        .image-container::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent, rgba(76, 175, 80, 0.1), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 1;
        }}
        .nft-card:hover .image-container::before {{
            opacity: 1;
        }}
        .image-container img {{
            width: 100%;
            height: 350px;
            object-fit: cover;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transition: transform 0.3s ease;
        }}
        .nft-card:hover .image-container img {{
            transform: scale(1.05);
        }}
        .card-info {{
            padding: 25px;
            background: rgba(0,0,0,0.2);
        }}
        .card-info h3 {{
            color: #4CAF50;
            margin-bottom: 12px;
            font-size: 1.4rem;
            font-weight: 700;
        }}
        .card-info p {{
            color: #ccc;
            margin-bottom: 6px;
            font-size: 0.95rem;
        }}
        .ai-label {{
            color: #4CAF50 !important;
            font-weight: 600;
            font-style: italic;
        }}
        .quality-label {{
            color: #FFD700 !important;
            font-weight: 600;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            margin: 20px 0;
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #4CAF50;
        }}
        .stat-label {{
            font-size: 0.9rem;
            color: #ccc;
            margin-top: 5px;
        }}
        
        @media (max-width: 768px) {{
            .gallery {{
                grid-template-columns: 1fr;
                gap: 20px;
                padding: 0 10px;
            }}
            .header h1 {{
                font-size: 2.5rem;
            }}
            .nft-card {{
                margin: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Gemini AI Enhanced Gallery</h1>
        <p>Professional {collection_type} Naruto NFT Collection</p>
        <p>AI-enhanced with professional character descriptions and authentic lore</p>
        <div class="ai-badge-header">🤖 Powered by Gemini AI</div>
    </div>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-number">20</div>
            <div class="stat-label">AI Artworks</div>
        </div>
        <div class="stat">
            <div class="stat-number">10</div>
            <div class="stat-label">Characters</div>
        </div>
        <div class="stat">
            <div class="stat-number">🤖</div>
            <div class="stat-label">AI Generated</div>
        </div>
        <div class="stat">
            <div class="stat-number">✨</div>
            <div class="stat-label">Pro Quality</div>
        </div>
    </div>
    
    <div class="gallery">
        {gallery_html}
    </div>
</body>
</html>'''
            
            self.wfile.write(html.encode('utf-8'))
            print(f"Served AI-enhanced collection with {len(image_files)} NFTs")
            
        else:
            self.send_error(404)

if __name__ == "__main__":
    print("Gemini AI Enhanced Naruto NFT Collection")
    print("=" * 50)
    print(f"Starting enhanced gallery on port {PORT}")
    print("Enhanced with professional character descriptions and authentic lore")
    print("=" * 50)
    
    with socketserver.TCPServer(("0.0.0.0", PORT), GeminiEnhancedHandler) as httpd:
        print(f"AI-Enhanced Gallery running on port {PORT}")
        httpd.serve_forever()