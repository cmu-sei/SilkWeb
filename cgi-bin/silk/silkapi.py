#!/usr/bin/python
""""
A simple CGI script to mimick rwfilter|rwcut type request over webservices

Supports:
Pagination (istart and iend variables)
Returns JSON, XML,CSV

Depends on:
Python SiLK libraries
Standard python libraries

Limitations:
Performance 

License:
See GPL license

Suggestions:
Use reverse proxy with mod_cache uses simple caching default 3days.

Author: Vijay Sarvepalli vss@cert.org
        Dwight Beaver dsbeaver@cert.org

SilkWeb
Copyright (c) 2016 Carnegie Mellon University.
All Rights Reserved.

NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN AS-IS BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.

Released under a BSD-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.  DM-0003718

This Software includes and/or makes use of the following Third-Party Software subject to its own license:
a.	jQuery : Copyright (c) 2016 jQuery Foundation (jquery.org/license)
b.	Bootstrap-table: Copyright (c) 2012-2016 Zhixin Wen wenzhixin2010@gmail.com (https://github.com/wenzhixin/bootstrap-table/blob/develop/LICENSE )
c.	D3 framework: Copyright 2010-2016 Mike Bostock (https://github.com/d3/d3/blob/master/LICENSE)

License.txt file:
SilkWeb
Copyright 2016 Carnegie Mellon University
All Rights Reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. SilkWeb includes and/or makes use of certain third party software ("Third Party Software"). You agree to comply with any and all the Third Party Software terms and conditions listed below and/or contained in any separate license file distributed with SilkWeb. The parties who own the Third Party Software ("Third Party Licensors") are intended third party beneficiaries to this License with respect to the terms applicable to their Third Party Software. Redistributions of source code must retain the above copyright notice, this list of conditions and the following acknowledgments and disclaimers.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following acknowledgments and disclaimers in the documentation and/or other materials provided with the distribution.
3. Products derived from this software may not include Carnegie Mellon University, "SEI and/or Software Engineering Institute" in the name of such derived product, nor shall Carnegie Mellon University, "SEI and/or Software Engineering Institute" be used to endorse or promote products derived from this software without prior written permission. For written permission, please contact permission@sei.cmu.edu.

ACKNOWLEDGMENTS AND DISCLAIMERS:
This material is based upon work funded and supported by the Department of Defense under Contract No. FA8721-05-C-0003 with Carnegie Mellon University for the operation of the Software Engineering Institute, a federally funded research and development center.

Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the United States Department of Defense.

NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN AS-IS BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.

[Distribution Statement A] This material has been approved for public release and unlimited distribution. Please see Copyright notice for non-US Government use and distribution.

CERTis a registered mark of Carnegie Mellon University.

THIRD PARTY SOFTWARE:
a.	jQuery :
The MIT License (MIT)

Copyright (c) 2016 jQuery Foundation

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
b.	Bootstrap-table :
(The MIT License)

Copyright (c) 2012-2016 Zhixin Wen <wenzhixin2010@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

c.	D3 framework :
Copyright 2010-2016 Mike Bostock
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the author nor the names of contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



"""

__appname__ = 'SilkAPI'
__version__ = "1.81"

import sys, re, silk, json, types, cgi, os, datetime, getopt, logging, imp, argparse, csv, warnings
from xml.etree.ElementTree import Element, tostring


try: # for python 3 compatibility check
    isinstance(1, long)
except:
    long=int 

def error_exit(errormsg, out_type="json"):
    if out_type == 'json':
        print('{"error": "' + errormsg.replace('"', '') + '"}')
    elif out_type == 'xml':
        print('<o><error><![CDATA[' + errormsg.replace("]]>", "") + "]]></error></o>")
    else:
        print("#ERROR:", errormsg)
    # print footer_print.get(out_type,"")
    sys.exit(255)


def fatal_exit(ex_cls, ex, tb):
    error_exit(str(ex))


def setupogging(logger, level=logging.CRITICAL, type='stdout', logfile=None,
                logformat="%(asctime)s - %(name)s - %(levelname)s - %(message)s"):
    """
    This function configures a logger
    :param logger: logging.getLogger() to be configured
    :return: stdout, syslog, or file logger
    """
    formatter = logging.Formatter(logformat)
    defout=sys.stdout
    if type.lower() == 'stderr':
        defout=sys.stderr
    if os.environ.get('HTTP_HOST', None): # always use stderr with webserver 
        defout=sys.stderr
    if type.lower() == 'file':  # Log to file
        handler = logging.FileHandler(logfile)
        handler.setFormatter(formatter)
    elif type.lower() == 'syslog':  # Log to syslog
        handler = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_DAEMON, address="/dev/log")
    else:  # Log to stdout
        handler = logging.StreamHandler(defout)
        handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(handler)
    return handler


def dict2xml(tag, d):
    """
    Convert python dictionary to xml
    :param tag:
    :param d:
    :return:
    """
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key.replace("/", ":"))  # For situations where we are using / as prefix like sip/24
        child.text = str(val)
        elem.append(child)
    return elem


def process_cmdline_args(args):
    """
    Function for parsing command line arguments
    :param args: input from the command line
    :return: dictionary of args for use with SilkAPI class
    """
    silk_args = {}
    for item in args:
        try:
            if '=' in item:
                key, value = item.split('=')
                key = key.replace('--', '')
                key = key.replace('-', '')
                silk_args[key] = value
            else:
                pass
        except:  # If the arguements aren't key=value, or aren't as expect just ignore them
            pass

    return silk_args


def print_version():
    """Print app version"""
    version = "{0} - version {1}".format(__appname__, __version__)
    print(version)


def helper(dvars, recvars):
    msg = ""
    for k in dvars:
        if k != "undefined":  # Silly Javascript undefined variable not needed in cli
            msg += "--" + k + "=  [default=" + str(dvars[k]) + "] "
    for f in recvars:
        msg += "--" + f + "=  [optional] "
    return msg


def mod_number_range(x, y, z):
    q = x.__getattribute__(y) - x.__getattribute__(y) % int(z)
    return str(q) + '-' + str(q + int(z) - 1)


def mod_datetime_range(x, y, z):
    q = int(x.__getattribute__(y).strftime("%s"))
    qf = q - q % int(z)
    fromtime = str(datetime.datetime.fromtimestamp(qf))
    totime = str(datetime.datetime.fromtimestamp(qf + int(z)))
    return fromtime + "-" + totime


def getformvalue(form, v):
    """
    :type form: cgi.FieldStorage
    """
    if isinstance(form.getvalue(v), list):
        return ",".join(form.getvalue(v))
    else:
        return form.getvalue(v)


def total_seconds(td): #  For those not having python 2.7
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / (10**6*1.0)

def get_site_config(): # Just send site configuration data back enumerating conditions
    site_config = {"classes": {}, "sensors": list(silk.site.sensors()), "default_class": silk.site.default_class()}
    for ctype in silk.site.classtypes():
        mclass = ctype[0]
        mtype = ctype[1]
        if not mclass in site_config["classes"]: #initiate a classes dict with "types" empty array and related sensors, default class
            site_config["classes"][mclass] = { "types" :[], "sensors" : list(silk.site.class_sensors(mclass)),
                                               "default_class" :list(silk.site.default_types(mclass))}
        site_config["classes"][mclass]["types"].append(mtype)
    return site_config


class SilkAPI:
    """
    """

    def __init__(self, args=None):
        self.program_args = {'maxrows': 1000, 'cachedays': 7, 'silkconf': "/data/silk.conf",
                             'logtype': 'stdout', 'loglevel': logging.WARNING}
        if os.environ.get("DEBUG", None):
            self.program_args['loglevel'] = logging.DEBUG
        self.loglevel = self.program_args['loglevel']
        self.logtype = self.program_args['logtype']
        self.silkconf = self.program_args['silkconf']
        self.maxrows = self.program_args['maxrows']
        if os.path.isfile("/etc/silkweb/silkwebconf.py"): # override program_args variables.
            exec(open("/etc/silkweb/silkwebconf.py").read())
        self.is_http_request = False  # Is this request a http request - assume it is CLI
        self.cachedays = 3  # cache the results for 3 days behind reverse proxy
        self.query_arguments = {'istart': 0, 'iend': 1000, 'out_type': 'json',
                                'sortby': 'bytes', 'stats': None,  # sortby=bytes is for what to sort by for stats
                                # this can be either bytes or packets or records
                                'undefined': ''}
        self.http_header = {"json": "Content-type: application/json\n",
                            'xml': "Content-type: text/xml\n", "csv": "Content-type: text/plain\n"}
        self.stats_fields = []
        self.default_silk_args = {}  # Default silk query arguments
        self.extra_silk_args = {}  # Extra silk query arguments
        self.valid_silk_args = {}
        self.stats_data = {}
        # For stats of default types we have lambda mapped methods to calculate.  Records are one per silk record
        # bytes and packets are automatically calculated. Any other field that user.
        self.stats_columns = {'bytes': lambda x: x.__getattribute__('bytes'),
                              'packets': lambda x: x.__getattribute__('packets'),
                              'records': lambda x: 1}
        self.stats_totals = {'bytes': 0, 'packets': 0, 'records': 0}
        self.group_by_functions = []  # These are the lmabda functions that perform group by
        self.silk_lambda_functions = {}
        self.version = __version__
        self.istart = 0
        self.iend = 1000
        self.args = {}
        self.logger = logging.getLogger('SilkAPI')
        self.handler = setupogging(self.logger, level=self.loglevel, type=self.logtype)
        self.rows_searched = 0
        self.timer = datetime.datetime.now()

        # Debug arguements checks
        self.logger.debug("default: {0}".format(self.default_silk_args))
        self.logger.debug("extra: {0}".format(self.extra_silk_args))
        self.logger.debug("valid: {0}".format(self.valid_silk_args))
        self.logger.debug("lambda: {0}".format(self.silk_lambda_functions))
        self.logger.debug("args: {0}".format(self.args))
        if os.environ.get("SILK_DATA_ROOTDIR", None):
            self.silkconf = os.environ["SILK_DATA_ROOTDIR"] + os.path.sep + "silk.conf"
        if os.environ.get("SILK_CONFIG_FILE", None): #override when SILK_CONFIG_FILE is also present
            self.silkconf = os.environ["SILK_CONFIG_FILE"]


        if os.path.isfile(self.silkconf) == False or silk.site.init_site(siteconf=self.silkconf) == False:
            if os.environ.get('HTTP_HOST', None):  # push headers before putting error out for HTTP sessions
                form = cgi.FieldStorage()
                if "out_type" in form:
                    self.query_arguments["out_type"] = getformvalue(form, "out_type")
                else:
                    self.query_arguments["out_type"] = "json"
                print(self.http_header.get(self.query_arguments["out_type"], "Content-type: text/plain\n"))
            error_exit("Error could not load silk.conf at " + self.silkconf +
                       ", update environment variable if needed SILK_DATA_ROOTDIR", self.query_arguments["out_type"])
            sys.exit(2)

    def setup_args(self, *args):
        """
        This method processes arguments and puts them class members.  It can handle arguments passed to the constructor
        and arguments passed through an HTTP_POST or through CLI arguments
        Currently classtypes is not supported, when supported a tuple like 
        ((class1,type1),(class2,type2)) may be provided instead of classname and types distinctly
        """


        self.default_silk_args = {'classname': str(silk.site.default_class()),
                                  'types': silk.site.default_types(silk.site.default_class()),
                                  'sensors': silk.site.class_sensors(silk.site.default_class()),
                                  'start': datetime.date.today().strftime('%Y/%m/%d:00'),
                                  'end': datetime.date.today().strftime('%Y/%m/%d:01')}
        self.valid_silk_args = self.return_valid_silk_args()

        # Process arguments from an HTTP_POST or HTTP_GET
        # HTTP_POST arguments can only update default_silk_args, query_arguments, and extra_silk_arguements
        # HTTP_POSTs cannot update program_args
        if os.environ.get('HTTP_HOST', None):
            self.is_http_request = True
            form = cgi.FieldStorage(*args)
            for v in form:
                if v in self.default_silk_args:
                    self.default_silk_args[v] = getformvalue(form, v)
                elif v in self.query_arguments:
                    self.query_arguments[v] = getformvalue(form, v)
                else:
                    self.extra_silk_args[v] = getformvalue(form, v)
            time_format = "%a, %d %b %Y %H:%M:%S %Z"
            print("Expires: %s" % (
                (datetime.datetime.now() + datetime.timedelta(days=self.cachedays)).strftime(time_format)))
            print("Date: %s" % (datetime.datetime.now().strftime(time_format)))
            print(self.http_header.get(self.query_arguments['out_type'], "Content-type: text/plain\n"))
        else:  # Assume CLI operations
            parg = argparse.ArgumentParser(description="silkweb parser",
                                           usage=helper(self.default_silk_args, self.valid_silk_args))
            uargs, addon = parg.parse_known_args()
            cform = {}
            i = 0
            while i < len(addon):
                addon[i] = re.sub(r'^\-+', '', addon[i])
                x = addon[i].split('=')
                if x[0] in ["v","version"]: 
                    print_version() # Just print version and exit
                    sys.exit(0)                        
                if len(x) > 1:
                    cform[x[0]] = "".join(x[1:])
                    i += 1
                else:
                    cform[addon[i]] = addon[i + 1]
                    i += 2
            for v in cform:
                if v in self.default_silk_args:
                    self.default_silk_args[v] = cform[v]
                elif v in self.query_arguments:
                    self.query_arguments[v] = cform[v]
                else:
                    self.extra_silk_args[v] = cform[v]
        if "site_config" in self.extra_silk_args:
            print(json.dumps(get_site_config()))
            sys.exit(0)
        # Updates types if classname is specified and types is NOT specified
        if self.default_silk_args['classname'] != str(silk.site.default_class()):
            if self.default_silk_args['types'] == silk.site.default_types(silk.site.default_class()):
                self.default_silk_args['types'] = silk.site.default_types(self.default_silk_args['classname'])
            if self.default_silk_args['sensors'] == silk.site.class_sensors(silk.site.default_class()):
                self.default_silk_args['sensors'] = silk.site.class_sensors(self.default_silk_args['classname'])

        # Remap legacy arguments 
        for legacy in ["start_date", "end_date"]:
            if legacy in self.extra_silk_args.keys():
                self.default_silk_args[legacy.replace("_date", "")] = self.extra_silk_args[legacy]
                self.extra_silk_args.pop(legacy)
        for converter in ["types", "sensors"]:  # These ought to be list something iterable for pysilk to use
            if isinstance(self.default_silk_args[converter], str):
                if self.default_silk_args[converter].startswith("!"):
                    allvars={} # A dictionary of all types and all sensors
                    allvars['types'] = set(silk.site.types("all"))
                    allvars['sensors'] = set(silk.site.sensors())
                    notvars = set(self.default_silk_args[converter].replace("!","").split(","))
                    #Set difference or relative compliment of these two sets will give the sets we want to search
                    self.default_silk_args[converter] = list(allvars[converter]-notvars)
                else:
                    self.default_silk_args[converter] = self.default_silk_args[converter].split(",")

        # Validate arguments and throw error

        for key in self.extra_silk_args.keys():
            if key not in self.valid_silk_args:
                error_exit("Some variable you provided are not recoginized " + str(key) + " : " + str(self.extra_silk_args[key]))
        if self.query_arguments['sortby'] not in self.stats_columns and self.query_arguments['sortby'] != "time":  #
            error_exit("Provided query argument for sortby to sort by should be either bytes or packets or records, "
                       "invalid argument provided " + self.query_arguments['sortby'])

        # Generate processing functions for valid silk args
        self.generate_record_lambda()

        # Combined Default and Specific arguments
        self.args = self.default_silk_args.copy()
        self.args.update(self.extra_silk_args)
        self.args.update(self.query_arguments)

        # Start/End for pagenation
        self.istart = int(self.args['istart'])
        self.iend = int(self.args['iend'])

        # Configure stats options

        if self.args['stats']:
            self.stats_fields = self.args['stats'].split(',')
            for field in self.stats_fields:
                fieldx = field.split("/")
                self.group_by_functions.append(self.create_lambda_group_by(field, silk.RWRec()))
                if fieldx[0] not in self.valid_silk_args:
                    error_exit(
                        "Fields given for stats is not valid should be one of the silk columns, invalid field is : " +
                        field)
        self.rows_searched=0

    @staticmethod
    def return_valid_silk_args():
        """  :return: list of valid silk arguments  """
        valid = []
        [valid.append(r) for r in dir(silk.RWRec())
         if not r.startswith('_')
         and not r.startswith('to_')
         and not r.startswith('as_')
         and not r.startswith('is_')]
        return valid

    def number_logic_to_lambda(self, invar, switch):
        """
    This subroutine does check the request to be either a range query or a comma delimited
    list query and does comparision.  If the requested match is neither range nor a delimited
    list, then the invar is sent back converted to integer.  Even floating point will be treated
    as integer. No float matches are done.
    If requested match is a range or a list, the matched item is sent back instead of invar!
        """
        z = invar.split('-')  # range queries
        if len(z) == 1:
            y = map(int, invar.split(','))  # multiple conditions
            if len(y) == 1:  # a single match
                return lambda x: (x == int(y[0])) ^ switch
            else:  # This is a comma delimited convert to list and send match condition back
                return lambda x: (x in y) ^ switch
        elif len(z) == 2:  # This is a query with "-"
            if z[1] == '':  # This is a greater than query
                return lambda x: (int(z[0]) <= x) ^ switch
            elif z[0] == '':  # This is a less than query
                return lambda x: (int(z[0]) >= x) ^ switch
            else:  # This is range query
                return lambda x: (int(z[0]) <= x <= int(z[1])) ^ switch

    def generate_record_lambda(self):
        """
        """
        temprec = silk.RWRec()
        for key in self.extra_silk_args:
            value = self.extra_silk_args[key]
            switcharoo = False
            if value.startswith("!"):
                value = value.replace("!", "")
                switcharoo = True
            if key not in self.valid_silk_args:
                error_exit("Some of the options you provided are not valid " + key + ":" + value)
            cattr = temprec.__getattribute__(key)
            self.silk_lambda_functions[key] = lambda x, y=value, z=switcharoo: (str(x) == y) ^ z
            if isinstance(cattr, silk.IPv4Addr):  # change it IPv4wildcard
                ipset = silk.IPSet(map(silk.IPWildcard, value.split(",")))
                self.silk_lambda_functions[key] = lambda x, y=ipset, z=switcharoo: (x in y) ^ z
            if isinstance(cattr, int):  # the next three treat them as numeric - number(s),ranges
                self.silk_lambda_functions[key] = self.number_logic_to_lambda(invar=value, switch=switcharoo)
            elif isinstance(cattr, float):  # float is also treated like a number
                self.silk_lambda_functions[key] = self.number_logic_to_lambda(invar=value, switch=switcharoo)
            elif isinstance(cattr, long):  # long is also treated numeric
                self.silk_lambda_functions[key] = self.number_logic_to_lambda(invar=value, switch=switcharoo)
            elif isinstance(cattr, tuple):  # Tuples can be converted to set for set intersection
                self.silk_lambda_functions[key] = lambda x, y=value, z=switcharoo: (set(y.split(",")).issubset(
                    set(x))) ^ z


    def create_lambda_group_by(self, tvar, samplerec):
        tvars = tvar.split("/")
        if len(tvars) == 1:  # No "/" found a simple send the right attribute
            return lambda x, y=tvars[0]: x.__getattribute__(y)
        cattr = samplerec.__getattribute__(tvars[0])
        if isinstance(cattr, silk.IPv4Addr):  # change it IPv4 subnet address mask
            return lambda x, y=tvars[0], z=tvars[1]: str(x.__getattribute__(y).mask_prefix(int(z))) + '/' + z
        if isinstance(cattr, int):  # the next three treat them as numeric - number(s),ranges
            return lambda x, y=tvars[0], z=tvars[1]: mod_number_range(x, y, z)
        elif isinstance(cattr, float):  # float is also treated like a number
            return lambda x, y=tvars[0], z=tvars[1]: mod_number_range(x, y, z)
        elif isinstance(cattr, long):  # long is also treated numeric
            return lambda x, y=tvars[0], z=tvars[1]: mod_number_range(x, y, z)
        elif isinstance(cattr, datetime.datetime):  # long is also treated numeric
            return lambda x, y=tvars[0], z=tvars[1]: mod_datetime_range(x, y, z)
        else:  # We cannot support group by functions on other columns of the record
            error_exit("Group by functions not supported for this variable " + tvar)

    def check_condition(self, rec):
        """
        :param rec:
        :return:
        """
        for key in self.silk_lambda_functions:
            if not self.silk_lambda_functions[key](rec.__getattribute__(key)):
                return False
        return True

    def recmapper(self, rec):
        """
        :param rec:
        :return:
        """
        rdata = {}
        for f in self.valid_silk_args:
            rdata[f] = rec.__getattribute__(f)
        return rdata

    def statsmapper(self, rec, funcs):
        values = []

        for f in funcs:
            values.append(str(f(rec)))

        key = ','.join(map(str, values))

        self.stats_data[key] = self.stats_data.get(key, {})
        for statscol in self.stats_columns.keys():
            xvar = self.stats_columns[statscol](rec)
            self.stats_data[key][statscol] = self.stats_data[key].get(statscol, 0) + xvar
            self.stats_totals[statscol]+= xvar #This will be used to calculate stats total.

    def format_stats(self):
        if self.iend - self.istart > self.maxrows:
            error_exit({"error": "Maximum rows allowed in a query is " + str(self.maxrows)})

        # keys = sorted(self.stats_data, key=self.stats_data.get, reverse=True)[:self.iend]
        sortcolumn = self.query_arguments['sortby']
        if self.query_arguments['sortby'] == "time":  # If it is sort by time then sort by keys of dictionary
            keys = list(sorted(self.stats_data.items(), key=lambda x: x[0], reverse=True))
        else:
            keys = list(sorted(self.stats_data.items(), key=lambda x: x[1][sortcolumn], reverse=True))
        # Now destory this dictionary to save some memory
        self.stats_data.clear()
        row = 1
        results = []
        for k in keys:
            record = dict(zip(self.stats_fields, k[0].split(',')))
            for statscol in self.stats_columns.keys():
                record[statscol] = k[1][statscol]
            record['rowid'] = row
            results.append(record)
            row += 1
        self.stats_totals["length"]=len(results) # we know the end of this stats
        return results[self.istart:self.iend]

    def stats_query(self):
        """
        Method executes a silk query that returns stats (rwfilter | rwstats)
        :returns: dictionary containing results
        """
        for filename in silk.site.repository_iter(**self.default_silk_args):
            for rec in silk.silkfile_open(filename, silk.READ):
                self.rows_searched += 1
                if self.check_condition(rec):
                    self.statsmapper(rec, self.group_by_functions)

        return self.format_stats()

    def record_query(self):
        """
        Function executes a silk query that returns records. (rwfilter query)
        :returns: List of dictionaries containing results
        """

        if self.iend - self.istart > self.maxrows:
            return {"error": "Maximum rows allowed in a query is " + str(self.maxrows)}

        row = 0
        results = []
        for filename in silk.site.repository_iter(**self.default_silk_args):
            for rec in silk.silkfile_open(filename, silk.READ):
                self.rows_searched += 1
                if self.check_condition(rec):
                    data = self.recmapper(rec);
                    row += 1
                    if self.istart <= row <= self.iend:
                        data.update({"rowid": row})
                        results.append(data)
                    if row > self.iend:
                        return results
        self.rows_searched += 1
        return results

    def return_results_header(self):
        """ Returns basic header containing version and timestamp """
        xheader = {}
        xheader['version'] = self.version
        xheader['timestamp'] = datetime.datetime.now().strftime("%s")
        return xheader

    def print_results(self):
        """
        Function determines the query type, executes the query, and converts the resulting data to the specified
        output type
        :returns: results string in the format specified by self.default_silk_args[out_type]
        """
        if self.args['stats']:
            data = self.stats_query()
        else:
            data = self.record_query()
        timetoexecute = datetime.datetime.now() - self.timer
        xheader = self.return_results_header()
        xheader['time_execution'] = str(total_seconds(timetoexecute)) + " seconds"
        print_args = self.args
        print_args.pop("undefined")  # annoying javascript undefined variable
        if self.args['out_type'] == 'json':
            xresults = {"header": xheader, "query_conditions": print_args, "stats_totals": self.stats_totals,
                        "gdata": data, "rows": str(len(data)), "rows_searched": self.rows_searched}
            print(json.dumps(xresults, default=str))
        elif self.args['out_type'] == 'xml':
            print('<?xml version="1.0" encoding="UTF-8"?>')
            print('<o>')
            print(tostring(dict2xml('header', xheader)))
            print(tostring(dict2xml('query_conditions', print_args)))
            print('<gdata class="array">')
            for xdata in data:
                print(tostring(dict2xml('record', xdata)))
            print("</gdata>")
            print(tostring(dict2xml('stats_totals',self.stats_totals)))
            print("<rows>" + str(len(data)) + "</rows>")
            print("<rows_searched>" + str(self.rows_searched) + "</rows_searched>")
            print('</o>')
        elif self.args['out_type'] == 'csv':
            print(cgi.escape("#" + ", ".join(["=".join([key, str(val)]) for key, val in print_args.items()]),
                             ", ".join(["=".join([key, str(val)]) for key, val in xheader.items()])))
            if self.args['stats']:
                csvwriter = csv.DictWriter(sys.stdout, fieldnames=data[0].keys() + ['rowid'])
                print(",".join(data[0].keys() + ['rowid']))
            else:
                csvwriter = csv.DictWriter(sys.stdout, fieldnames=self.valid_silk_args + ['rowid'])
                print(",".join(self.valid_silk_args + ['rowid']))
            for xdata in data:
                csvwriter.writerow(xdata)

    def execute_query(self):
        """
        Entry point into the SilkAPI class for executing queries. Function will determine if a
        request is from an HTTP_POST and will apply the appropriate header.
        Supports basic timing for performance monitoring
        :returns: results string in the format specified by self.default_silk_args[out_type] with appropriate headers
        """

        if self.loglevel == logging.DEBUG:
            timer = datetime.datetime.now()
            self.print_results()
            elapsed_time = datetime.datetime.now() - timer
            self.logger.debug("Query: {0}: executed in {1}s".format(str(self.args), str(elapsed_time)))
        else:
            self.print_results()


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    sys.excepthook = fatal_exit
    silkq = SilkAPI()
    #to execute this in fastCGI or WSGI run setup_args with CGI variable for cgi.FieldStorage(*args) to inherit
    silkq.setup_args(None)
    # Execute and display the data
    silkq.execute_query()
