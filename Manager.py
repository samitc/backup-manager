import tkinter
import pickle
import os
import ntpath
from tkinter import filedialog

from File import File

global rootFile
global curFile
global curFileData
global curFileList

dataWid = []
listWid = []

global accentW


def initFiles():
    global curFile
    global rootFile
    rootFile = File(None, "beckup", "", "")
    curFile = rootFile


def addAc():
    global curFile
    global accentW
    curFile.addAccent(accentW.get())
    newFile(curFile)


def removeAc():
    global curFile
    global accentW
    curFile.removeAccent(accentW.get())
    newFile(curFile)


def loadData():
    global rootFile
    with open("data.ser", "rb") as input:
        rootFile = pickle.load(input)
    newFile(rootFile)


def saveData():
    global rootFile
    with open("data.ser", "wb") as output:
        pickle.dump(rootFile, output, pickle.HIGHEST_PROTOCOL)


def initWindow(root):
    global curFileData
    global curFileList
    curFileData = tkinter.Frame(root)
    curFileList = tkinter.Frame(root)
    generalFrame = tkinter.Frame(root)
    addAccent = tkinter.Button(generalFrame, text="add accent", command=addAc)
    addAccent.pack()
    removeAccent = tkinter.Button(generalFrame, text="remove accent", command=removeAc)
    removeAccent.pack()
    global accentW
    accentW = tkinter.Entry(generalFrame)
    accentW.pack()
    newFolder = tkinter.Button(generalFrame, text="add folder", command=addFolder)
    newFolder.pack()
    newfile = tkinter.Button(generalFrame, text="add file", command=addFile)
    newfile.pack()
    deletefile = tkinter.Button(generalFrame, text="delete file", command=delFile)
    deletefile.pack()
    back = tkinter.Button(generalFrame, text="back", command=backClick)
    back.pack()
    load = tkinter.Button(generalFrame, text="load", command=loadData)
    load.pack()
    save = tkinter.Button(generalFrame, text="save", command=saveData)
    save.pack()
    curFileList.pack(side=tkinter.RIGHT, fill=tkinter.X)
    curFileData.pack(side=tkinter.LEFT, fill=tkinter.X)
    generalFrame.pack(side=tkinter.BOTTOM, fill=tkinter.Y)
    newFile(curFile)


def newFile(file):
    global dataWid
    global listWid
    global curFile
    curFile = file
    for w in dataWid:
        w.destroy()
    for w in listWid:
        w.destroy()
    dataWid = createFileDataFrame(file, curFileData)
    listWid = createFileListFrame(file, curFileList)


def backClick():
    if curFile.parent is not None:
        newFile(curFile.parent)


def lClick(event):
    fileName = event.widget.cget("text")
    for file in curFile.files:
        if file.name == fileName:
            newFile(file)
            break


def createFileDataFrame(file, frame):
    thisFile = tkinter.Text(frame)
    thisFile.insert(tkinter.INSERT, "name:")
    thisFile.insert(tkinter.INSERT, file.name)
    thisFile.insert(tkinter.INSERT, os.linesep)
    thisFile.insert(tkinter.INSERT, "hash:")
    thisFile.insert(tkinter.INSERT, file.hash)
    thisFile.insert(tkinter.INSERT, os.linesep)
    thisFile.insert(tkinter.INSERT, os.linesep)
    thisFile.insert(tkinter.INSERT, "accents:")
    thisFile.insert(tkinter.INSERT, os.linesep)
    for acc in file.accents:
        thisFile.insert(tkinter.INSERT, acc)
        thisFile.insert(tkinter.INSERT, os.linesep)
    thisFile.pack()
    return [thisFile]


def createFileListFrame(file, frame):
    wid = []
    for f in file.files:
        label = tkinter.Label(frame, text=f.name)
        label.bind('<Button-1>', lClick)
        label.pack()
        wid.append(label)
    return wid


def delFile():
    global curFile
    nextFile = curFile.parent
    if nextFile is not None:
        nextFile.removeFile(curFile)
    newFile(nextFile)


def addFile():
    filePath = filedialog.askopenfilename(title="select file")
    hashFilePath = filedialog.askopenfilename(title="select file hash")
    hashStr = None
    with open(hashFilePath, "r") as f:
        for line in f:
            if hashStr == None:
                line = line[line.index(": ") + 2:]
                hashStr = ''
            hashStr += line.strip() + " "
    fileName = ntpath.basename(filePath)
    hashName = ntpath.basename(hashFilePath)
    global curFile
    curFile.addFile(File(curFile, fileName, hashName, hashStr))
    newFile(curFile)


def addFolder():
    global curFile
    global accentW
    name = accentW.get()
    curFile.addFile(File(curFile, name, "", ""))
    newFile(curFile)


initFiles()
top = tkinter.Tk()
initWindow(top)
top.mainloop()
