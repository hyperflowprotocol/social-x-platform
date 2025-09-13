#!/usr/bin/env python3
"""
Simple SVG Art Viewer - Direct access to NFT artwork
"""
import http.server
import socketserver
import os
import urllib.parse

class SVGViewerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self.serve_art_browser()
        elif path.endswith('.svg'):
            self.serve_svg_direct(path)
        else:
            super().do_GET()
    
    def serve_art_browser(self):
        """Serve simple art browser"""
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>NFT Art Viewer</title>
    <style>
        body { font-family: Arial; background: #111; color: white; margin: 20px; }
        .art-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .art-card { background: #222; padding: 15px; border-radius: 10px; text-align: center; }
        .art-image { width: 100%; height: 200px; border: 1px solid #444; border-radius: 8px; }
        h1 { color: #FFD700; text-align: center; }
        .collection { margin-bottom: 40px; }
    </style>
</head>
<body>
    <h1>🎨 NFT Artwork Gallery</h1>
    
    <div class="collection">
        <h2>🍥 Naruto Collection</h2>
        <div class="art-grid" id="narutoArt"></div>
    </div>
    
    <div class="collection">
        <h2>⚡ HyperEVM Collection</h2>
        <div class="art-grid" id="hyperevmArt"></div>
    </div>
    
    <div class="collection">
        <h2>🔥 Advanced Naruto Collection</h2>
        <div class="art-grid" id="advancedArt"></div>
    </div>
    
    <script>
        // Load Naruto NFTs
        const narutoContainer = document.getElementById('narutoArt');
        for (let i = 1; i <= 20; i++) {
            narutoContainer.innerHTML += `
                <div class="art-card">
                    <iframe src="/naruto_collection_1755535292/images/${i}.svg" 
                            class="art-image" frameborder="0">
                    </iframe>
                    <h3>Shinobi #${i}</h3>
                    <a href="/naruto_collection_1755535292/images/${i}.svg" target="_blank" 
                       style="color: #FFD700;">View Full Size</a>
                </div>
            `;
        }
        
        // Load HyperEVM NFTs  
        const hyperevmContainer = document.getElementById('hyperevmArt');
        for (let i = 1; i <= 10; i++) {
            hyperevmContainer.innerHTML += `
                <div class="art-card">
                    <iframe src="/hyperevm_collection_1755535080/images/${i}.svg" 
                            class="art-image" frameborder="0">
                    </iframe>
                    <h3>HyperEVM #${i}</h3>
                    <a href="/hyperevm_collection_1755535080/images/${i}.svg" target="_blank" 
                       style="color: #FFD700;">View Full Size</a>
                </div>
            `;
        }
        
        // Load Advanced Naruto NFTs
        const advancedContainer = document.getElementById('advancedArt');
        for (let i = 1; i <= 30; i++) {
            advancedContainer.innerHTML += `
                <div class="art-card">
                    <iframe src="/advanced_naruto_collection_1755535921/images/${i}.svg" 
                            class="art-image" frameborder="0">
                    </iframe>
                    <h3>Elite Shinobi #${i}</h3>
                    <a href="/advanced_naruto_collection_1755535921/images/${i}.svg" target="_blank" 
                       style="color: #FFD700;">View Full Size</a>
                </div>
            `;
        }
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_svg_direct(self, path):
        """Serve SVG files directly"""
        try:
            file_path = path[1:]  # Remove leading slash
            if os.path.exists(file_path) and file_path.endswith('.svg'):
                with open(file_path, 'r') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_error(404, "SVG not found")
        except Exception as e:
            self.send_error(500, str(e))

def run_svg_viewer():
    port = 5003
    
    print(f"🎨 NFT Art Viewer starting on port {port}")
    print(f"📁 Serving SVG artwork directly")
    print(f"🖼️  Browse your generated NFT art")
    
    try:
        with socketserver.TCPServer(("", port), SVGViewerHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Art viewer stopped")
    except OSError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_svg_viewer()