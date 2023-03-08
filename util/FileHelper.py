import os
fileList = []

def init():
    i = os.listdir("download/")
    for j in i:
        fileList.append(j)

def getFileList():
    return fileList

def addFile(fileName):
    fileList.append(fileName)

