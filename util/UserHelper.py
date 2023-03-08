import json
import random
import time


class UserHelper:
    instance = None
    userPath = None
    cookiePath = None

    userPasswordDict = None
    userCookieDict = None

    def __init__(self, userPath, cookiePath):
        self.userPath = userPath
        self.cookiePath = cookiePath
        self.userPasswordDict = json.load(open(self.userPath, 'r'))
        self.userCookieDict = json.load(open(self.cookiePath, 'r'))
        UserHelper.instance = self

    def checkUser(self, username, hashPassword) -> bool:
        if username in self.userPasswordDict:
            return self.userPasswordDict[username] == hashPassword
        else:
            return False

    def getUserOfCookie(self, cookie: str) -> str:
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

    def close(self):
        self.saveAll()

    def addUser(self, username, hashPassword):
        self.userPasswordDict[username] = hashPassword

    def summonCookieForUser(self, username):
        for cookie in self.userCookieDict:
            if self.userCookieDict[cookie] == username:
                return cookie
        # summon one

        cookie = str(int(time.time()) ** 2 +
                     random.randint(0, 1000000000) + hash(username))
        self.userCookieDict[cookie] = username
        return cookie

    @ classmethod
    def getInstance(self):
        return UserHelper.instance
