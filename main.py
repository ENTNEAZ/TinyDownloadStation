from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import ssl
import time

import config
import Log


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
    log = None
    try:
        t = str(time.ctime())
        t = t.replace(' ', '_')
        t = t.replace(':', '-')
        log = Log.LoggerBasic("log/", t + ".log")
    except Exception as e:
        print(e)
        raise e

    try:
        log.basicLog('Server started')
        server = ThreadedHTTPServer(('127.0.0.1', 80), Handler)
        '''
        server.socket = ssl.wrap_socket(
            server.socket,
            keyfile=config.keyfile,
            certfile=config.certfile,
            server_side=True
        )
        '''
        print('[HttpServer]Starting server, use <Ctrl-C> to stop')
        server.serve_forever()

    except KeyboardInterrupt:
        print('[HttpServer]Stopping server')
        log.basicLog('Server stopped by user')
        server.socket.close()
        log.close()
        exit(0)
    except Exception as e:
        print(e)
        log.basicLog('Server stopped by error')
        log.basicLog(e)
        server.socket.close()
        log.close()
        exit(-1)
