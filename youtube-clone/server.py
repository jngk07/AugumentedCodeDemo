#!/usr/bin/env python3
"""
Simple HTTP server for the YouTube Clone project.
Run this script to serve the files locally.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Configuration
PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    """Start the HTTP server and optionally open the browser."""
    
    # Change to the project directory
    os.chdir(DIRECTORY)
    
    # Create the server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🎥 YouTube Clone Server")
        print(f"📁 Serving directory: {DIRECTORY}")
        print(f"🌐 Server running at: http://localhost:{PORT}")
        print(f"🏠 Home page: http://localhost:{PORT}/index.html")
        print(f"🧪 Test page: http://localhost:{PORT}/test.html")
        print(f"\n📋 Available pages:")
        print(f"   • Home: http://localhost:{PORT}/index.html")
        print(f"   • Video Player: http://localhost:{PORT}/video.html")
        print(f"   • Search: http://localhost:{PORT}/search.html")
        print(f"   • Test: http://localhost:{PORT}/test.html")
        print(f"\n⚡ Press Ctrl+C to stop the server")
        
        # Optionally open the browser
        if len(sys.argv) > 1 and sys.argv[1] == '--open':
            webbrowser.open(f'http://localhost:{PORT}/test.html')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    main()
