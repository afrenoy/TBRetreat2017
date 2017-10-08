#!/usr/bin/env python3

import urllib.parse
import urllib.request
import sys

url = 'https://absynth.issb.genopole.fr/Bioinformatics/tools/EcoliTox/process.php'
molstruct = open(sys.argv[1], 'r').read()

postdata = urllib.parse.urlencode({'mol': molstruct}).encode()
result = urllib.request.urlopen(url, data=postdata).read()

print(result)

# Note: if necessary, we could have used the autentification cookie like this
#
#user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
#headers = { 'User-Agent' : user_agent, 'Cookie':'PHPSESSID=i2lcl1ooblvjqc3b3am94m3f67' }
#req = urllib.request.Request(url, data=postdata, headers=headers)
#result = urllib.request.urlopen(req).read()
