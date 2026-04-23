import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Global version
CURRENT_VERSION = "1.0"

class UpdateServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global CURRENT_VERSION
        
        # Loader'ın kontrol ettiği API
        if self.path == '/api/version':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"version": CURRENT_VERSION}
            self.wfile.write(json.dumps(response).encode())
            
        # Admin Web Paneli (Railway'de tarayıcıdan girilecek)
        elif self.path == '/' or self.path == '/admin':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Basit Web Arayüzü (HTML)
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>KRMV Hile Kontrol Paneli</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #2c3e50; color: white; text-align: center; margin-top: 50px; }}
                    .container {{ background-color: #34495e; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0px 0px 15px rgba(0,0,0,0.5); }}
                    h1 {{ color: #f1c40f; }}
                    h2 {{ color: #2ecc71; }}
                    .btn {{ background-color: #e74c3c; color: white; border: none; padding: 15px 30px; font-size: 18px; font-weight: bold; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin-top: 20px; }}
                    .btn:hover {{ background-color: #c0392b; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Admin Kontrol Paneli</h1>
                    <h2>Guncel Hile Versiyonu: {CURRENT_VERSION}</h2>
                    <form method="POST" action="/update">
                        <button class="btn" type="submit">HILEYI 1.1'E GUNCELLE (UPDATE AT)</button>
                    </form>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global CURRENT_VERSION
        if self.path == '/update':
            # Butona basıldığında versiyonu 1.1 yap
            CURRENT_VERSION = "1.1"
            
            # Geri ana sayfaya yönlendir
            self.send_response(303)
            self.send_header('Location', '/admin')
            self.end_headers()

def run_server():
    # Railway'in atadığı portu al, yoksa 8080 kullan
    port = int(os.environ.get("PORT", 8080))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, UpdateServerHandler)
    print(f"Server started on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
