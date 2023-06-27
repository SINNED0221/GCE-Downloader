import tkinter
from tkinter import *
from tkinter import filedialog
import requests
import os.path
import threading

with open('resources/config.py', 'r') as c:
    exec(c.read())

years=[y for y in range (1990,2023)]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def findYear(year):
    y=str(year)
    yy = str(y)[2:5]
    url = 'https://papers.gceguide.com/' + subject['level'] + '/' + subject['subject'] + '/' + y + '/' + \
          subject['code'] + '_' + 'w' + yy + '_' + 'qp' + '_' + '1' + '2' + '.' + 'pdf'
    try:
        # download with requests
        res = requests.get(url, headers=headers, allow_redirects=True, stream=True, timeout=5)
        heads = requests.head(url)
        size = heads.headers["Content-Length"]  # testing if the file actually exist
        return True
    except:
        pass

for k in alSubjectList.keys():
    subject=alSubjectList[k]
    temp=''
    for i in years:
        if findYear(i):
            temp=i
            break

    alSubjectList[k]=temp

print(alSubjectList)