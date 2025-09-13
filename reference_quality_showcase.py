#!/usr/bin/env python3
"""
Reference Quality Showcase - Displays professional anime artwork matching reference standards
"""

import os
import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

class ReferenceQualityHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url_parts = urlparse(self.path)
        path = url_parts.path
        
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reference Quality Naruto NFTs - Professional Anime Art</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        
        .header {
            text-align: center;
            padding: 3rem 2rem;
            background: rgba(0, 0, 0, 0.3);
            border-bottom: 3px solid #ff6b35;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
        }
        
        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 2rem;
            padding: 2rem;
            background: rgba(0, 0, 0, 0.2);
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
            padding: 1rem 2rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: #ff6b35;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-top: 0.5rem;
        }
        
        .gallery {
            padding: 3rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .nft-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .nft-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .nft-image {
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .nft-info {
            padding: 1.5rem;
        }
        
        .nft-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #ff6b35;
        }
        
        .nft-description {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 1rem;
            line-height: 1.5;
        }
        
        .traits-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
        }
        
        .trait {
            background: rgba(0, 0, 0, 0.3);
            padding: 0.5rem;
            border-radius: 6px;
            text-align: center;
        }
        
        .trait-label {
            font-size: 0.7rem;
            opacity: 0.7;
            display: block;
        }
        
        .trait-value {
            font-size: 0.8rem;
            font-weight: 600;
            color: #ff6b35;
        }
        
        .rarity-legendary { border-color: #ffd700; }
        .rarity-epic { border-color: #a855f7; }
        .rarity-rare { border-color: #3b82f6; }
        .rarity-uncommon { border-color: #10b981; }
        .rarity-common { border-color: #64748b; }
        
        .loading {
            text-align: center;
            padding: 3rem;
            font-size: 1.2rem;
            opacity: 0.7;
        }
        
        .quality-badge {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: linear-gradient(45deg, #ff6b35, #f7931e);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8rem;
            box-shadow: 0 2px 8px rgba(255, 107, 53, 0.3);
        }
        
        .card-container {
            position: relative;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .stats-bar { gap: 1rem; }
            .stat-item { padding: 0.8rem 1.2rem; }
            .gallery-grid { grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Reference Quality Naruto NFTs</h1>
        <p>Professional anime artwork matching reference image quality standards. 
           Advanced character features, detailed eye techniques, and authentic jutsu effects.</p>
    </div>
    
    <div class="stats-bar" id="statsBar">
        <div class="loading">Loading collection statistics...</div>
    </div>
    
    <div class="gallery">
        <div class="gallery-grid" id="galleryGrid">
            <div class="loading">Loading reference quality artwork...</div>
        </div>
    </div>

    <script>
        let collectionData = null;
        let nftData = [];
        
        async function loadCollection() {
            try {
                const response = await fetch('/api/collection/reference_quality');
                collectionData = await response.json();
                
                document.getElementById('statsBar').innerHTML = `
                    <div class="stat-item">
                        <span class="stat-number">${collectionData.total_supply}</span>
                        <span class="stat-label">Total Supply</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${collectionData.average_power?.toLocaleString() || 'N/A'}</span>
                        <span class="stat-label">Avg Power</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${collectionData.legendary_characters || 0}</span>
                        <span class="stat-label">Legendary</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${collectionData.special_techniques || 0}</span>
                        <span class="stat-label">Special Eyes</span>
                    </div>
                `;
                
                await loadNFTs();
            } catch (error) {
                console.error('Error loading collection:', error);
            }
        }
        
        async function loadNFTs() {
            try {
                const response = await fetch('/api/nfts/reference_quality');
                nftData = await response.json();
                
                renderNFTs(nftData);
            } catch (error) {
                console.error('Error loading NFTs:', error);
                document.getElementById('galleryGrid').innerHTML = 
                    '<div class="loading">Error loading NFTs. Please refresh the page.</div>';
            }
        }
        
        function renderNFTs(nfts) {
            const grid = document.getElementById('galleryGrid');
            
            if (!nfts || nfts.length === 0) {
                grid.innerHTML = '<div class="loading">No NFTs found in collection.</div>';
                return;
            }
            
            grid.innerHTML = nfts.map(nft => {
                const rarity = nft.attributes?.find(attr => attr.trait_type === 'Rarity')?.value?.toLowerCase() || 'common';
                const character = nft.attributes?.find(attr => attr.trait_type === 'Character')?.value || 'Unknown';
                const eyes = nft.attributes?.find(attr => attr.trait_type === 'Eye Technique')?.value || 'Normal';
                const jutsu = nft.attributes?.find(attr => attr.trait_type === 'Jutsu')?.value || 'None';
                const power = nft.attributes?.find(attr => attr.trait_type === 'Power Level')?.value || 0;
                
                return `
                    <div class="card-container">
                        <div class="nft-card rarity-${rarity}">
                            <img src="/image/reference_quality/${nft.id}.png" 
                                 alt="${nft.name}" 
                                 class="nft-image"
                                 onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjNjY3ZWVhIi8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTUwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5JbWFnZSBMb2FkaW5nLi4uPC90ZXh0Pgo8L3N2Zz4='">
                            <div class="nft-info">
                                <div class="nft-title">${nft.name}</div>
                                <div class="nft-description">${nft.description}</div>
                                <div class="traits-grid">
                                    <div class="trait">
                                        <span class="trait-label">Character</span>
                                        <span class="trait-value">${character}</span>
                                    </div>
                                    <div class="trait">
                                        <span class="trait-label">Eyes</span>
                                        <span class="trait-value">${eyes}</span>
                                    </div>
                                    <div class="trait">
                                        <span class="trait-label">Jutsu</span>
                                        <span class="trait-value">${jutsu}</span>
                                    </div>
                                    <div class="trait">
                                        <span class="trait-label">Power</span>
                                        <span class="trait-value">${power.toLocaleString()}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="quality-badge">Reference Quality</div>
                    </div>
                `;
            }).join('');
        }
        
        // Load collection on page load
        loadCollection();
    </script>
</body>
</html>
            """
            
            self.wfile.write(html.encode('utf-8'))
            
        elif path == '/api/collection/reference_quality':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Find the latest reference quality folder
            folders = [f for f in os.listdir('.') if f.startswith('reference_quality_')]
            if not folders:
                self.wfile.write(b'{"error": "No reference quality collection found"}')
                return
                
            latest_folder = max(folders)
            collection_file = f'{latest_folder}/collection.json'
            
            if os.path.exists(collection_file):
                with open(collection_file, 'r', encoding='utf-8') as f:
                    collection_data = json.load(f)
                self.wfile.write(json.dumps(collection_data).encode('utf-8'))
            else:
                self.wfile.write(b'{"error": "Collection metadata not found"}')
                
        elif path == '/api/nfts/reference_quality':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Find the latest reference quality folder
            folders = [f for f in os.listdir('.') if f.startswith('reference_quality_')]
            if not folders:
                self.wfile.write(b'[]')
                return
                
            latest_folder = max(folders)
            metadata_dir = f'{latest_folder}/metadata'
            
            nfts = []
            if os.path.exists(metadata_dir):
                for filename in sorted(os.listdir(metadata_dir), key=lambda x: int(x) if x.isdigit() else 0):
                    if filename.isdigit():
                        with open(f'{metadata_dir}/{filename}', 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            metadata['id'] = int(filename)
                            nfts.append(metadata)
            
            self.wfile.write(json.dumps(nfts).encode('utf-8'))
            
        elif path.startswith('/image/reference_quality/'):
            # Serve reference quality images
            filename = path.split('/')[-1]
            
            # Find the latest reference quality folder
            folders = [f for f in os.listdir('.') if f.startswith('reference_quality_')]
            if not folders:
                self.send_error(404, "Collection not found")
                return
                
            latest_folder = max(folders)
            image_path = f'{latest_folder}/images/{filename}'
            
            if os.path.exists(image_path):
                self.send_response(200)
                if filename.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    self.send_header('Content-type', 'image/jpeg')
                else:
                    self.send_header('Content-type', 'application/octet-stream')
                    
                self.end_headers()
                
                with open(image_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Image not found")
        else:
            self.send_error(404, "File not found")

def main():
    PORT = 5000
    print("🎨 Reference Quality Naruto NFT Showcase")
    print("=" * 60)
    print(f"🌟 Professional anime artwork matching reference standards")
    print(f"🚀 Server starting on port {PORT}")
    print(f"🔗 Visit: http://0.0.0.0:{PORT}")
    print("=" * 60)
    
    with socketserver.TCPServer(("0.0.0.0", PORT), ReferenceQualityHandler) as httpd:
        print(f"✅ Reference Quality Showcase running on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()