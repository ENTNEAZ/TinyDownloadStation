from urllib import parse
import util.UserHelper as UserHelper
import time
import json

import config_test as config
from . import Log
from . import UserHelper
from . import FileHelper


def api(http, api: str, query: str):
    query = parse.parse_qs(query)
    try:
        return {
            'login': login,
            'getDownloadList': getDownloadList
        }[api](http, query)
    except KeyError:
        http.send_response(404)
        http.send_header("Content-type", "text/html")
        http.end_headers()
        http.wfile.write(br'{"reason":"API not found"}')


def login(http, query: dict):
    result = UserHelper.UserHelper.getInstance().checkUser(
        query['username'][0], query['hashPassword'][0])
    Log.LoggerBasic.getInstance().loginLog(
        ip=http.client_address[0], username=query['username'][0], success=result)
    if result:
        http.send_response(302)
        http.send_header("Content-type", "text/html")
        # add cookie
        cookie = "userSessionID=" + UserHelper.UserHelper.getInstance().summonCookieForUser(query['username'][0]) +\
            ";domain=" + config.domain + \
            ";samesite=none;secure;expires=" + \
            time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", time.gmtime(
                time.time() + config.userCookieExpireTime)) + ";" + \
            "path=/"

        http.send_header("Set-Cookie", cookie)
        http.send_header("Location", "/login/loginSuccess.html")
        http.end_headers()
        http.wfile.write(b"Login Success")
    else:
        http.send_response(302)
        http.send_header("Content-type", "text/html")
        http.send_header("Location", "/login/loginFailed.html")
        http.end_headers()
        http.wfile.write(b"Login Failed")


def getDownloadList(http, query: dict):
    cookie = http.headers.get('Cookie')
    if cookie is None:
        http.send_response(302)
        http.send_header("Content-type", "text/html")
        http.send_header("Location", "/login/login.html")
        http.end_headers()
        http.wfile.write(b"Login")
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
    if not (UserHelper.UserHelper.getInstance().getUserOfCookie(realCookie) is None):
        # get file list
        fileList = FileHelper.getFileList()
        http.send_response(200)
        http.send_header("Content-type", "application/json")
        http.end_headers()
        http.wfile.write(json.dumps(fileList).encode('utf-8'))
    else:
        http.send_response(302)
        http.send_header("Content-type", "text/html")
        http.send_header("Location", "/login/login.html")
        http.end_headers()
        http.wfile.write(b"Login")
        return
