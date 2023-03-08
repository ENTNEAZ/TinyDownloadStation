import os
import config
fileList = []


def init():
    i = os.listdir(config.savePath)
    for j in i:
        fileList.append(j)


def getFileList():
    return fileList


def addFile(fileName):
    fileList.append(fileName)
