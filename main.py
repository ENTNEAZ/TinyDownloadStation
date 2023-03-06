# http服务器
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import ssl


import config


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello World !")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello World !")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    server = ThreadedHTTPServer(('127.0.0.1', 8532), Handler)
    server.socket = ssl.wrap_socket(
        server.socket,
        keyfile=config.keyfile,
        certfile=config.certfile,
        server_side=True
    )
    print('[HttpServer]Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
