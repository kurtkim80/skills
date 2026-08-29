import http.server
import socketserver
import subprocess
import json

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/sync':
            print("Sync started...")
            result = subprocess.run(["python3", "skill_collector.py", "sync"], capture_output=True, text=True)
            self.send_response(200 if result.returncode == 0 else 500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "success" if result.returncode == 0 else "error", "output": result.stdout}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            print("Sync finished.")
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    print(f"Open http://localhost:{PORT} in your browser.")
    httpd.serve_forever()
