#!/usr/bin/env python3
"""
Real Digital Art Viewer - Display actual PIL-generated artwork
Shows the difference between SVG and real image processing
"""
import http.server
import socketserver
import os
import urllib.parse
import base64
from io import BytesIO
from PIL import Image

class RealArtHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self.show_real_art_gallery()
        elif path.startswith("/view/"):
            image_path = path[6:]  # Remove /view/ prefix
            self.display_real_image(image_path)
        elif path.endswith('.png'):
            self.serve_png_file(path[1:])
        else:
            super().do_GET()
    
    def show_real_art_gallery(self):
        """Show real digital art gallery"""
        
        # Find real digital art folder
        real_art_folder = None
        for folder in os.listdir('.'):
            if folder.startswith('real_digital_art_'):
                real_art_folder = folder
                break
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Real Digital Art Gallery - PIL Generated!</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 100%); 
            color: white; 
            margin: 0; 
            padding: 20px;
            min-height: 100vh;
        }}
        .header {{ 
            text-align: center; 
            margin-bottom: 40px; 
            padding: 30px;
            background: linear-gradient(45deg, #32CD32 0%, #00FF00 50%, #90EE90 100%);
            border-radius: 20px;
            color: #000;
            box-shadow: 0 10px 30px rgba(50,205,50,0.4);
        }}
        .title {{ font-size: 3.8em; margin: 0; font-weight: bold; }}
        .subtitle {{ font-size: 1.6em; margin: 15px 0 0 0; }}
        
        .breakthrough-banner {{
            background: linear-gradient(90deg, #FF4500 0%, #FF6347 50%, #FF8C00 100%);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
            color: #000;
            font-size: 1.9em;
            font-weight: bold;
            box-shadow: 0 8px 25px rgba(255,69,0,0.4);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.02); }}
            100% {{ transform: scale(1); }}
        }}
        
        .tech-comparison {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 40px 0;
        }}
        .tech-card {{
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(15px);
            border: 3px solid;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        }}
        .svg-card {{ 
            border-color: #FF6B6B; 
            background: linear-gradient(135deg, rgba(255,107,107,0.1), rgba(255,107,107,0.05));
        }}
        .real-card {{ 
            border-color: #32CD32; 
            background: linear-gradient(135deg, rgba(50,205,50,0.1), rgba(50,205,50,0.05));
        }}
        
        .tech-title {{ 
            font-size: 2.4em;
            text-align: center; 
            margin: 0 0 20px 0;
            padding: 15px;
            border-radius: 12px;
            font-weight: bold;
        }}
        .svg-title {{ background: linear-gradient(45deg, #FF6B6B, #FF8E53); color: #000; }}
        .real-title {{ background: linear-gradient(45deg, #32CD32, #90EE90); color: #000; }}
        
        .tech-features {{
            list-style: none;
            padding: 0;
        }}
        .tech-features li {{
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-size: 1.1em;
        }}
        .svg-feature {{ color: #FF6B6B; }}
        .real-feature {{ color: #32CD32; }}
        
        .art-showcase {{ 
            display: grid; 
            grid-template-columns: repeat(6, 1fr); 
            gap: 20px; 
            margin: 30px 0;
        }}
        .art-preview {{ 
            aspect-ratio: 1;
            background: rgba(0,0,0,0.8); 
            border-radius: 15px; 
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid transparent;
            transition: all 0.3s ease;
            cursor: pointer;
            overflow: hidden;
        }}
        .art-preview:hover {{
            transform: translateY(-8px) scale(1.05);
            box-shadow: 0 20px 40px rgba(50,205,50,0.4);
            border-color: #32CD32;
        }}
        
        .art-preview img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 12px;
        }}
        
        .art-link {{ 
            color: #32CD32; 
            text-decoration: none; 
            font-weight: bold;
            font-size: 1em;
            text-align: center;
            padding: 10px;
        }}
        
        .quality-badge {{
            background: linear-gradient(45deg, #32CD32, #00FF00);
            color: #000;
            padding: 12px 24px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.2em;
            display: inline-block;
            margin: 20px 10px;
            box-shadow: 0 5px 15px rgba(50,205,50,0.3);
        }}
        
        @media (max-width: 1200px) {{
            .tech-comparison {{ grid-template-columns: 1fr; }}
            .art-showcase {{ grid-template-columns: repeat(4, 1fr); }}
        }}
        @media (max-width: 768px) {{
            .art-showcase {{ grid-template-columns: repeat(3, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">🎨 REAL DIGITAL ART</h1>
        <p class="subtitle">PIL/Pillow Generated - Like Professional Art Tools!</p>
    </div>

    <div class="breakthrough-banner">
        🚀 BREAKTHROUGH! Using Real Image Processing Instead of SVG
    </div>

    <div class="tech-comparison">
        <div class="tech-card svg-card">
            <h2 class="tech-title svg-title">❌ SVG Limitations</h2>
            <ul class="tech-features">
                <li class="svg-feature">• Vector shapes only</li>
                <li class="svg-feature">• Limited realistic effects</li>
                <li class="svg-feature">• No pixel-level control</li>
                <li class="svg-feature">• Basic gradients</li>
                <li class="svg-feature">• Cannot create detailed textures</li>
                <li class="svg-feature">• Mathematical drawings</li>
            </ul>
        </div>
        
        <div class="tech-card real-card">
            <h2 class="tech-title real-title">✅ PIL/Pillow Power</h2>
            <ul class="tech-features">
                <li class="real-feature">• Pixel-perfect artwork</li>
                <li class="real-feature">• Advanced image filters</li>
                <li class="real-feature">• Professional gradients</li>
                <li class="real-feature">• Color enhancement</li>
                <li class="real-feature">• Blur and sharpening</li>
                <li class="real-feature">• Real digital art tools</li>
            </ul>
        </div>
    </div>
    
    <div style="text-align: center; margin: 40px 0;">
        <div class="quality-badge">🎯 Reference-Quality Artwork</div>
        <div class="quality-badge">🖼️ PNG Format Images</div>
        <div class="quality-badge">✨ Professional Effects</div>
    </div>'''
        
        if real_art_folder and os.path.exists(real_art_folder):
            html += f'''
    <div style="text-align: center; margin: 40px 0;">
        <h2 style="color: #32CD32; font-size: 2.5em; margin: 0;">Real Digital Art Gallery</h2>
        <p style="color: #90EE90; font-size: 1.3em; margin: 15px 0;">Click any artwork to view in full resolution</p>
    </div>
    
    <div class="art-showcase">''' + ''.join([f'''
        <div class="art-preview">
            <a href="/view/{real_art_folder}/images/{i}.png" class="art-link">
                <img src="/{real_art_folder}/images/{i}.png" alt="Real Art #{i}" loading="lazy">
            </a>
        </div>''' for i in range(1, 19) if os.path.exists(f'{real_art_folder}/images/{i}.png')]) + '''
    </div>'''
        else:
            html += '''
    <div style="text-align: center; padding: 60px; background: rgba(255,69,0,0.1); border-radius: 20px;">
        <h3 style="color: #FF6347; font-size: 2.2em; margin: 0 0 20px 0;">⚡ Generating Real Digital Art...</h3>
        <p style="color: #ddd; font-size: 1.2em; margin: 0;">Using PIL/Pillow to create pixel-perfect artwork similar to your reference</p>
    </div>'''
        
        html += '''
    <div style="text-align: center; margin: 50px 0; padding: 40px; background: rgba(50,205,50,0.1); border-radius: 20px;">
        <h3 style="color: #32CD32; margin: 0 0 20px 0; font-size: 2.2em;">🎯 Professional Quality Achieved!</h3>
        <p style="color: #90EE90; margin: 0; font-size: 1.3em; line-height: 1.5;">
            This collection uses REAL image processing with PIL/Pillow to create pixel-perfect digital art<br>
            Similar to professional drawing tools like Adobe Photoshop or Procreate
        </p>
    </div>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def display_real_image(self, image_path):
        """Display real image in fullscreen view"""
        try:
            if os.path.exists(image_path) and image_path.endswith('.png'):
                # Convert PNG to base64 for embedding
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                
                # Get image info
                img = Image.open(BytesIO(img_data))
                width, height = img.size
                
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                
                html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Real Digital Art - {image_path}</title>
    <style>
        body {{ 
            margin: 0; 
            padding: 0; 
            background: #000; 
            display: flex; 
            justify-content: center; 
            align-items: center;
            min-height: 100vh;
            flex-direction: column;
            font-family: Arial, sans-serif;
        }}
        .nav {{
            position: fixed;
            top: 20px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(0,0,0,0.9);
            padding: 15px 25px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            z-index: 1000;
            border: 2px solid #32CD32;
        }}
        .back-link {{
            color: #32CD32;
            text-decoration: none;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 24px;
            border: 2px solid #32CD32;
            border-radius: 10px;
            background: rgba(50,205,50,0.1);
            transition: all 0.3s ease;
        }}
        .back-link:hover {{
            background: #32CD32;
            color: #000;
            transform: scale(1.05);
        }}
        .artwork {{ 
            max-width: 90vw; 
            max-height: 80vh; 
            border: 5px solid #32CD32;
            border-radius: 25px;
            background: rgba(50,205,50,0.1);
            padding: 30px;
            box-shadow: 0 0 80px rgba(50,205,50,0.5);
            margin-top: 80px;
        }}
        .artwork img {{
            width: 100%;
            height: auto;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        }}
        .info {{
            color: white;
            text-align: center;
            margin-top: 30px;
            font-family: Arial, sans-serif;
        }}
        .tech-badge {{
            background: linear-gradient(45deg, #32CD32, #90EE90);
            color: #000;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 16px;
            display: inline-block;
            margin: 10px;
            box-shadow: 0 5px 15px rgba(50,205,50,0.4);
        }}
        .resolution {{
            color: #90EE90;
            font-size: 18px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="nav">
        <a href="/" class="back-link">← Back to Gallery</a>
        <div style="color: #32CD32; font-weight: bold; font-size: 20px;">Real Digital Art</div>
        <div style="color: #90EE90; font-size: 14px;">{os.path.basename(image_path)}</div>
    </div>
    
    <div class="artwork">
        <img src="data:image/png;base64,{img_base64}" alt="Real Digital Art">
    </div>
    
    <div class="info">
        <div class="tech-badge">🎨 PIL/Pillow Generated</div>
        <div class="tech-badge">🖼️ PNG Format</div>
        <div class="tech-badge">✨ Pixel Perfect</div>
        <div class="resolution">Resolution: {width} × {height} pixels</div>
        <p style="color: #32CD32; margin: 20px 0 0 0; font-size: 18px;">
            Real image processing artwork - not SVG!
        </p>
    </div>
</body>
</html>'''
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            else:
                self.send_error(404, "Real artwork not found")
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_png_file(self, file_path):
        """Serve PNG files"""
        try:
            if os.path.exists(file_path) and file_path.endswith('.png'):
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "PNG not found")
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == "__main__":
    port = 5001
    print(f"🎨 Real Digital Art Viewer starting on port {port}")
    print(f"✅ Displaying PIL/Pillow generated artwork")
    print(f"🖼️ Actual PNG images - not SVG!")
    print(f"🎯 Pixel-perfect digital art")
    
    try:
        with socketserver.TCPServer(("", port), RealArtHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Real art viewer stopped")
    except OSError as e:
        print(f"❌ Error: {e}")