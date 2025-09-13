#!/usr/bin/env python3
"""
NFT Gallery - Web interface to view generated NFT collections
Displays artwork, metadata, and collection statistics
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from pathlib import Path
import mimetypes

class NFTGalleryHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self.serve_gallery_home()
        elif path == "/api/collections":
            self.serve_collections_api()
        elif path.startswith("/api/collection/"):
            collection_name = path.split("/")[-1]
            self.serve_collection_api(collection_name)
        elif path.startswith("/images/"):
            self.serve_image(path)
        elif path.startswith("/metadata/"):
            self.serve_metadata(path)
        else:
            self.send_error(404, "Not found")
    
    def serve_gallery_home(self):
        """Serve main gallery page"""
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NFT Gallery - View Your Collections</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
        }
        
        .header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #FFD700, #FF69B4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .collections-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        
        .collection-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .collection-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .collection-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .collection-icon {
            font-size: 2.5rem;
            margin-right: 15px;
        }
        
        .collection-title {
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .collection-subtitle {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-top: 5px;
        }
        
        .collection-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-item {
            text-align: center;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }
        
        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: #FFD700;
        }
        
        .stat-label {
            font-size: 0.8rem;
            opacity: 0.8;
            margin-top: 5px;
        }
        
        .view-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .view-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .nft-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .nft-card {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .nft-card:hover {
            transform: scale(1.05);
        }
        
        .nft-image {
            width: 100%;
            height: 200px;
            border-radius: 8px;
            margin-bottom: 15px;
            background: rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .nft-title {
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .nft-traits {
            font-size: 0.8rem;
            opacity: 0.8;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 1.2rem;
        }
        
        .hidden { display: none; }
        
        @media (max-width: 768px) {
            .collections-grid {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 NFT Gallery</h1>
        <p>View your generated NFT collections and artwork</p>
    </div>
    
    <div class="container">
        <div id="collectionsView">
            <h2>Your Collections</h2>
            <div id="collectionsGrid" class="collections-grid">
                <div class="loading">Loading collections...</div>
            </div>
        </div>
        
        <div id="collectionView" class="hidden">
            <button onclick="showCollections()" style="margin-bottom: 20px; padding: 10px 20px; background: #333; color: white; border: none; border-radius: 5px; cursor: pointer;">← Back to Collections</button>
            <div id="collectionHeader"></div>
            <div id="nftGrid" class="nft-grid"></div>
        </div>
    </div>
    
    <script>
        let collections = [];
        
        async function loadCollections() {
            try {
                const response = await fetch('/api/collections');
                collections = await response.json();
                displayCollections();
            } catch (error) {
                document.getElementById('collectionsGrid').innerHTML = '<div class="loading">No collections found. Generate some NFTs first!</div>';
            }
        }
        
        function displayCollections() {
            const grid = document.getElementById('collectionsGrid');
            
            if (collections.length === 0) {
                grid.innerHTML = '<div class="loading">No collections found. Generate some NFTs first!</div>';
                return;
            }
            
            let html = '';
            collections.forEach(collection => {
                const icon = collection.name.includes('Naruto') ? '🍥' : 
                           collection.name.includes('Hyper') ? '⚡' : '🎨';
                
                html += `
                    <div class="collection-card">
                        <div class="collection-header">
                            <div class="collection-icon">${icon}</div>
                            <div>
                                <div class="collection-title">${collection.name}</div>
                                <div class="collection-subtitle">${collection.description || 'NFT Collection'}</div>
                            </div>
                        </div>
                        <div class="collection-stats">
                            <div class="stat-item">
                                <div class="stat-number">${collection.total_supply}</div>
                                <div class="stat-label">Total NFTs</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number">${collection.blockchain || 'HyperEVM'}</div>
                                <div class="stat-label">Blockchain</div>
                            </div>
                        </div>
                        <button class="view-btn" onclick="viewCollection('${collection.folder}', '${collection.name}')">
                            View Collection
                        </button>
                    </div>
                `;
            });
            
            grid.innerHTML = html;
        }
        
        async function viewCollection(folder, name) {
            document.getElementById('collectionsView').classList.add('hidden');
            document.getElementById('collectionView').classList.remove('hidden');
            
            document.getElementById('collectionHeader').innerHTML = `
                <h2>${name}</h2>
                <p>Loading NFTs...</p>
            `;
            
            try {
                const response = await fetch(`/api/collection/${folder}`);
                const data = await response.json();
                displayNFTs(data.nfts, folder);
                
                document.getElementById('collectionHeader').innerHTML = `
                    <h2>${name}</h2>
                    <p>${data.nfts.length} unique NFTs with detailed traits</p>
                `;
            } catch (error) {
                document.getElementById('nftGrid').innerHTML = '<div class="loading">Error loading collection</div>';
            }
        }
        
        function displayNFTs(nfts, folder) {
            const grid = document.getElementById('nftGrid');
            
            let html = '';
            nfts.forEach(nft => {
                const mainTraits = nft.attributes.slice(0, 3).map(attr => 
                    `${attr.trait_type}: ${attr.value}`
                ).join('<br>');
                
                const powerLevel = nft.attributes.find(attr => attr.trait_type === 'Power Level')?.value || 'N/A';
                const village = nft.attributes.find(attr => attr.trait_type === 'Village')?.value || 'Unknown';
                
                html += `
                    <div class="nft-card">
                        <div class="nft-image">
                            <object data="/images/${folder}/images/${nft.id}.svg" 
                                    type="image/svg+xml" 
                                    width="180" height="180" 
                                    style="border-radius: 8px; background: #222;">
                                <div style="width: 180px; height: 180px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; text-align: center; padding: 10px;">
                                    <div>
                                        <div style="font-size: 16px; font-weight: bold;">${nft.name}</div>
                                        <div style="font-size: 12px; margin-top: 5px;">${village}</div>
                                        <div style="font-size: 10px; margin-top: 3px;">⚡ ${powerLevel}</div>
                                    </div>
                                </div>
                            </object>
                        </div>
                        <div class="nft-title">${nft.name}</div>
                        <div class="nft-traits">${mainTraits}</div>
                        <div style="margin-top: 8px; font-size: 0.75rem; color: #FFD700;">
                            Power: ${powerLevel}
                        </div>
                        <button onclick="viewNFTArt('${folder}', ${nft.id})" style="margin-top: 10px; padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 0.8rem;">
                            View Full Art
                        </button>
                    </div>
                `;
            });
            
            grid.innerHTML = html;
        }
        
        function viewNFTArt(folder, id) {
            // Open SVG in new window for full view
            window.open(`/images/${folder}/images/${id}.svg`, '_blank');
        }
        
        function viewNFTDetails(folder, id) {
            window.open(`/metadata/${folder}/metadata/${id}`, '_blank');
        }
        
        function showCollections() {
            document.getElementById('collectionsView').classList.remove('hidden');
            document.getElementById('collectionView').classList.add('hidden');
        }
        
        // Load collections on page load
        window.addEventListener('DOMContentLoaded', loadCollections);
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_collections_api(self):
        """API endpoint to list all collections"""
        collections = []
        
        # Find collection folders
        for item in os.listdir('.'):
            if os.path.isdir(item) and ('collection' in item.lower() or 'naruto' in item.lower()):
                collection_info = self.get_collection_info(item)
                if collection_info:
                    collection_info['folder'] = item
                    collections.append(collection_info)
        
        self.send_json_response(collections)
    
    def serve_collection_api(self, folder):
        """API endpoint for specific collection"""
        try:
            # Load collection metadata
            collection_path = Path(folder)
            if not collection_path.exists():
                self.send_error(404, "Collection not found")
                return
            
            nfts = []
            metadata_dir = collection_path / 'metadata'
            
            if metadata_dir.exists():
                for metadata_file in sorted(metadata_dir.iterdir(), key=lambda x: int(x.name) if x.name.isdigit() else 0):
                    if metadata_file.is_file():
                        try:
                            with open(metadata_file, 'r') as f:
                                metadata = json.load(f)
                                metadata['id'] = metadata_file.name
                                nfts.append(metadata)
                        except:
                            continue
            
            response = {
                'collection': self.get_collection_info(folder),
                'nfts': nfts
            }
            
            self.send_json_response(response)
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_image(self, path):
        """Serve SVG images"""
        try:
            # Handle /images/collection_folder/images/file.svg
            file_path = path[1:]  # Remove leading slash
            
            # If path starts with 'images/', treat it as direct file access
            if file_path.startswith('images/'):
                file_path = file_path[7:]  # Remove 'images/' prefix
                
            if os.path.exists(file_path) and (file_path.endswith('.svg') or file_path.endswith('.png') or file_path.endswith('.jpg')):
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                if file_path.endswith('.svg'):
                    self.send_header('Content-type', 'image/svg+xml')
                elif file_path.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                else:
                    self.send_header('Content-type', 'image/jpeg')
                    
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, f"Image not found: {file_path}")
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_metadata(self, path):
        """Serve metadata files"""
        try:
            file_path = path[1:]  # Remove leading slash
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_error(404, "Metadata not found")
        except Exception as e:
            self.send_error(500, str(e))
    
    def get_collection_info(self, folder):
        """Get collection information from folder"""
        try:
            collection_file = Path(folder) / 'collection.json'
            if collection_file.exists():
                with open(collection_file, 'r') as f:
                    return json.load(f)
            else:
                # Fallback info
                metadata_dir = Path(folder) / 'metadata'
                total_supply = len(list(metadata_dir.glob('*'))) if metadata_dir.exists() else 0
                
                return {
                    'name': folder.replace('_', ' ').title(),
                    'description': 'NFT Collection',
                    'total_supply': total_supply,
                    'blockchain': 'HyperEVM'
                }
        except:
            return None
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

def run_gallery():
    """Start the NFT gallery server"""
    port = 5001
    handler = NFTGalleryHandler
    
    print(f"🎨 Starting NFT Gallery...")
    print(f"✅ Server running at http://localhost:{port}")
    print(f"🌐 External access: Available through Replit")
    print(f"📁 Serving collections from current directory")
    print(f"🖼️  View your generated NFT artwork and metadata")
    print(f"Ready to display your NFT collections! 🚀")
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Gallery server stopped")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Port {port} is already in use. Try stopping other servers first.")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    run_gallery()