from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote_plus 
import mimetypes
from pathlib import Path
import json
from datetime import datetime

class HttpGetHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers.get('Content-Length')))
        self.save_to_json(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        match url.path:
            case '/':
                self.send_html('index.html')
            case '/contacts':
                self.send_html('contacts.html')
            case '/message':
                self.send_html('message.html')
            case '/blog':
                self.send_html('blog.html')
            case _:
                file_path = Path(url.path[1:])
                if file_path.exists():
                    self.send_static(str(file_path))
                else:
                    self.send_html('message.html', 404)
                
    def send_static(self, static_filename):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(static_filename, 'rb') as f:
            self.wfile.write(f.read())


    def send_html(self, html_filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', "text/html")
        self.end_headers()
        with open(html_filename, 'rb') as f:
            self.wfile.write(f.read())

    def save_to_json(self, raw_data):
        data = unquote_plus(raw_data.decode())
        dict_data = {key: value for key, value in [el.split("=") for el in data.split("&")]}
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open("storage/data.json", "r+", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}
            existing_data[timestamp] = dict_data
            f.seek(0)
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            f.truncate()

def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 3000 )
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == "__main__":
    run()

