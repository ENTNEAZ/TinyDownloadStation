from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib import parse
import ssl
import time

import config
import util.Log as Log
from util.UserHelper import UserHelper

# logger
log = None
# userHelper
userHelper = None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        if (parsed_path.path.startswith('/api/')):
            self.do_API(parsed_path.path)
            return

        if (parsed_path.path == '/'):
            # give user.html or login.html
            # up to cookie
            self.send_response(418)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Hello World !")
            ...
        else:
            # return file in html folder
            requirePath = parsed_path.path[1:]
            try:
                f = open("html/" + requirePath, 'rb')
                self.send_response(200)

                # decode require file type
                requireFileType = requirePath.split('.')
                try:
                    ret = {
                        'html': 'text/html',
                        'css': 'text/css',
                        'js': 'text/javascript',
                        'png': 'image/png',
                        'jpg': 'image/jpg',
                        'ico': 'image/ico'
                    }[requireFileType[-1]]
                except KeyError:
                    ret = 'text/html'

                self.send_header("Content-type", ret)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            except Exception as e:
                print(e)
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"404 Not Found")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello World !")

    def do_API(self, path):
        # path example : /api/xxx/xxx/xxx
        path = path.split('/')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello World API !")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    try:
        t = str(time.ctime())
        t = t.replace(' ', '_')
        t = t.replace(':', '-')
        log = Log.LoggerBasic(config.logPath, t + ".log")

        userHelper = UserHelper(
            config.userPasswordFilePath, config.userCookieFilePath)
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
