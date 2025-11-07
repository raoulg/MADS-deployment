from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello from Python Container!')

if __name__ == '__main__':
    server = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
    print('Starting server on port 8000')
    server.serve_forever()
