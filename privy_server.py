#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 5000
BIND_ADDRESS = "0.0.0.0"

class PryvyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="hyperflow-presale-live", **kwargs)

def main():
    print(f"Starting HyperFlow Privy Server on {BIND_ADDRESS}:{PORT}")
    print(f"Real Privy Integration: http://localhost:{PORT}/real-privy.html")
    print(f"Original Presale: http://localhost:{PORT}/index.html")
    
    try:
        with socketserver.TCPServer((BIND_ADDRESS, PORT), PryvyHandler) as httpd:
            print(f"Server running at http://{BIND_ADDRESS}:{PORT}")
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {PORT} is already in use. Server may already be running.")
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()