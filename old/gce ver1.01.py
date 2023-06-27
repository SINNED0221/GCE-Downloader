import urllib3.contrib.pyopenssl
import tkinter
from tkinter import *
from tkinter import filedialog
import requests
import os.path
import threading

root = Tk()
root.title('GCE downloader gui')
root.iconbitmap('resources/icon.ico')
root.geometry('360x720')
root.resizable(height=True, width=False)

# assets for https compatibility
urllib3.contrib.pyopenssl.inject_into_urllib3()
requests.packages.urllib3.disable_warnings()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def updateSubject(*args):
    subs = levelList[varLevel.get()]
    varSubject.set(subs[0])
    menu = drdSubject['menu']
    menu.delete(0, 'end')
    for sub in subs:
        menu.add_command(label=sub, command=lambda nation=sub: varSubject.set(nation))


def updateSeason(*args):
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    titles = list(subject.keys())
    lastI = len(titles)
    seasons = titles[5:lastI - 1]
    varSeason.set(seasons[0])
    menu = drdSeason['menu']
    menu.delete(0, 'end')
    for season in seasons:
        menu.add_command(label=season, command=lambda nation=season: varSeason.set(nation))


def updatePaper(*args):
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    papers = subject['paper']
    varPaper.set(papers[0])
    menu = drdPaper['menu']
    menu.delete(0, 'end')
    for paper in papers:
        menu.add_command(label=paper, command=lambda nation=paper: varPaper.set(nation))


def updateVariant(*args):
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    variants = subject[varSeason.get()]
    varVariant.set(variants[0])
    menu = drdVariant['menu']
    menu.delete(0, 'end')
    for variant in variants:
        menu.add_command(label=variant, command=lambda nation=variant: varVariant.set(nation))


def updateCompo(*args):
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    composs = subject['components']
    compos = composs.keys()
    for compo in compos:
        varCompo = IntVar()
        compoMenu.menu.add_checkbutton(label=compo, variable=varCompo)
        compoCheck[compo] = varCompo


def addUrl():
    level = levelRedirect[varLevel.get()]
    subject = level[varSubject.get()]
    year = varYear.get()
    yy = year[2:]
    season = varSeason.get()
    paper = varPaper.get()
    variant = varVariant.get()
    checks = [(name, varCompo.get()) for name, varCompo in compoCheck.items()]
    for (i, b) in checks:
        if b == 1:
            compo = i
            fileFormat = subject['components'][compo]
            url = 'https://papers.gceguide.com/' + subject['level'] + '/' + subject['subject'] + '/' + year + '/' + \
                  subject['code'] + '_' + season + yy + '_' + compo + '_' + paper + variant + '.' + fileFormat
            fileName = subject['code'] + '_' + season + yy + '_' + compo + '_' + paper + variant + '.' + fileFormat
            urlList.append(url)
            downList.append(fileName)
    fileListBox.delete(0, END)
    fileListBox.insert(END, *downList)


def removeLast():
    try:
        del urlList[-1]
        del downList[-1]
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
    if len(path) > 27:
        showPath = path[0:13] + '...' + path[len(path) - 13:]
    else:
        showPath = path
    savePathLabel['text'] = showPath


def download():
    if os.path.exists(path):
        pass
    else:
        pathFinder()

    # top levels to show state
    loadingPop = Toplevel(root)
    loadingPop.geometry('360x150')
    loadingPop.title('Downloading...')
    loadingPop.resizable(height=False, width=False)

    loadingPop.grab_set()  # prevent accessing main window during download
    downloadingLabel = Label(loadingPop, text='Downloading now, please wait...')
    downloadingLabel.place(relx=.5, rely=.5, anchor=CENTER)
    downloadingLabel.pack

    # download module
    def coreDownload():
        # button for quiting the completion pop up
        def quitCompletion():
            completionPop.destroy()

        total = len(urlList)
        fails = 0

        def monoDownload(url):
            # fetch file name
            if url.find("/"):
                fileName = (url.rsplit('/', 1)[1])
            # download with requests
            res = requests.get(url, headers=headers, allow_redirects=True, stream=True)
            heads = requests.head(url)
            try:  # testing if the file actually exist
                size = heads.headers["Content-Length"]
                open(path + '/' + fileName, "wb").write(res.content)
            except:
                fails += 1

        # download complete, remove old pop up and out pop up with results
        loadingPop.destroy()

        completionPop = Toplevel(root)
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


# record for paper detail
igCS = {}
igPhysics = {'name': 'Physics',
             'level': 'Cambridge%20IGCSE',
             'subject': 'Physics%20(0625)',
             'code': '0625',
             'paper': [1, 2, 3, 4, 5, 6],
             'm': [2],
             's': [1, 2, 3],
             'w': [1, 2, 3],
             'components': {'qp': 'pdf', 'ms': 'pdf'}}
alPhysics = {}
alChemistry = {}

levelList = {'iGCSE': ['Physics', 'Computer Science'],
             'AS/ALevel': ['Physics', 'Chemistry']}
yearList = ['2017', '2018', '2019', '2020', '2021']
igSubjectList = {'Physics': igPhysics, 'Computer Science': igCS}
alSubjectList = {'Physics': alPhysics, 'Chemistry': alChemistry}
levelRedirect = {'iGCSE': igSubjectList, 'AS/ALevel': alSubjectList}

# url and paper name and save path
urlList = []
downList = []
path = ''
showPath = ''

# variables of each menu
varLevel = StringVar()
varSubject = StringVar()
varYear = StringVar()
varSeason = StringVar()
varPaper = StringVar()
varVariant = StringVar()
varCompo = IntVar()

# components menu button
compoMenu = Menubutton(root, text="▼ Resource types", relief=RAISED)
compoMenu.menu = Menu(compoMenu, tearoff=0)
compoMenu["menu"] = compoMenu.menu
compoCheck = {}

# detect change of each menu
varLevel.trace('w', updateSubject)
varSubject.trace('w', updateSeason)
varSubject.trace('w', updatePaper)
varSeason.trace('w', updateVariant)
varSubject.trace('w', updateCompo)

# frame for menus
menuFrame = Frame(root)

drdLevel = OptionMenu(menuFrame, varLevel, *levelList.keys())
drdSubject = OptionMenu(menuFrame, varSubject, '')
drdYear = OptionMenu(menuFrame, varYear, *yearList)
drdSeason = OptionMenu(menuFrame, varSeason, '')
drdPaper = OptionMenu(menuFrame, varPaper, '')
drdVariant = OptionMenu(menuFrame, varVariant, '')

labelLevel = Label(menuFrame, text='Level', height=1)
labelSubject = Label(menuFrame, text='Subject', height=1)
labelYear = Label(menuFrame, text='Year', height=1)
labelSeason = Label(menuFrame, text='Season', height=1)
labelPaper = Label(menuFrame, text='Paper', height=1)
labelVariant = Label(menuFrame, text='Variant', height=1)

# buttons
addButton = Button(root, text='Add to list', command=addUrl, width=30)

deleteSectionFrame = Frame(root)
removeButton = Button(deleteSectionFrame, text='Remove last item', command=removeLast, width=14)
clearButton = Button(deleteSectionFrame, text='Clear all items', command=clearAll, width=14)

downButton = Button(root, text='DOWNLOAD!', command=download, width=30, height=3)

# list box frame
fileListFrame = Frame(root)
# file list box
fileListBox = Listbox(fileListFrame, width=30, height=9)
# listbox scroll bar
fileListScroll = Scrollbar(fileListFrame)
fileListBox.config(yscrollcommand=fileListScroll.set)
fileListScroll.config(command=fileListBox.yview)

# browse save path
savePathFrame = Frame(root)
savePathLabel = Label(savePathFrame, text=showPath, width=30, height=1, relief=RIDGE)
browseButton = Button(savePathFrame, text='Browse...', command=pathFinder)
saveTitle = Label(savePathFrame, text='Save path:', anchor='w', width=30)

# title at the top
theTitle = Label(root, text='GCE Downloader', width=30, font=('Arial', 20, 'bold'))

varLevel.set('iGCSE')
varYear.set('2021')

# placement of each menu
theTitle.pack(padx=5, pady=7)

menuFrame.pack(padx=3, pady=3)

labelLevel.grid(padx=3, pady=3, column=0, row=0, sticky='e')
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

compoMenu.pack(padx=3, pady=3)

addButton.pack(padx=3, pady=3)

deleteSectionFrame.pack(padx=3, pady=3)
removeButton.grid(column=0, row=0, padx=3)
clearButton.grid(column=1, row=0, padx=3)

fileListFrame.pack(padx=3, pady=3)
fileListBox.grid(column=0, row=0)
fileListScroll.grid(column=1, row=0, sticky=tkinter.N + tkinter.S)

savePathFrame.pack(padx=3, pady=3)
saveTitle.grid(column=0, row=0)
savePathLabel.grid(column=0, row=1)
browseButton.grid(column=1, row=1)

downButton.pack(padx=3, pady=3)

root.mainloop()
