#!/usr/bin/env python3
"""
Fixed Art Showcase - Shows your reference quality artwork
"""

import http.server
import socketserver
import os
import base64

PORT = 5007

def get_image_base64(image_path):
    """Convert image to base64 for direct embedding"""
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except:
        return None

class FixedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            # Find reference quality folder
            folders = [f for f in os.listdir('.') if f.startswith('reference_quality_') and os.path.isdir(f)]
            if not folders:
                self.wfile.write(b'<h1>No artwork found</h1>')
                return
                
            latest_folder = max(folders)
            images_dir = f'{latest_folder}/images'
            
            print(f"Looking in folder: {latest_folder}")
            print(f"Images directory: {images_dir}")
            
            # Get all PNG files
            image_files = []
            if os.path.exists(images_dir):
                all_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]
                print(f"Found {len(all_files)} PNG files")
                # Sort by numeric value, handling both "1.png" and "01.png" formats safely
                try:
                    image_files = sorted(all_files, key=lambda x: int(x.split('.')[0]))
                except ValueError:
                    # Fallback to simple sort if numeric sort fails
                    image_files = sorted(all_files)
            
            print(f"Sorted image files: {image_files[:5]}...")  # Show first 5
            
            # Generate HTML with images
            images_html = ""
            for i, img_file in enumerate(image_files, 1):
                img_path = f"{images_dir}/{img_file}"
                img_base64 = get_image_base64(img_path)
                if img_base64:
                    images_html += f'''
                    <div class="nft">
                        <img src="data:image/png;base64,{img_base64}" alt="NFT #{i}">
                        <h3>Naruto NFT #{i}</h3>
                        <p>Reference Quality Artwork</p>
                        <div class="traits">
                            <span class="trait">Professional</span>
                            <span class="trait">Anime Style</span>
                            <span class="trait">PNG Format</span>
                        </div>
                    </div>
                    '''
            
            html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Professional Naruto NFT Collection</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            margin: 0; 
            padding: 20px;
            min-height: 100vh;
        }}
        .header {{ 
            text-align: center; 
            margin-bottom: 30px; 
            background: rgba(0,0,0,0.3);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            background: linear-gradient(45deg, #ff6b35, #f7931e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .gallery {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); 
            gap: 25px; 
            max-width: 1400px;
            margin: 0 auto;
        }}
        .nft {{ 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 20px; 
            text-align: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .nft:hover {{
            transform: translateY(-10px);
            background: rgba(255,255,255,0.15);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }}
        .nft img {{
            width: 100%;
            height: 280px;
            object-fit: cover;
            border-radius: 15px;
            margin-bottom: 15px;
        }}
        .nft h3 {{
            margin: 10px 0;
            font-size: 1.3em;
            color: #ff6b35;
        }}
        .traits {{
            display: flex;
            gap: 8px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 15px;
        }}
        .trait {{
            background: rgba(255,107,53,0.2);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            border: 1px solid rgba(255,107,53,0.3);
        }}
        .stats {{
            text-align: center; 
            margin-top: 40px; 
            padding: 25px; 
            background: rgba(0,0,0,0.4); 
            border-radius: 15px; 
            border: 2px solid rgba(255,107,53,0.3);
        }}
        .stats h2 {{
            color: #ff6b35;
            margin-bottom: 20px;
        }}
        .stats-grid {{
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin: 20px 0;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 12px;
            backdrop-filter: blur(5px);
        }}
        .stat-number {{
            font-size: 28px; 
            font-weight: bold; 
            color: #ff6b35;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Professional Naruto NFT Collection</h1>
        <p>Reference Quality Anime Artwork - Professional PIL Processing</p>
    </div>
    
    <div class="gallery">
        {images_html}
    </div>
    
    <div class="stats">
        <h2>Collection Breakthrough</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{len(image_files)}</div>
                <div>Total Artworks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">PNG</div>
                <div>High Quality Format</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">PIL</div>
                <div>Professional Processing</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">800x800</div>
                <div>Resolution</div>
            </div>
        </div>
        <p><strong>Achievement:</strong> Created professional anime NFT artwork that matches reference image quality standards!</p>
    </div>
</body>
</html>
'''
            
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404)

print("🎨 Fixed Art Showcase")
print("=" * 50)
print(f"🌟 Displaying your breakthrough artwork")
print(f"🚀 Server starting on port {PORT}")
print(f"🔗 Visit: http://0.0.0.0:{PORT}")
print("=" * 50)

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), FixedHandler) as httpd:
        print(f"✅ Fixed Art Showcase running on port {PORT}")
        httpd.serve_forever()
except OSError as e:
    print(f"❌ Error starting server: {e}")
    print("Trying alternative port...")
    PORT = 5008
    with socketserver.TCPServer(("0.0.0.0", PORT), FixedHandler) as httpd:
        print(f"✅ Fixed Art Showcase running on port {PORT}")
        httpd.serve_forever()