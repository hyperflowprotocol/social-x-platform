#!/usr/bin/env python3
"""
Simple Art Display - Direct SVG viewing without iframes
"""
import http.server
import socketserver
import os
import urllib.parse

class SimpleArtHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self.show_art_gallery()
        elif path.startswith("/art/"):
            # Direct SVG display
            art_file = path[5:]  # Remove /art/ prefix
            self.display_svg_directly(art_file)
        elif path.endswith('.svg'):
            self.serve_svg_file(path[1:])
        else:
            super().do_GET()
    
    def show_art_gallery(self):
        """Show simple art gallery with direct SVG display"""
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>NFT Art Gallery</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: #111; 
            color: white; 
            margin: 0; 
            padding: 20px; 
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px; 
            background: linear-gradient(45deg, #FFD700, #FFA500);
            padding: 20px;
            border-radius: 15px;
            color: #000;
        }
        .title { font-size: 2.5em; margin: 0; }
        .subtitle { font-size: 1.2em; margin: 10px 0 0 0; }
        
        .comparison { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 30px; 
            margin: 30px 0; 
        }
        .section { 
            background: #222; 
            padding: 20px; 
            border-radius: 15px; 
            border: 2px solid #444;
        }
        .section h2 { 
            color: #FFD700; 
            text-align: center; 
            margin-top: 0; 
        }
        .art-grid { 
            display: grid; 
            grid-template-columns: repeat(2, 1fr); 
            gap: 15px; 
        }
        .art-item { 
            background: #333; 
            padding: 10px; 
            border-radius: 8px; 
            text-align: center;
            border: 1px solid #555;
        }
        .art-item:hover {
            border-color: #FFD700;
            transform: scale(1.02);
            transition: all 0.3s ease;
        }
        .art-link { 
            color: #87CEEB; 
            text-decoration: none; 
            font-weight: bold;
            display: block;
            padding: 15px;
            background: #444;
            border-radius: 5px;
            margin: 5px 0;
        }
        .art-link:hover { 
            background: #FFD700; 
            color: #000; 
        }
        .improvement { 
            background: linear-gradient(45deg, #32CD32, #228B22);
            padding: 15px; 
            border-radius: 10px; 
            text-align: center; 
            margin: 20px 0;
            color: white;
            font-size: 1.3em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">🎨 NFT Art Evolution</h1>
        <p class="subtitle">Professional Anime-Style Upgrade Complete</p>
    </div>

    <div class="improvement">
        ✅ ARTWORK UPGRADE: From Basic Shapes to Professional Anime Art
    </div>

    <div class="comparison">
        <div class="section">
            <h2>🔥 NEW: Advanced Collection</h2>
            <p style="text-align: center; color: #32CD32;">Professional anime-style artwork with detailed features</p>
            <div class="art-grid">''' + \
''.join([f'''
                <div class="art-item">
                    <a href="/art/advanced_naruto_collection_1755535921/images/{i}.svg" class="art-link">
                        Elite Shinobi #{i}
                    </a>
                </div>''' for i in range(1, 9)]) + '''
            </div>
        </div>
        
        <div class="section">
            <h2>📝 OLD: Basic Collection</h2>
            <p style="text-align: center; color: #FFA500;">Simple geometric shapes (for comparison)</p>
            <div class="art-grid">''' + \
''.join([f'''
                <div class="art-item">
                    <a href="/art/naruto_collection_1755535292/images/{i}.svg" class="art-link">
                        Basic Shinobi #{i}
                    </a>
                </div>''' for i in range(1, 9)]) + '''
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin: 30px 0; color: #87CEEB;">
        <p>Click any link above to view the full artwork directly</p>
    </div>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def display_svg_directly(self, file_path):
        """Display SVG with simple HTML wrapper"""
        try:
            if os.path.exists(file_path) and file_path.endswith('.svg'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                
                html = f'''<!DOCTYPE html>
<html>
<head>
    <title>NFT Artwork</title>
    <style>
        body {{ 
            margin: 0; 
            padding: 20px; 
            background: #000; 
            display: flex; 
            justify-content: center; 
            align-items: center;
            min-height: 100vh;
            flex-direction: column;
        }}
        .artwork {{ 
            max-width: 90vw; 
            max-height: 80vh; 
            border: 3px solid #FFD700;
            border-radius: 15px;
            background: #111;
            padding: 10px;
        }}
        .back-link {{
            color: #FFD700;
            text-decoration: none;
            font-size: 18px;
            margin-bottom: 20px;
            padding: 10px 20px;
            border: 2px solid #FFD700;
            border-radius: 8px;
            background: #222;
        }}
        .back-link:hover {{
            background: #FFD700;
            color: #000;
        }}
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Gallery</a>
    <div class="artwork">
        {svg_content}
    </div>
</body>
</html>'''
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            else:
                self.send_error(404, "Artwork not found")
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_svg_file(self, file_path):
        """Serve raw SVG files"""
        try:
            if os.path.exists(file_path) and file_path.endswith('.svg'):
                with open(file_path, 'r', encoding='utf-8') as f:
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

if __name__ == "__main__":
    port = 5005
    print(f"🎨 Simple Art Display starting on port {port}")
    print(f"🖼️ Direct SVG viewing without iframes")
    print(f"🔥 Compare basic vs advanced artwork")
    
    try:
        with socketserver.TCPServer(("", port), SimpleArtHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Art display stopped")
    except OSError as e:
        print(f"❌ Error: {e}")