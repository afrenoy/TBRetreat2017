#!/usr/bin/env python3

import urllib.request
import re
from bs4 import BeautifulSoup
import os

url = 'http://www.nature.com/nature/archive/index.html?year='
url = url + '2016'

html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

allblocks = soup('li', {'class': re.compile('odd|even')})
allissues = []

for block in allblocks:
    allissues.extend(block('a'))

for issue in allissues:
    url_issue = 'http://www.nature.com' + issue['href']
    if '_supp' in url_issue:
        continue
    html_issue = urllib.request.urlopen(url_issue).read()
    soup_issue = BeautifulSoup(html_issue, 'html.parser')
    articles = soup_issue('div', {'id': 'af'})[0]
    letters = soup_issue('div', {'id': 'lt'})[0]
    for item in articles('article')+letters('article'):
        url_item = 'http://www.nature.com' + item('a')[0]['href']
        pdflink = url_item.replace('full', 'pdf').replace('html', 'pdf')
        os.system('wget ' + pdflink)
