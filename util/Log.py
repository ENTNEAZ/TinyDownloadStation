import time


class LoggerBasic:
    fileName = None
    filePath = None
    openFile = None

    # static instance
    instance = None

    def __init__(self, filePath: str, fileName: str):
        self.fileName = fileName
        self.filePath = filePath
        try:
            self.openFile = open(self.filePath + self.fileName, 'w')
        except Exception as e:
            print(e)
            raise e
        LoggerBasic.instance = self

    def basicLog(self, msg):
        msg = '[' + time.ctime() + '] ' + msg
        print(msg)
        self.openFile.write(msg + '\n')

    def loginLog(self, ip: str, username: str, success: bool):
        if success:
            self.basicLog('[' + ip + ']Login successful: ' + username)
        else:
            self.basicLog('[' + ip + ']Login failed: ' + username)

    def uploadLog(self, ip: str, username: str, fileName: str):
        self.basicLog('['+ip+']'+username+' uploaded file: '+fileName)

    def downloadLog(self, ip: str, username: str, fileName: str):
        self.basicLog('['+ip+']'+username+' downloaded file: '+fileName)

    def close(self):
        self.basicLog('Log file closed')
        self.openFile.close()

    @staticmethod
    def getInstance():
        return LoggerBasic.instance
