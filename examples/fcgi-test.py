#!/usr/bin/python
from flup.server import fcgi
from StringIO import StringIO
import sys,json,os,re
sys.path.append("/usr/lib/cgi-bin/silk");
os.environ["HTTP_HOST"]="FastCGI"
import silkapi

def app(environ, start_response):
	old_stdout = sys.stdout
	result = StringIO()
	sys.stdout = result
        a.setup_args(environ['wsgi.input'],None,"",environ)
        a.execute_query()
	result.seek(0)
	header=result.read(10)
	while header:
		header=header+result.read(10)
		hsplit=re.split(r'\r?\n\r?\n',header)
		if len(hsplit) == 2:
			htree=re.split(r'\r?\n',hsplit[0])
			headers=[tuple(x.split(": ",1)) for x in htree]
			start_response('200 OK', headers)
			header=None
	line=hsplit[1]
	if line == "":
		line=result.read(10)
	while line:
		yield(line)
		line=result.read(10)
	result.close()
        sys.stdout=old_stdout

#Faking HTTP_HOST environment for silkapi to think of this as HTTP Request
a=silkapi.SilkAPI()
#Fast CGI server can listen on port 4040
#In apache load module libapache2-mod-fastcgi and add the following line
##FastCgiServer /var/www/download/fcgi-test.py -processes 4 -port 4040
fcgi.WSGIServer(app, bindAddress = ('127.0.0.1',4040)).run()


