from time import sleep
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import requests
import os.path
import threading
from datetime import date
import time
import os
import sys
from PIL import ImageTk, Image
import webbrowser


# THIS PROGRAM IS (SOMEHOW) DEPENDENT ON urllib3 version 1.23 AS NEWER VERSIONS HAVE SOME BUGS


def resourcePath(relativePath):  # get the embeded files' location
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")
    return os.path.join(basePath, relativePath)


root = Tk()  # main window settings
root.title('GCE downloader gui')
root.iconbitmap(resourcePath('icon.icns'))
root.geometry('750x490')
root.resizable(height=False, width=False)


# TODO:Resizable windows with widgets resize accordingly

def quitRoot():  # terminate the program
    root.quit()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", quitRoot)  # terminate the program once root is closed

levelList = {}
allYearList = []
igSubjectList = {}
alSubjectList = {}
levelRedirect = {}
defaultPath = ''
defaultThread = 4
latestYear = []
igBeginYear = []
alBeginYear = []
allSeason = []

# read config file
with open('resources/config.txt', 'r') as c:
    exec(c.read())

# user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# update functions are used to change the values in each menu when corresponding menus are changed
def updateSubject(*args):
    subs = levelList[varLevel.get()]  # subs= list of all subjects
    varSubject.set(subs[0])
    menu = drdSubject['menu']  # clear menu box
    menu.delete(0, 'end')
    for sub in subs:  # add each element into menu box
        menu.add_command(label=sub, command=lambda nation=sub: varSubject.set(nation))


def updateSeason(*args):
    level = levelRedirect[varLevel.get()]  # list of all subjects
    subject = level[varSubject.get()]  # paper detail of the subject
    titles = list(subject.keys())  # dictionary keys of paper detail
    lastI = len(titles)  # the index of last key in the dictionary
    seasons = titles[5:lastI - 2]  # list of keys that store seasons
    year = varYear.get()  # test if it is the latest year
    try:  # remove the seasons that haven't been released yey
        if int(year) == latestYear[0]:
            if latestYear[1] == 1:
                seasons.remove('s')
                seasons.remove('w')
            elif latestYear[1] == 2:
                seasons.remove('w')
    except:
        pass
    try:
        varSeason.set(seasons[0])
    except:
        pass
    menu = drdSeason['menu']
    menu.delete(0, 'end')  # clear menu box
    for season in seasons:  # add elements into menu box
        menu.add_command(label=season, command=lambda nation=season: varSeason.set(nation))


def updatePaper(*args):
    level = levelRedirect[varLevel.get()]  # list of all subjects
    subject = level[varSubject.get()]  # paper detail of the subject
    papers = subject['paper']  # list of papers
    varPaper.set(papers[0])

    # For the subjects that has changed papers, remove according to the year
    if subject == alMath:
        if int(varYear.get()) >=2020:
            papers = [1, 2, 3, 4, 5, 6]
            print(papers)
        else:
            papers = [1, 2, 3, 4, 5, 6, 7]
    else:
        pass

    menu = drdPaper['menu']
    menu.delete(0, 'end')  # clear menu box
    for paper in papers:  # add elements into menu box
        menu.add_command(label=paper, command=lambda nation=paper: varPaper.set(nation))


def updateVariant(*args):
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]  # paper detail
    try:  # in case the given paper do not have all variants
        variants = subject[varSeason.get()]
    except:  # if not, give the default variant
        keys = list(subject.keys())
        variants = subject[keys[5]]
    varVariant.set(variants[0])
    menu = drdVariant['menu']
    menu.delete(0, 'end')

    # check if the given paper has variant
    exceptionDic = subject['exception']
    exceptions = exceptionDic.keys()
    for exception in exceptions:
        if exception == varPaper.get():
            for e in exceptionDic[exception]:
                if e == 'noVariant':
                    variants = ['']
                    varVariant.set('')
                else:
                    pass
        else:
            pass

    # this shit was tough
    # if the given subject has experiment, add the variants to the list
    hasExperiment = varSubject.get() == "Biology" or varSubject.get() == "Physics" or varSubject.get() == "Chemistry"
    if hasExperiment and varLevel.get() == "AS/ALevel" and varPaper.get() == "3":
        if varSeason.get() == "m":  # for may/june, only variant 3 is available to experiment
            variants = [3]
            varVariant.set(3)
        else:
            variants = [1, 2, 3, 4, 5]  # for the rest seasons, add all five

    for variant in variants:
        menu.add_command(label=variant, command=lambda nation=variant: varVariant.set(nation))


def updateCompo(*args):
    global compoCheck
    compoMenu.menu.delete(0, END)
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    composs = subject['components']
    compos = composs.keys()
    compos = list(compos)  # list of all components available

    # check if the given paper have excluded component
    # exceptions is a dictionary which its keys are the papers and the elements is list of unavailable component
    exceptionDic = subject['exception']
    exceptions = exceptionDic.keys()
    for exception in exceptions:
        if exception == varPaper.get():
            for e in exceptionDic[exception]:
                try:
                    compos.remove(e)
                except:
                    pass
        else:
            pass
    compoCheck = {}  # clear the dictionary the holds component name and boolean value
    for compo in compos:
        varCompo = IntVar()
        compoMenu.menu.add_checkbutton(label=compo, variable=varCompo)
        compoCheck[compo] = varCompo


def updateYear(*args):  # to make new subjects display correct years
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    name = subject['name']
    titles = list(subject.keys())  # dictionary keys of paper detail
    lastI = len(titles)  # the index of last key in the dictionary
    seasons = titles[5:lastI - 2]  # list of keys that store seasons
    if varLevel.get() == 'iGCSE':
        beginYear = igBeginYear[name]
    elif varLevel.get() == 'AS/ALevel':
        beginYear = alBeginYear[name]
    allYearList = [y for y in
                   range(beginYear, latestYear[0] + 1)]  # work out the list from the beginning year of the subject
    yearList = sorted(allYearList, reverse=True)
    # for the subjects that has stopped, the later years are removed
    if name == 'Computer Science(9608)':
        yearList = [y for y in yearList if int(y) <= 2021]
    else:
        pass

    yearList = sorted(yearList, reverse=True)
    varVariant.set(yearList[0])
    try:  # remove the seasons that is not released yet
        if latestYear[1] == 1:
            seasons.remove('s')
            seasons.remove('w')
        elif latestYear[1] == 2:
            seasons.remove('w')
    except:
        pass
    if seasons == []:  # if the latest year does not have any paper released yet, remove latest year
        yearList.pop(0)
    else:
        pass

    menu = drdYear['menu']
    menu.delete(0, 'end')
    for year in yearList:
        menu.add_command(label=year, command=lambda nation=year: varYear.set(nation))

    if yearList.count(varYear.get()) > 0:  # set to default year if the previous year is not present in the new list
        pass
    else:
        varYear.set(yearList[0])


def addUrl():  # add the selected url and file name for download into lists
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    year = varYear.get()
    yy = year[2:]
    season = varSeason.get()
    paper = varPaper.get()
    variant = varVariant.get()
    if varCompoSelectAll.get() == 1:  # to see if the select all switch is turned
        checks = []
        checks = [(name, 1) for name, varCompo in compoCheck.items()]
    else:
        checks = []
        checks = [(name, varCompo.get()) for name, varCompo in compoCheck.items()]
    for (i, b) in checks:  # i= name of the component, b= boolean value(1/0) to show if the option is selected
        if b == 1:
            compo = i
            fileFormat = subject['components'][compo]
            url = 'https://papers.gceguide.com/' + subject['level'] + '/' + subject['subject'] + '/' + year + '/' + \
                  subject['code'] + '_' + season + yy + '_' + compo + '_' + paper + variant + '.' + fileFormat
            fileName = subject['code'] + '_' + season + yy + '_' + compo + '_' + paper + variant + '.' + fileFormat
            for n in downList:  # check if there is same files
                if n == fileName:
                    break
            else:
                urlList.append(url)
                fileName = (url.rsplit('/', 1)[1])
                if checkHistory(fileName):  # check if the file exists
                    downList.append(fileName+" (downloaded)")
                else:
                    downList.append(fileName)
    fileListBox.delete(0, END)
    fileListBox.insert(END, *downList)
    fileListBox.yview(END)  # scroll to the bottom once new item is added


def removeSelected(
        event=None):  # FIXED: when the button is pressed, no event is passed, so set the default value to None
    try:
        for i in sorted(fileListBox.curselection(),
                        reverse=True):  # put the selection in backward to avoid messed up index :)
            del downList[i]
            del urlList[i]
        fileListBox.delete(0, END)
        fileListBox.insert(END, *downList)
    except:
        pass


def clearAll():
    del urlList[0:]
    del downList[0:]
    fileListBox.delete(0, END)


def pathFinder():
    global path
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    # when the path length is longer than the label box could handle, shrink the path into showPath
    if len(path) > 31:
        showPath = path[0:14] + '...' + path[len(path) - 14:]
    else:
        showPath = path

    # edit default path into config.txt
    with open('resources/config.txt', 'r') as c:
        cList = c.readlines()
        cList[0] = 'defaultPath=' + '"' + path + '"' + '\n'
    with open('resources/config.txt', 'w') as c:
        c.writelines(cList)
        c.close()

    savePathLabel['text'] = showPath


def download():
    if os.path.exists(path):
        pass
    else:
        pathFinder()

    # top levels to show state
    loadingPop = Toplevel(root)
    loadingPop.iconbitmap(resourcePath('icon.icns'))
    loadingPop.geometry('360x150')
    loadingPop.title('Downloading...')
    loadingPop.resizable(height=False, width=False)

    # progress bar
    downProgress = ttk.Progressbar(loadingPop, orient=HORIZONTAL, mode='determinate', length=300)

    # disable X button
    def disableX():
        pass

    loadingPop.protocol("WM_DELETE_WINDOW", disableX)

    loadingPop.grab_set()  # prevent accessing main window during download
    downloadingLabel = Label(loadingPop, text='Downloading now, please wait...')
    downloadingLabel.place(relx=.5, rely=.5, anchor=CENTER)
    downloadingLabel.pack(pady=(40, 5), anchor=CENTER)
    downProgress.pack(pady=(0, 40), anchor=CENTER)

    # download module
    def coreDownload():
        global fails
        total = len(urlList)
        fails = 0  # record number of fail downloads

        # button for quiting the completion pop up
        def quitCompletion():
            completionPop.destroy()

        def monoDownload(url, number):
            global fails
            # fetch file name
            if url.find("/"):
                fileName = (url.rsplit('/', 1)[1])

            try:
                # download with requests
                res = requests.get(url, headers=headers, allow_redirects=True, stream=True, timeout=5)
                heads = requests.head(url)
                size = heads.headers["Content-Length"]  # testing if the file actually exist
                open(path + '/' + fileName, "wb").write(res.content)
                addDownHistory(fileName)  # add file to the history
                if "(downloaded)" in downList[number]:  # change the file name to downloaded
                    pass
                else:
                    downList[number] += " (downloaded)"
            except:
                fails += 1

        # multi-thread download with threadN threads
        threadN = varThread.get()
        # divide urls into groups of each with threadN urls
        chunks = [urlList[i * threadN:(i + 1) * threadN] for i in range((len(urlList) + threadN - 1) // threadN)]
        numberList = list(range(len(downList)))  # pass the file number to modify names in file listbox
        fileNumber = [numberList[i * threadN:(i + 1) * threadN] for i in range((len(numberList) + threadN - 1) // threadN)]
        for chunk, indexes in zip(chunks, fileNumber):  # download with multi-thread
            threads = []
            for u, i in zip(chunk, indexes):
                time.sleep(0.05)  # wait for file history to write in
                thread = threading.Thread(target=monoDownload, args=(u, i, ))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
                downProgress['value'] += (1 / total * 100)  # add the percentage of the file to the progress bar

        time.sleep(0.5)  # wait for the progress bar to display

        fileListBox.delete(0, END)  # refreshes list
        fileListBox.insert(END, *downList)
        fileListBox.yview(END)

        # download complete, remove old pop up and out pop up with results
        loadingPop.destroy()

        root.bell()  # ring the bell to notify
        completionPop = Toplevel(root)
        completionPop.iconbitmap(resourcePath('icon.icns'))
        completionPop.geometry('360x150')
        completionPop.title('Finished!')
        completionPop.resizable(height=False, width=False)
        quitButton = Button(completionPop, text='OK', command=quitCompletion)

        completionPop.grab_set()
        completionLabel = Label(completionPop,
                                text='Download Complete!\n\nSuccess:' + str(total - fails) + '\n\nFails:' + str(fails))
        completionLabel.pack(pady=10)
        quitButton.pack()

    # begin download with multi-thread
    downThread = threading.Thread(target=coreDownload, args=())
    downThread.start()


def popUpCR(*args):  # credit page
    cRpop = Toplevel(root)
    cRpop.iconbitmap(resourcePath('icon.icns'))
    cRpop.geometry('360x150')
    cRpop.title('Thanks for using!')
    cRpop.resizable(height=True, width=False)

    qrImage = Image.open(resourcePath('eegg.png'))  # image of qr code
    qrImage = qrImage.resize((250, 250))
    qrImage = ImageTk.PhotoImage(qrImage)
    qrLabel = Label(cRpop, image=qrImage)  # panel of the qr code
    qrLabel.image = qrImage

    cRLabel = Label(cRpop,
                    text='GCE downloader developed by Dennis Zhang\n\nVersion 1.06\n\n©2023, All rights reserved')
    cRLabel.pack(pady=27)
    qrLabel.pack()


def updateLatestYear():
    def coreLatestYear():
        global count
        global latestYear

        def findLatest(year, season):  # look for the latest year by go to the latest paper possible
            global count
            y = str(year)
            yy = str(y)[2:5]
            url = 'https://papers.gceguide.com/' + 'A%20Levels/Physics%20(9702)' + '/' + y + '/' + \
                  '9702' + '_' + season + yy + '_' + 'qp' + '_' + '1' + '2' + '.' + 'pdf'
            try:
                # download with requests
                res = requests.get(url, headers=headers, allow_redirects=True, stream=True, timeout=1)
                heads = requests.head(url)
                size = heads.headers["Content-Length"]  # testing if the file actually exist
            except KeyError:  # this count counts the amount of paper that cannot be downloaded
                count += 1
            except requests.exceptions.RequestException:
                count += 10  # indicate a connection error

        loadingPop = Toplevel(root)  # window pop up when updating
        loadingPop.iconbitmap(resourcePath('icon.icns'))
        loadingPop.geometry('360x150')
        loadingPop.title('Updating...')
        loadingPop.resizable(height=False, width=False)

        downloadingLabel = Label(loadingPop, text='Updating...')
        downloadingLabel.place(relx=.5, rely=.5, anchor=CENTER)
        downloadingLabel.pack

        loadingPop.grab_set()  # prevent accessing main window during download
        today = date.today()
        currentYear = int(today.strftime('%Y'))
        allSeason = ['m', 's', 'w']
        testList = [[currentYear - 1, 'w'], [currentYear, 'm'], [currentYear, 's'], [currentYear, 'w']]
        count = 0

        chunk = testList
        threads = []
        for u in chunk:
            thread = threading.Thread(target=findLatest, args=(u[0], u[1],))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        # according to the amount of paper that can be found, determine the seasons that is available
        if count == 0:  # All papers are found
            latestYear = [currentYear, 3]
        elif count == 1:
            latestYear = [currentYear, 2]
        elif count == 2:
            latestYear = [currentYear, 1]
        elif count == 3:
            latestYear = [currentYear - 1, 3]
        elif count == 4:  # no paper is found
            latestYear = [currentYear - 1, 2]

        updateYear()
        updateSeason()
        downloadingLabel.destroy()

        def killPopup():  # Function to kill the toplevel
            loadingPop.destroy()

        if not count > 10:  # ignore if there is connection error
            with open('resources/config.txt', 'r') as c:
                cList = c.readlines()
                cList[2] = 'latestYear= ' + str(latestYear) + '\n'
            with open('resources/config.txt', 'w') as c:
                c.writelines(cList)
                c.close()
            downloadingLabel = Label(loadingPop, text='Updating succeed!')
            downloadingLabel.place(relx=.5, rely=.4, anchor=CENTER)
            downloadingLabel.pack
            # Button to confirm and close the toplevel
            closeButton = Button(loadingPop, text='OK', command=lambda: killPopup(), width=30)
            closeButton.place(relx=.5, rely=.7, anchor=CENTER)
            closeButton.pack
        else:
            downloadingLabel = Label(loadingPop, text='Updating failed, please try again')
            downloadingLabel.place(relx=.5, rely=.4, anchor=CENTER)
            downloadingLabel.pack
            # Button to confirm and close the toplevel
            closeButton = Button(loadingPop, text='OK', command=lambda: killPopup(), width=30)
            closeButton.place(relx=.5, rely=.7, anchor=CENTER)
            closeButton.pack

    downThread = threading.Thread(target=coreLatestYear, args=())
    downThread.start()


def goURL(event):  # redirect to browser when the name in the list box is clicked
    number = fileListBox.curselection()[0]
    url = urlList[number]
    webbrowser.open(url, new=2)


def getAppdataDir():
    return os.path.join(os.path.expanduser('~/Library/Application Support'), 'GCE_download_history.txt')


def addDownHistory(name):
    historyDir = getAppdataDir()
    try:
        with open(historyDir, 'r') as f:
            download_history = set(f.read().splitlines())
    except FileNotFoundError:
        download_history = set()

    download_history.add(name)

    with open(historyDir, 'w') as f:
        f.write('\n'.join(download_history))


def checkHistory(name):
    historyDir = getAppdataDir()
    try:
        with open(historyDir, 'r') as f:
            download_history = set(f.read().splitlines())
    except FileNotFoundError:
        return False

    return name in download_history


# url and paper name and save path
urlList = []
downList = []
# get path from the config file
path = defaultPath
if len(path) > 31:
    showPath = path[0:14] + '...' + path[len(path) - 14:]
else:
    showPath = path

# left and right main frame
leftFrame = Frame(root)
rightFrame = Frame(root)
midCanvas = Canvas(root, width=4, height=330)
# make the two section same width
leftHolder = Label(leftFrame, width=40)
rightHolder = Label(rightFrame, width=40)

# variables of each menu
varLevel = StringVar()
varSubject = StringVar()
varYear = StringVar()
varSeason = StringVar()
varPaper = StringVar()
varVariant = StringVar()
varCompo = IntVar()
varCompoSelectAll = IntVar()

# components menu frame
compoFrame = Frame(leftFrame)
# components menu button
compoMenu = Menubutton(compoFrame, text="▼ Resource types", relief=RAISED)
compoMenu.menu = Menu(compoMenu, tearoff=0)
compoMenu["menu"] = compoMenu.menu
compoCheck = {}
# check box to select all
compoSelectAll = Checkbutton(compoFrame, variable=varCompoSelectAll, text='Select All')

# detect change of each menu
varLevel.trace('w', updateSubject)

varSubject.trace('w', updateSeason)
varYear.trace('w', updateSeason)

varSubject.trace('w', updatePaper)

varPaper.trace('w', updateVariant)
varSeason.trace('w', updateVariant)

varPaper.trace('w', updateCompo)
varSubject.trace('w', updateCompo)

varSubject.trace('w', updateYear)

# frame for menus
menuFrame = Frame(leftFrame)

drdLevel = OptionMenu(menuFrame, varLevel, *levelList.keys())
drdSubject = OptionMenu(menuFrame, varSubject, '')
drdYear = OptionMenu(menuFrame, varYear, '')
drdSeason = OptionMenu(menuFrame, varSeason, '')
drdPaper = OptionMenu(menuFrame, varPaper, '')
drdVariant = OptionMenu(menuFrame, varVariant, '')

# text to indicate menus
labelLevel = Label(menuFrame, text='Level', height=1)
labelSubject = Label(menuFrame, text='Subject', height=1)
labelYear = Label(menuFrame, text='Year', height=1)
labelSeason = Label(menuFrame, text='Season', height=1)
labelPaper = Label(menuFrame, text='Paper', height=1)
labelVariant = Label(menuFrame, text='Variant', height=1)

# buttons
addButton = Button(leftFrame, text='Add to list', command=addUrl, width=30)

deleteSectionFrame = Frame(rightFrame)
removeButton = Button(deleteSectionFrame, text='Remove selected', command=removeSelected, width=14)
clearButton = Button(deleteSectionFrame, text='Clear all', command=clearAll, width=14)

downButton = Button(root, text='DOWNLOAD!', command=download, width=50, height=2)

updateLatestButton = Button(root, text='Update Latest Information', command=updateLatestYear)

# use keyboard to delete
root.bind('<Delete>', removeSelected)

# list box frame
fileListFrame = Frame(rightFrame)
# file list box
fileListBox = Listbox(fileListFrame, width=30, height=8, selectmode=EXTENDED)
# listbox scroll bar
fileListScroll = Scrollbar(fileListFrame)
fileListBox.config(yscrollcommand=fileListScroll.set)
fileListScroll.config(command=fileListBox.yview)
# listbox title
fileListBoxTitle = Label(rightFrame, width=33, text='Download List:          \n(double click to open)', anchor='w')
# listbox double click to go to the url
fileListBox.bind('<Double-1>', goURL)

# browse save path
savePathFrame = Frame(rightFrame)
savePathLabel = Label(savePathFrame, text=showPath, width=27, height=1, relief=RIDGE)
browseButton = Button(savePathFrame, text='Browse...', command=pathFinder)
saveTitle = Label(savePathFrame, text='Save path:', anchor='w', width=27)

# title at the top
theTitle = Label(root, text='GCE Downloader', width=30, font=('Arial', 40, 'bold', 'underline'), cursor='hand2')
# trigger event when click the title to pop up copyright page
theTitle.bind('<Button-1>', popUpCR)

# frame for thread select
threadFrame = Frame(rightFrame)
# dropdown for number of threads
threadList = [1, 2, 3, 4, 5, 6, 7, 8]
varThread = IntVar()
drdThread = OptionMenu(threadFrame, varThread, *threadList)
varThread.set(defaultThread)
# label for thread
threadLabel = Label(threadFrame, text='enable multi-thread download\nMIGHT IMPACT PERFORMANCE')


def updateDefaultThread(*args):  # change default thread
    t = varThread.get()
    with open('resources/config.txt', 'r') as c:
        cList = c.readlines()
        cList[1] = 'defaultThread=' + str(t) + '\n'
    with open('resources/config.txt', 'w') as c:
        c.writelines(cList)
        c.close()


# monitor change of thread menu
varThread.trace('w', updateDefaultThread)

varLevel.set('iGCSE')
varYear.set(latestYear[0])

# placement of each menu
theTitle.grid(padx=5, pady=(15, 0), row=0, column=0, columnspan=3)

# left and right sections
leftFrame.grid(row=1, column=0)
rightFrame.grid(row=1, column=2)
midCanvas.grid(row=1, column=1)
midCanvas.create_line(2, 30, 2, 5000)
leftHolder.pack()
rightHolder.pack()

menuFrame.pack(padx=3, pady=(0, 3))

labelLevel.grid(padx=3, pady=(0, 3), column=0, row=0, sticky='e')
labelSubject.grid(padx=3, pady=3, column=0, row=1, sticky='e')
labelYear.grid(padx=3, pady=3, column=0, row=2, sticky='e')
labelSeason.grid(padx=3, pady=3, column=0, row=3, sticky='e')
labelPaper.grid(padx=3, pady=3, column=0, row=4, sticky='e')
labelVariant.grid(padx=3, pady=3, column=0, row=5, sticky='e')

drdLevel.grid(padx=3, pady=3, column=1, row=0, sticky='w')
drdSubject.grid(padx=3, pady=3, column=1, row=1, sticky='w')
drdYear.grid(padx=3, pady=3, column=1, row=2, sticky='w')
drdSeason.grid(padx=3, pady=3, column=1, row=3, sticky='w')
drdPaper.grid(padx=3, pady=3, column=1, row=4, sticky='w')
drdVariant.grid(padx=3, pady=3, column=1, row=5, sticky='w')

compoFrame.pack(padx=3, pady=3)
compoMenu.grid(padx=3, pady=3, column=0, row=0)
compoSelectAll.grid(padx=3, pady=3, column=1, row=0)

addButton.pack(padx=3, pady=3)

fileListBoxTitle.pack()

fileListFrame.pack(padx=3, pady=(0, 3))
fileListBox.grid(column=0, row=0)
fileListScroll.grid(column=1, row=0, sticky=tkinter.N + tkinter.S)

deleteSectionFrame.pack(padx=3, pady=3)
removeButton.grid(column=0, row=0, padx=3)
clearButton.grid(column=1, row=0, padx=3)

savePathFrame.pack(padx=3, pady=3)
saveTitle.grid(column=0, row=0)
savePathLabel.grid(column=0, row=1)
browseButton.grid(column=1, row=1)

threadFrame.pack()
threadLabel.grid(padx=3, pady=3, column=0, row=0)
drdThread.grid(padx=3, pady=3, column=1, row=0)

downButton.grid(padx=3, pady=(12, 3), row=2, column=0, columnspan=3)

updateLatestButton.grid(padx=3, pady=0, row=3, column=0, columnspan=3)

root.mainloop()
# done! :)
