from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib import parse
import ssl
import time
import cgi

import config_test as config
import util.Log as Log
from util.UserHelper import UserHelper
import util.ParseAPI as ParseAPI
import util.FileHelper as FileHelper
# logger
log = None
# userHelper
userHelper = None


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # correct ip

        if (self.client_address[0] == "127.0.0.1"):
            try:
                IP_addr = self.headers.get('Ali-CDN-Real-IP')
                if IP_addr is None:
                    IP_addr = self.headers.get('X-Forwarded-For')
                if IP_addr is None:
                    IP_addr = self.headers.get('X-Real-IP')
                if IP_addr is None:
                    IP_addr = self.client_address[0]
                self.client_address = (IP_addr, self.client_address[1])
            except Exception as e:
                ...

        parsed_path = parse.urlparse(self.path)
        if (parsed_path.path.startswith('/api/')):
            self.do_API(parsed_path.path, parsed_path.query)
            return

        if (parsed_path.path == '/'):
            # give user.html or login.html
            # up to cookie
            # parse cookie
            cookie = self.headers.get('Cookie')
            if cookie is None:
                self.send_response(302)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/login/login.html")
                self.end_headers()
                self.wfile.write(b"Login")
                return
            cookie = cookie.split(';')
            realCookie = ''
            for i in cookie:
                i = i.strip()  # reduce space
                if i.startswith('userSessionID='):
                    print(realCookie)
                    realCookie = i.split('=')[1]
                    break
            # check cookie
            if not (userHelper.getInstance().getUserOfCookie(realCookie) is None):
                # return user.html
                with open("html/user/user.html", 'rb') as f:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(f.read())
            else:
                # return login.html
                self.send_response(302)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/login/login.html")
                self.end_headers()
                self.wfile.write(b"Login")
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
        # correct ip

        if (self.client_address[0] == "127.0.0.1"):
            try:
                IP_addr = self.headers.get('Ali-CDN-Real-IP')
                if IP_addr is None:
                    IP_addr = self.headers.get('X-Forwarded-For')
                if IP_addr is None:
                    IP_addr = self.headers.get('X-Real-IP')
                if IP_addr is None:
                    IP_addr = self.client_address[0]
                self.client_address = (IP_addr, self.client_address[1])
            except Exception as e:
                ...

        parsed_path = parse.urlparse(self.path)
        if (parsed_path.path.startswith('/upload')):
            # upload file
            # save file
            formdata = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            cookie = self.headers.get('Cookie')
            if cookie is None:
                self.send_response(302)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/login/login.html")
                self.end_headers()
                self.wfile.write(b"Login")
                return
            cookie = cookie.split(';')
            realCookie = ''
            for i in cookie:
                i = i.strip()
                if i.startswith('userSessionID='):
                    realCookie = i.split('=')[1]
                    break
            # check cookie
            username = userHelper.getInstance().getUserOfCookie(realCookie)
            if not (username is None):
                # parse file name
                fileName = formdata['filename']
                fileContent = formdata['file']

                # save file
                fileName = fileName.value
                with open('download/' + fileName, 'wb') as f:
                    f.write(fileContent.file.read())

                log.uploadLog(
                    self.client_address[0], username, fileName)
                FileHelper.addFile(fileName)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Upload Success")
            else:
                # return login.html
                self.send_response(302)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/login/login.html")
                self.end_headers()
                self.wfile.write(b"Login")
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_API(self, path, query):
        # path example : /api/xxx/xxx/xxx?xxx=xxx&xxx=xxx
        apiName = path.split('/')[2]
        ParseAPI.api(self, apiName, query)


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

        FileHelper.init()
    except Exception as e:
        print(e)
        raise e

    try:
        log.basicLog('Server started')
        server = ThreadedHTTPServer(('127.0.0.1', config.port), Handler)
        server.socket = ssl.wrap_socket(
            server.socket,
            keyfile=config.keyfile,
            certfile=config.certfile,
            server_side=True
        )
        print('[HttpServer]Starting server, use <Ctrl-C> to stop')
        server.serve_forever()

    except KeyboardInterrupt:
        print('[HttpServer]Stopping server')
        log.basicLog('Server stopped by user')
        server.socket.close()
        log.close()
        userHelper.close()
        exit(0)
    except Exception as e:
        print(e)
        log.basicLog('Server stopped by error')
        log.basicLog(e)
        server.socket.close()
        log.close()
        userHelper.close()
        exit(-1)
