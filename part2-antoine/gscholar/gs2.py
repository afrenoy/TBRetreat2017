#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import sys

url = sys.argv[1]
start = 0

csv = False
if len(sys.argv) > 2 and 'csv' in sys.argv[2]:
    csv = True

while True:
    url_full = url + '&cstart=%d&pagesize=100' % start
    html = urllib.request.urlopen(url_full).read()
    soup = BeautifulSoup(html, 'html.parser')
    listpub = soup('tr', {'class': 'gsc_a_tr'})

    for publine in listpub:
        title = publine('td', {'class': 'gsc_a_t'})[0]('a')[0].get_text().replace(';', '')
        ncite = publine('td', {'class': 'gsc_a_c'})[0]('a')[0].get_text()
        if not ncite:
            ncite = 0
        else:
            ncite = int(ncite)
        if csv:
            print('%s;%d' % (title, ncite))
        else:
            print('article "%s"; cited %d times' % (title, ncite))

    if len(listpub) < 100:
        break
    start = start + 100
