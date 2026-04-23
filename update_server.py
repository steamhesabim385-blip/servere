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
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1a1a1a; color: white; text-align: center; margin-top: 50px; }}
                    .container {{ background-color: #262626; padding: 40px; border-radius: 15px; display: inline-block; box-shadow: 0px 0px 25px rgba(0,0,0,0.7); border: 1px solid #333; }}
                    h1 {{ color: #007aff; margin-bottom: 10px; }}
                    h2 {{ color: #2ecc71; font-size: 24px; }}
                    .version-box {{ font-size: 48px; font-weight: bold; margin: 20px 0; color: #f1c40f; }}
                    input[type="text"] {{ padding: 12px; font-size: 18px; border-radius: 5px; border: 1px solid #444; background: #111; color: white; width: 100px; text-align: center; margin-bottom: 20px; }}
                    .btn {{ background-color: #007aff; color: white; border: none; padding: 15px 30px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.3s; width: 100%; }}
                    .btn:hover {{ background-color: #0056b3; transform: scale(1.02); }}
                    p {{ color: #888; font-size: 14px; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>KRMV Loader Control</h1>
                    <p>Mevcut Sunucu Versiyonu</p>
                    <div class="version-box">{CURRENT_VERSION}</div>
                    
                    <form method="POST" action="/update">
                        <label>Yeni Versiyonu Girin:</label><br><br>
                        <input type="text" name="version" value="{CURRENT_VERSION}" placeholder="Örn: 1.2">
                        <br>
                        <button class="btn" type="submit">VERSIONU GUNCELLE</button>
                    </form>
                    <p>Loader bu versiyonu /api/version adresinden kontrol eder.</p>
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
            # Form verisini oku
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            if 'version' in params:
                new_version = params['version'][0]
                CURRENT_VERSION = new_version
                print(f"Versiyon güncellendi: {CURRENT_VERSION}")
            
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
