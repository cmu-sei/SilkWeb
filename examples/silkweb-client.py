#!/bin/env python
import argparse,re,urllib2
def helper():
    return """ Use with --url to the SilkWeb URL base and pass parameters as arguments
           Example: silkweb-client.py --url=http://silkweb/cgi-bin/silk/silkapi.py --protocol=6 --dport=80 
           See silkweb documentation https://github.com/cmu-sei/SilkWeb/ """

parg = argparse.ArgumentParser(description="silkweb client parser",
                               usage=helper())
uargs, addon = parg.parse_known_args()
cform = {}
i = 0
urlargs = ""
url = "http://localhost/cgi-bin/silk/silkapi.py?"
proxy = ""
proxydict = {}
while i < len(addon):
    addon[i] = re.sub(r'^\-+', '', addon[i])
    x = addon[i].split('=')
    if x[0] == 'url':
        url = x[1]+"?"
    else:
        urlargs += addon[i] + "&"
    i = i + 1
req = urllib2.urlopen(url+urlargs)
print(req.read())


