#!/usr/bin/env python3
"""
Simple test server to isolate the port binding issue
"""
import socket
import http.server
import socketserver
import time
import sys

def test_port_binding():
    """Test if we can bind to port 5000"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', 5000))
            print("✅ Port 5000 is available")
            return True
    except Exception as e:
        print(f"❌ Port 5000 binding failed: {e}")
        return False

def start_simple_server():
    """Start a simple HTTP server"""
    class SimpleHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>SocialX Test Server Running</h1>")

    PORT = 5000
    
    # Test port availability first
    if not test_port_binding():
        print("Trying alternative port...")
        PORT = 5001
    
    try:
        httpd = socketserver.TCPServer(("0.0.0.0", PORT), SimpleHandler)
        httpd.allow_reuse_address = True
        print(f"🚀 Test server starting on port {PORT}...")
        print(f"📍 Server URL: http://0.0.0.0:{PORT}")
        
        # Test that server actually starts
        for i in range(5):
            print(f"Server tick {i+1}...")
            httpd.handle_request()
            time.sleep(1)
        
        print("✅ Test server completed successfully")
        
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_simple_server()