import urllib3.contrib.pyopenssl
import tkinter
from tkinter import filedialog
import requests


path = "C:/Users/13931/Downloads"
url = "https://papers.gceguide.com/Cambridge%20IGCSE/Physics%20(0625)/2021/0625_m21_ms_12.pdf"


# pop up file explorer to select path
def pathFinder():
    global path
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askdirectory()


# assets for https compatibility
urllib3.contrib.pyopenssl.inject_into_urllib3()
requests.packages.urllib3.disable_warnings()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# downloading sequence
def download(path, url):
    global headers
    # fetch file name
    if url.find("/"):
        fileName = (url.rsplit('/', 1)[1])
    # download with requests
    heads = requests.head(url)
    print(heads)
    #size = heads.headers["Content-Length"]
    res = requests.get(url, headers=headers, allow_redirects=True, stream=True)
    heads = requests.head(url)
    open(path + '/' + fileName, "wb").write(res.content)



download(path, url)
