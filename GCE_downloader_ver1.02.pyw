import tkinter
from tkinter import *
from tkinter import filedialog
import requests
import os.path
import threading

# THIS PROGRAM IS (SOMEHOW) DEPENDENT ON urllib3 version 1.23 AS NEWER VERSIONS HAVE SOME BUGS

root = Tk()  # main window settings
root.title('GCE downloader gui')
root.iconbitmap('resources/icon.ico')
root.geometry('600x460')
root.resizable(height=True, width=True)

# TODO:Resizable windows with widgets resize accordingly
# TODO:Auto detect latest year

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

# read config file
with open('resources/config.py', 'r') as c:
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
    varSeason.set(seasons[0])
    menu = drdSeason['menu']
    menu.delete(0, 'end')  # clear menu box
    for season in seasons:  # add elements into menu box
        menu.add_command(label=season, command=lambda nation=season: varSeason.set(nation))


def updatePaper(*args):
    level = levelRedirect[varLevel.get()]  # list of all subjects
    subject = level[varSubject.get()]  # paper detail of the subject
    papers = subject['paper']  # list of papers
    varPaper.set(papers[0])
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
    yearList = sorted(allYearList, reverse=True)
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    name = subject['name']
    # for the subjects that has stopped or began recently, the previous or afterwards years are removed
    if name == 'Computer Science(9608)':
        yearList = [y for y in yearList if int(y) <= 2021]
    elif name == 'Computer Science(9618)':
        for y in yearList:
            yearList = [y for y in yearList if int(y) >= 2021]
    elif name == 'Psychology(9990)':
        for y in yearList:
            yearList = [y for y in yearList if int(y) >= 2018]
    else:
        pass

    yearList = sorted(yearList, reverse=False)
    varVariant.set(yearList[0])
    menu = drdYear['menu']
    menu.delete(0, 'end')
    for year in yearList:
        menu.add_command(label=year, command=lambda nation=year: varYear.set(nation))


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
    if len(path) > 27:
        showPath = path[0:12] + '...' + path[len(path) - 12:]
    else:
        showPath = path

    # edit default path into config.py
    with open('resources/config.py', 'r') as c:
        cList = c.readlines()
        cList[0] = 'defaultPath=' + '"' + path + '"' + '\n'
    with open('resources/config.py', 'w') as c:
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
    loadingPop.iconbitmap('resources/icon.ico')
    loadingPop.geometry('360x150')
    loadingPop.title('Downloading...')
    loadingPop.resizable(height=False, width=False)

    loadingPop.grab_set()  # prevent accessing main window during download
    downloadingLabel = Label(loadingPop, text='Downloading now, please wait...')
    downloadingLabel.place(relx=.5, rely=.5, anchor=CENTER)
    downloadingLabel.pack

    # download module
    def coreDownload():
        global fails
        total = len(urlList)
        fails = 0  # record number of fail downloads

        # button for quiting the completion pop up
        def quitCompletion():
            completionPop.destroy()

        def monoDownload(url):
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
            except:
                fails += 1

        # multi-thread download with threadN threads
        threadN = varThread.get()
        # divide urls into groups of each with threadN urls
        chunks = [urlList[i * threadN:(i + 1) * threadN] for i in range((len(urlList) + threadN - 1) // threadN)]
        for chunk in chunks:  # download with multi-thread
            threads = []
            for u in chunk:
                thread = threading.Thread(target=monoDownload, args=(u,))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()

        # download complete, remove old pop up and out pop up with results
        loadingPop.destroy()

        completionPop = Toplevel(root)
        completionPop.iconbitmap('resources/icon.ico')
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
    cRpop.iconbitmap('resources/icon.ico')
    cRpop.geometry('360x150')
    cRpop.title('Thanks for using!')
    cRpop.resizable(height=False, width=False)

    cRLabel = Label(cRpop,
                    text='GCE downloader developed by Dennis Zhang\n\nVersion 1.02\n\n©2022, All rights reserved')
    cRLabel.pack(pady=16)


# url and paper name and save path
urlList = []
downList = []
# get path from the config file
path = defaultPath
if len(path) > 27:
    showPath = path[0:12] + '...' + path[len(path) - 12:]
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
fileListBoxTitle = Label(rightFrame, width=33, text='Download List:', anchor='w')

# browse save path
savePathFrame = Frame(rightFrame)
savePathLabel = Label(savePathFrame, text=showPath, width=27, height=1, relief=RIDGE)
browseButton = Button(savePathFrame, text='Browse...', command=pathFinder)
saveTitle = Label(savePathFrame, text='Save path:', anchor='w', width=27)

# title at the top
theTitle = Label(root, text='GCE Downloader', width=30, font=('Arial', 20, 'bold', 'underline'), cursor='hand2')
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
    with open('resources/config.py', 'r') as c:
        cList = c.readlines()
        cList[1] = 'defaultThread=' + str(t) + '\n'
    with open('resources/config.py', 'w') as c:
        c.writelines(cList)
        c.close()


# monitor change of thread menu
varThread.trace('w', updateDefaultThread)

varLevel.set('iGCSE')
varYear.set('2021')

# placement of each menu
theTitle.grid(padx=5, pady=(15,0), row=0, column=0, columnspan=3)

# left and right sections
leftFrame.grid(row=1, column=0)
rightFrame.grid(row=1, column=2)
midCanvas.grid(row=1, column=1)
midCanvas.create_line(2, 30, 2, 5000)
leftHolder.pack()
rightHolder.pack()

menuFrame.pack(padx=3, pady=(0,3))

labelLevel.grid(padx=3, pady=(0,3), column=0, row=0, sticky='e')
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

fileListFrame.pack(padx=3, pady=(0,3))
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

downButton.grid(padx=3, pady=12, row=2, column=0, columnspan=3)

root.mainloop()
# done! :)
