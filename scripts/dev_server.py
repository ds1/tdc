import http.server
import socketserver
import os
import mimetypes
import json

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Get project root directory
        self.project_root = os.path.dirname(script_dir)
        # Set src directory
        self.src_dir = os.path.join(self.project_root, 'src')
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        """Map URLs to the correct directory"""
        # Remove query parameters if any
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        
        # Remove .html if present at the end
        if path.endswith('.html'):
            path = path[:-5]

        # Normalize slashes
        path = path.strip('/')
        
        # Special handling for domain detail pages
        if path.startswith('domains/') and not path.endswith(('.html', '.css', '.js')):
            return os.path.join(self.src_dir, 'domains/template.html')
        
        # Special handling for root path
        if not path:
            return os.path.join(self.src_dir, 'index.html')
        
        # Handle data directory requests
        if path.startswith('data/'):
            return os.path.join(self.project_root, path)
        
        # All other paths serve from src directory
        return os.path.join(self.src_dir, path)

    def send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def send_csp_headers(self):
        """Send Content Security Policy headers"""
        csp = (
            "default-src 'self' blob: data: https:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' blob: https:; "
            "style-src 'self' 'unsafe-inline' https:; "
            "img-src 'self' data: blob: https:; "
            "font-src 'self' data: https:; "
            "connect-src 'self' https: http: ws: wss: localhost:*; "
            "worker-src 'self' blob: https:; "
            "frame-src 'self' https:; "
            "media-src 'self' blob: https:; "
            "object-src 'none'; "
            "base-uri 'self';"
        )
        self.send_header('Content-Security-Policy', csp)

    def do_GET(self):
        """Handle GET requests"""
        # Map the requested path to a file system path
        path = self.translate_path(self.path)
        
        try:
            # Special handling for JSON files
            if path.endswith('.json'):
                with open(path, 'r', encoding='utf-8') as f:
                    content = json.load(f)  # Verify it's valid JSON
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps(content).encode('utf-8'))
                    return

            # Handle all other files
            with open(path, 'rb') as f:
                self.send_response(200)
                
                # Set content type
                content_type = self.guess_type(path)
                if content_type is None:
                    content_type = 'application/octet-stream'
                self.send_header('Content-Type', content_type)
                
                # Send appropriate headers based on file type
                if path.endswith('.html'):
                    self.send_csp_headers()
                
                self.send_cors_headers()
                
                # Send file length
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs[6]))
                
                self.end_headers()
                
                # Send file content
                self.copyfile(f, self.wfile)
                
        except FileNotFoundError:
            # Special handling for domain detail pages
            if self.path.startswith('/domains/'):
                try:
                    template_path = os.path.join(self.src_dir, 'domains/template.html')
                    with open(template_path, 'rb') as f:
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/html')
                        self.send_csp_headers()
                        self.send_cors_headers()
                        self.end_headers()
                        self.copyfile(f, self.wfile)
                        return
                except FileNotFoundError:
                    pass
            self.send_error(404, f"File not found: {self.path}")
        except json.JSONDecodeError as e:
            self.send_error(500, f"Invalid JSON file: {e}")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

    def guess_type(self, path):
        """Guess the type of a file based on its extension"""
        type = super().guess_type(path)
        if type is None:
            if path.endswith('.json'):
                return 'application/json'
        return type

    def log_message(self, format, *args):
        """Log messages to console"""
        print(f"{self.client_address[0]} - {format%args}")

def run_server(port=8080):
    """Run the development server"""
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"\nStarting development server at http://localhost:{port}")
        print("\nDirectory structure:")
        print(f"  Project root: {os.path.abspath(os.path.dirname(os.path.dirname(__file__)))}")
        print("\nAvailable routes:")
        print("  - /                           -> src/index.html")
        print("  - /domains/{domain-name}      -> src/domains/template.html")
        print("  - /data/output/domains.json   -> data/output/domains.json")
        print("  - /data/output/thumbnails/*   -> data/output/thumbnails/*")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == '__main__':
    run_server()