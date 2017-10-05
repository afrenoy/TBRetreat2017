#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import sys

url = sys.argv[1]
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

for publine in soup('tr', {'class': 'gsc_a_tr'}):
    title = publine('td', {'class': 'gsc_a_t'})[0]('a')[0].get_text()
    ncite = publine('td', {'class': 'gsc_a_c'})[0]('a')[0].get_text()
    if not ncite:
        ncite = 0
    else:
        ncite = int(ncite)
    print('article "%s"; cited %d times' % (title, ncite))
