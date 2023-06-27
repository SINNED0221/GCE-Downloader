import tkinter
from tkinter import *
from tkinter import filedialog
import requests
import os.path
import threading
from datetime import date

with open('resources/config.txt', 'r') as c:
    exec(c.read())

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def findLatest(year, season):
    global count
    y = str(year)
    yy = str(y)[2:5]
    url = 'https://papers.gceguide.com/' + 'Cambridge%20IGCSE' + '/' + 'Physics%20(0625)' + '/' + y + '/' + \
          '0625' + '_' + season + yy + '_' + 'qp' + '_' + '1' + '2' + '.' + 'pdf'
    try:
        # download with requests
        res = requests.get(url, headers=headers, allow_redirects=True, stream=True, timeout=1)
        heads = requests.head(url)
        size = heads.headers["Content-Length"]  # testing if the file actually exist
    except KeyError:
        count += 1
    except requests.exceptions.RequestException:
        count += 10


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

if count == 0:
    latestYear = [currentYear, 'm', 's', 'w']
elif count == 1:
    latestYear = [currentYear, 'm', 's']
elif count == 2:
    latestYear = [currentYear, 'm']
elif count == 3:
    latestYear = [currentYear - 1, 'm', 's', 'w']
elif count == 4:
    latestYear = [currentYear - 1, 'm', 's']

if not count > 10:
    with open('resources/config.txt', 'r') as c:
        cList = c.readlines()
        cList[2] = 'latestYear=' + str(latestYear) + '\n'
    with open('resources/config.py', 'w') as c:
        c.writelines(cList)
        c.close()
