import urllib3.contrib.pyopenssl
import tkinter
from tkinter import filedialog
import requests


path = ""


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
    res = requests.get(url, headers=headers, allow_redirects=True, stream=True)
    heads = requests.head(url)
    try:  # testing if the file actually exist
        size = heads.headers["Content-Length"]
        open(path + '/' + fileName, "wb").write(res.content)
    except:
        print("File doesn't exist")
        return 0


pathFinder()
for year in range(2012, 2023):
    url = "https://cemc.uwaterloo.ca/contests/past_contests/"+str(year)+"/"+str(year)+"EuclidSolution.pdf"
    download(path, url)
    url = "https://cemc.uwaterloo.ca/contests/past_contests/" + str(year) + "/" + str(year) + "EuclidContest.pdf"
    download(path, url)

