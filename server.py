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
        elif self.path == '/api/add-source':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(body)
                repo_url = payload.get('repo')
                name = payload.get('name')
                if repo_url:
                    print(f"Adding source: {repo_url} ({name})...")
                    cmd = ["python3", "skill_collector.py", "add-source", repo_url]
                    if name:
                        cmd += ["--name", name]
                    subprocess.run(cmd, capture_output=True, text=True)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {"status": "success", "message": f"Added source {repo_url}"}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    return
            except Exception as e:
                print("Error adding source:", e)
            self.send_response(400)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    print(f"Open http://localhost:{PORT} in your browser.")
    httpd.serve_forever()
