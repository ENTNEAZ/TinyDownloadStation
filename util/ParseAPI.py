from urllib import parse
import util.UserHelper as UserHelper
import time


import config


def api(http, api: str, query: str):
    query = parse.parse_qs(query)
    try:
        return {
            'login': login
        }[api](http, query)
    except KeyError:
        http.send_response(404)
        http.send_header("Content-type", "text/html")
        http.end_headers()
        http.wfile.write(br'{"reason":"API not found"}')


def login(http, query: dict):
    result = UserHelper.UserHelper.getInstance().checkUser(
        query['username'][0], query['hashPassword'][0])
    if result:
        http.send_response(302)
        http.send_header("Content-type", "text/html")
        # add cookie
        cookie = "user_session=" + UserHelper.UserHelper.getInstance().summonCookieForUser(query['username'][0]) +\
            ";domain=" + config.domain + \
            ";samesite=none;secure;expires=" + \
            time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", time.gmtime(
                time.time() + config.userCookieExpireTime))

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
    ...
