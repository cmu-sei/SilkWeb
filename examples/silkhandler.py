#! /usr/bin/python
import scgi
import scgi.scgi_server
import sys,json,os,cgi
os.environ["HTTP_HOST"]="SCGI"
os.environ["SILK_DATA_ROOTDIR"]="/data/silk/"
sys.path.append("/usr/lib/cgi-bin/silk")
import silkapi

class SiLKHandler(scgi.scgi_server.SCGIHandler):
    def produce(self, env, bodysize, inputx, outfile):
        xdtout=sys.stdout
        sys.stdout=outfile
        os.environ["HTTP_HOST"]="HELLO";
        a.iend=10
        a.args.update({'iend':10})
        a.setup_args(inputx,None,"",env)
        a.execute_query()
        outfile.write(json.dumps(a.args))
        outfile.write(json.dumps(env))
        sys.stdout=xdtout

# Main program: create an SCGIServer object to
# listen on port 4000.  We tell the SCGIServer the
# handler class that implements our application.
a=silkapi.SilkAPI()
server = scgi.scgi_server.SCGIServer(
    handler_class=SiLKHandler,
    port=4000
    )
# Tell our SCGIServer to start servicing requests.
# This loops forever.
server.serve()
#Apache config looks like
#<Location "/scgitest">
#    SCGIHandler On
#</Location>
#SCGIMount /scgitest 127.0.0.1:4000
