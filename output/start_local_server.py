"""
Simple local HTTP server to serve the character database HTML.
This avoids CORS issues when opening HTML files.
"""

import http.server
import socketserver
import os
import webbrowser

PORT = 8002

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

def start_server():
    """Start local HTTP server"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/character_database.html"
        print("="*60)
        print("Local HTTP Server Started!")
        print("="*60)
        print(f"\nServer running at: http://localhost:{PORT}")
        print(f"\nOpen in browser: {url}")
        print("\nPress Ctrl+C to stop the server")
        print("="*60)
        
        # Try to open browser automatically
        try:
            webbrowser.open(url)
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    start_server()
