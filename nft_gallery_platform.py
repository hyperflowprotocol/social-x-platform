#!/usr/bin/env python3
"""
NFT Gallery Platform - Anime-Inspired Generative Art Collections
Specializing in professional Naruto character NFTs with advanced generative techniques
"""

import http.server
import socketserver
import json
import os
import random
from datetime import datetime
from advanced_naruto_art import AdvancedNarutoArtGenerator

PORT = 5000

class NFTGalleryHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.serve_gallery_homepage()
        elif self.path == "/api/collections":
            self.serve_collections_api()
        elif self.path == "/api/generate-nft":
            self.serve_generate_nft()
        elif self.path.startswith("/api/nft/"):
            nft_id = self.path.split("/")[-1]
            self.serve_nft_details(nft_id)
        else:
            super().do_GET()
    
    def serve_gallery_homepage(self):
        """Serve the main NFT gallery homepage"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Get recent collections
        collections = self.get_available_collections()
        recent_nfts = self.get_recent_nfts()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Anime NFT Gallery - Professional Naruto Collections</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #0f0f23, #1a1a2e, #16213e);
                    color: white;
                    min-height: 100vh;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                header {{
                    text-align: center;
                    padding: 40px 0;
                    border-bottom: 2px solid rgba(255, 215, 0, 0.3);
                    margin-bottom: 40px;
                }}
                
                h1 {{
                    font-size: 3rem;
                    background: linear-gradient(45deg, #FFD700, #FF6B35, #F7931E);
                    background-clip: text;
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 10px;
                }}
                
                .subtitle {{
                    font-size: 1.2rem;
                    color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 30px;
                }}
                
                .stats-bar {{
                    display: flex;
                    justify-content: center;
                    gap: 30px;
                    margin-top: 20px;
                }}
                
                .stat {{
                    text-align: center;
                    padding: 15px 25px;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 10px;
                    border: 1px solid rgba(255, 215, 0, 0.2);
                }}
                
                .stat-value {{
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #FFD700;
                }}
                
                .stat-label {{
                    font-size: 0.9rem;
                    color: rgba(255, 255, 255, 0.7);
                }}
                
                .section {{
                    margin: 50px 0;
                }}
                
                .section-title {{
                    font-size: 2rem;
                    margin-bottom: 30px;
                    color: #FFD700;
                    border-left: 4px solid #FFD700;
                    padding-left: 15px;
                }}
                
                .collections-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 25px;
                    margin-bottom: 40px;
                }}
                
                .collection-card {{
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 15px;
                    padding: 25px;
                    border: 1px solid rgba(255, 215, 0, 0.2);
                    transition: all 0.3s ease;
                    cursor: pointer;
                }}
                
                .collection-card:hover {{
                    transform: translateY(-5px);
                    border-color: #FFD700;
                    box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
                }}
                
                .collection-title {{
                    font-size: 1.3rem;
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: #FFD700;
                }}
                
                .collection-desc {{
                    color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 15px;
                    line-height: 1.5;
                }}
                
                .collection-stats {{
                    display: flex;
                    justify-content: space-between;
                    font-size: 0.9rem;
                }}
                
                .nft-preview-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                }}
                
                .nft-card {{
                    background: rgba(255, 255, 255, 0.03);
                    border-radius: 12px;
                    padding: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    transition: all 0.3s ease;
                }}
                
                .nft-card:hover {{
                    border-color: #FFD700;
                    transform: scale(1.02);
                }}
                
                .nft-image {{
                    width: 100%;
                    height: 200px;
                    background: linear-gradient(45deg, #FF6B35, #F7931E);
                    border-radius: 8px;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 3rem;
                    color: white;
                }}
                
                .nft-title {{
                    font-weight: bold;
                    margin-bottom: 8px;
                    color: #FFD700;
                }}
                
                .nft-traits {{
                    font-size: 0.9rem;
                    color: rgba(255, 255, 255, 0.7);
                    margin-bottom: 10px;
                }}
                
                .generate-btn {{
                    background: linear-gradient(45deg, #FFD700, #FF6B35);
                    color: black;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 25px;
                    font-size: 1.1rem;
                    font-weight: bold;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    margin: 20px auto;
                    display: block;
                }}
                
                .generate-btn:hover {{
                    transform: scale(1.05);
                    box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
                }}
                
                @media (max-width: 768px) {{
                    .stats-bar {{
                        flex-direction: column;
                        gap: 15px;
                    }}
                    
                    h1 {{
                        font-size: 2rem;
                    }}
                    
                    .collections-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>🎨 Anime NFT Gallery</h1>
                    <p class="subtitle">Professional Naruto Character NFTs with Advanced Generative Art</p>
                    
                    <div class="stats-bar">
                        <div class="stat">
                            <div class="stat-value">{len(collections)}</div>
                            <div class="stat-label">Collections</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{len(recent_nfts)}</div>
                            <div class="stat-label">Generated NFTs</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">9+</div>
                            <div class="stat-label">Art Styles</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">100+</div>
                            <div class="stat-label">Unique Traits</div>
                        </div>
                    </div>
                </header>
                
                <section class="section">
                    <h2 class="section-title">🏮 Featured Collections</h2>
                    <div class="collections-grid">
                        {self.render_collections(collections)}
                    </div>
                </section>
                
                <section class="section">
                    <h2 class="section-title">⚡ Recently Generated</h2>
                    <button class="generate-btn" onclick="generateNewNFT()">Generate New Naruto NFT</button>
                    <div class="nft-preview-grid">
                        {self.render_recent_nfts(recent_nfts)}
                    </div>
                </section>
            </div>
            
            <script>
                async function generateNewNFT() {{
                    try {{
                        const response = await fetch('/api/generate-nft');
                        const nft = await response.json();
                        
                        if (nft.success) {{
                            alert(`🎉 Generated: ${{nft.name}}\\n\\nTraits: ${{nft.traits.Village}} | ${{nft.traits.Character_Type}}\\nRarity Score: ${{nft.rarity_score}}`);
                            location.reload(); // Refresh to show new NFT
                        }}
                    }} catch (error) {{
                        console.error('Generation failed:', error);
                        alert('❌ NFT generation failed. Please try again.');
                    }}
                }}
                
                function viewCollection(collectionName) {{
                    alert(`📁 Viewing collection: ${{collectionName}}\\n\\nThis would open the collection viewer with all NFTs from this collection.`);
                }}
                
                // Auto-refresh recent NFTs every 30 seconds
                setInterval(() => {{
                    fetch('/api/collections')
                        .then(response => response.json())
                        .then(data => {{
                            console.log('Collections updated:', data.collections.length);
                        }});
                }}, 30000);
            </script>
        </body>
        </html>
        """
        
        self.wfile.write(html_content.encode('utf-8'))
    
    def render_collections(self, collections):
        """Render collection cards HTML"""
        html = ""
        for collection in collections:
            html += f"""
            <div class="collection-card" onclick="viewCollection('{collection['name']}')">
                <div class="collection-title">{collection['name']}</div>
                <div class="collection-desc">{collection['description']}</div>
                <div class="collection-stats">
                    <span>📦 {collection['nft_count']} NFTs</span>
                    <span>⭐ {collection['avg_rarity']:.1f} Avg Rarity</span>
                </div>
            </div>
            """
        return html
    
    def render_recent_nfts(self, nfts):
        """Render recent NFT cards HTML"""
        html = ""
        for nft in nfts[:6]:  # Show only 6 most recent
            emoji = self.get_character_emoji(nft['traits'].get('Character_Type', 'Custom Shinobi'))
            html += f"""
            <div class="nft-card">
                <div class="nft-image">{emoji}</div>
                <div class="nft-title">{nft['name']}</div>
                <div class="nft-traits">
                    🏮 {nft['traits'].get('Village', 'Unknown')}<br>
                    👤 {nft['traits'].get('Character_Type', 'Unknown')}<br>
                    ⚡ {nft['traits'].get('Jutsu_Manifestation', 'None')}
                </div>
                <div style="color: #FFD700; font-weight: bold;">
                    Rarity: {nft['rarity_score']:.1f}/100
                </div>
            </div>
            """
        return html
    
    def get_character_emoji(self, character_type):
        """Get emoji for character type"""
        emoji_map = {
            'Naruto Style': '🦊',
            'Sasuke Style': '⚡',
            'Sakura Style': '🌸',
            'Kakashi Style': '📖',
            'Gaara Style': '🏜️',
            'Itachi Style': '🦅',
            'Hinata Style': '👁️',
            'Neji Style': '🎯',
            'Rock Lee Style': '💪',
            'Custom Shinobi': '🥷'
        }
        return emoji_map.get(character_type, '🥷')
    
    def serve_collections_api(self):
        """API endpoint for collections data"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        collections = self.get_available_collections()
        recent_nfts = self.get_recent_nfts()
        
        result = {
            'success': True,
            'collections': collections,
            'recent_nfts': recent_nfts,
            'total_nfts': len(recent_nfts)
        }
        
        self.wfile.write(json.dumps(result).encode('utf-8'))
    
    def serve_generate_nft(self):
        """Generate a new NFT and return metadata"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Create new NFT using the advanced generator
            generator = AdvancedNarutoArtGenerator()
            nft_data = generator.generate_nft()
            
            # Add timestamp and ID
            nft_data['id'] = f"naruto_{int(datetime.now().timestamp())}"
            nft_data['timestamp'] = datetime.now().isoformat()
            nft_data['collection'] = 'Advanced Naruto Collection'
            
            # Save to recent NFTs
            self.save_recent_nft(nft_data)
            
            result = {
                'success': True,
                'nft': nft_data,
                'message': f"Generated {nft_data['name']} with rarity {nft_data['rarity_score']:.1f}"
            }
            
        except Exception as e:
            result = {
                'success': False,
                'error': str(e),
                'message': 'NFT generation failed'
            }
        
        self.wfile.write(json.dumps(result, default=str).encode('utf-8'))
    
    def serve_nft_details(self, nft_id):
        """Serve detailed NFT information"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Load NFT details from storage
        nft_data = self.load_nft_by_id(nft_id)
        
        if nft_data:
            result = {'success': True, 'nft': nft_data}
        else:
            result = {'success': False, 'error': 'NFT not found'}
        
        self.wfile.write(json.dumps(result, default=str).encode('utf-8'))
    
    def get_available_collections(self):
        """Get list of available collections"""
        collections = [
            {
                'name': 'Advanced Naruto Collection',
                'description': 'High-quality Naruto character NFTs with detailed traits and advanced generative art',
                'nft_count': 42,
                'avg_rarity': 45.2,
                'created': '2025-08-20'
            },
            {
                'name': 'Professional Naruto Series',
                'description': 'Professional-grade anime artwork featuring iconic Naruto characters and abilities',
                'nft_count': 38,
                'avg_rarity': 52.1,
                'created': '2025-08-18'
            },
            {
                'name': 'Anime Pixel Art Collection',
                'description': 'Retro pixel-style interpretations of beloved Naruto characters',
                'nft_count': 25,
                'avg_rarity': 41.8,
                'created': '2025-08-17'
            }
        ]
        
        # Add collection folders if they exist
        for folder in os.listdir('.'):
            if 'collection_' in folder and os.path.isdir(folder):
                try:
                    collection_path = os.path.join(folder, 'collection.json')
                    if os.path.exists(collection_path):
                        with open(collection_path, 'r') as f:
                            collection_data = json.load(f)
                            collections.append(collection_data)
                except:
                    pass
        
        return collections
    
    def get_recent_nfts(self):
        """Get recently generated NFTs"""
        recent_nfts = []
        
        # Load from recent NFTs file if it exists
        try:
            if os.path.exists('recent_nfts.json'):
                with open('recent_nfts.json', 'r') as f:
                    recent_nfts = json.load(f)
        except:
            pass
        
        # Generate some sample NFTs if none exist
        if not recent_nfts:
            generator = AdvancedNarutoArtGenerator()
            for i in range(6):
                nft_data = generator.generate_nft()
                nft_data['id'] = f"sample_{i+1}"
                nft_data['timestamp'] = datetime.now().isoformat()
                recent_nfts.append(nft_data)
            
            # Save samples
            self.save_recent_nfts(recent_nfts)
        
        # Sort by timestamp (newest first)
        recent_nfts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return recent_nfts
    
    def save_recent_nft(self, nft_data):
        """Save a newly generated NFT to recent list"""
        recent_nfts = self.get_recent_nfts()
        recent_nfts.insert(0, nft_data)  # Add to beginning
        
        # Keep only the 20 most recent
        recent_nfts = recent_nfts[:20]
        
        self.save_recent_nfts(recent_nfts)
    
    def save_recent_nfts(self, nfts):
        """Save recent NFTs to file"""
        try:
            with open('recent_nfts.json', 'w') as f:
                json.dump(nfts, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving recent NFTs: {e}")
    
    def load_nft_by_id(self, nft_id):
        """Load NFT data by ID"""
        recent_nfts = self.get_recent_nfts()
        for nft in recent_nfts:
            if nft.get('id') == nft_id:
                return nft
        return None

def start_nft_gallery():
    """Start the NFT Gallery Platform server"""
    print("🎨 Starting Anime NFT Gallery Platform...")
    print("=" * 60)
    print("🏮 Features:")
    print("  - Professional Naruto Character NFTs")
    print("  - Advanced Generative Art Collections")
    print("  - Real-time NFT Generation")
    print("  - Responsive Gallery Interface")
    print("  - Metadata-driven Display System")
    print("=" * 60)
    print(f"🚀 NFT Gallery Platform: http://localhost:{PORT}")
    print("🎯 Professional anime art collection ready...")
    
    with socketserver.TCPServer(("", PORT), NFTGalleryHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    start_nft_gallery()