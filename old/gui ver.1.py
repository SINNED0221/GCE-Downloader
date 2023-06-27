import urllib3.contrib.pyopenssl
import tkinter
from tkinter import *
from tkinter import filedialog
import requests
from PIL import ImageTk, Image

igPhysics = {"name": "physics",
             "level": "Cambridge%20IGCSE",
             "subject": "Physics%20(0625)",
             "code": "0625",
             "paper": [1, 2, 3, 4, 5, 6],
             "m": [2],
             "s": [1, 2, 3],
             "w": [1, 2, 3]}
alPhysics = {}
igcse = {"Physics": igPhysics}
alevel = {"Physcis": alPhysics}
levelTable = {"igcse": igcse, "alevel": alevel}

# basic window setting
root = Tk()
root.title("GCE downloader gui")
root.iconbitmap("resources/icon.ico")
root.geometry("480x720")

title = Label(root, text="GCE downloader\ncopyright 2022 all rights reserved")
title.pack()

# dropdown for level selection
level = StringVar()
dropLevel = OptionMenu(root, level, *levelTable.keys())
dropLevel.pack()
# function that updates the level selection
curLevel = []
def confirmLevel():
    global curLevel
    curLevel = levelTable[level.get]
# button that confirms
levelCon = Button(root, text="confirm", command=confirmLevel)
levelCon.pack()



root.mainloop()
