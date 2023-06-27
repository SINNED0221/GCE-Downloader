import re
import urllib3.contrib.pyopenssl
import tkinter
from tkinter import filedialog
import requests

path = "C:/Users/13931/Downloads"
url = "https://papers.gceguide.com/Cambridge%20IGCSE/Physics%20(0625)/2021/0625_m21_ms_12.pdf"

# fetch file name
if url.find("/"):
    fileName = (url.rsplit('/', 1)[1])

urllib3.contrib.pyopenssl.inject_into_urllib3()
requests.packages.urllib3.disable_warnings()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def download(path, url):
    global headers
    r = requests.get(url, headers=headers, allow_redirects=True)
    open(path +'/'+ fileName, "wb").write(r.content)


download(path, url)
input('process complete')
