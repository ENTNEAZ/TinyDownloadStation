import json


class UserHelper:
    userPath = None
    cookiePath = None

    userPasswordDict = None
    userCookieDict = None

    def __init__(self, userPath, cookiePath):
        self.userPath = userPath
        self.cookiePath = cookiePath
        self.userPasswordDict = json.load(open(self.userPath, 'r'))
        self.userCookieDict = json.load(open(self.cookiePath, 'r'))

    def checkUser(self, username, hashPassword) -> bool:
        if username in self.userPasswordDict:
            return self.userPasswordDict[username] == hashPassword
        else:
            return False

    def getUserOfCookie(self, cookie) -> str:
        # return None if not found
        if cookie in self.userCookieDict:
            return self.userCookieDict[cookie]
        else:
            return None

    def addCookie(self, username, cookie):
        self.userCookieDict[cookie] = username

    def saveAll(self):
        json.dump(self.userPasswordDict, open(self.userPath, 'w'))
        json.dump(self.userCookieDict, open(self.cookiePath, 'w'))

    def addUser(self, username, hashPassword):
        self.userPasswordDict[username] = hashPassword
