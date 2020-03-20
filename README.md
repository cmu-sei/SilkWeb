# silkweb - include SBOM SWID tags format
A web services API for SiLK tools
The intent of this silkweb API service is to enable a simplified JSON/XML/CSV exporter that will
use minimal python libraries and Python Silk libraries https://tools.netsa.cert.org/silk/pysilk.html to
mimick SiLK tools like rwfilter and rwstats type of tools using a pure python API.

Dependency:
Build Silk tools with python support

Designed with Apache or NGINX with CGI in mind.  The scrips sits on server and exports
local Silk repository over webservices.

Directory structure
/var/www
	/cgi-bin/silk/silkapi.py (executable chmod 655)
	/html/silk/* (html and Javascript components)
	[For Ubuntu you may need to put cgi-bin/silk to /usr/lib/cgi-bin]
/etc
    /httpd/conf.d/silkweb.conf (If your silk environment variable needs to be different from default /data/silk.conf)
    /silkweb/silkwebconf.py (If you want to overiride tings like max rows returned to the user from 1000 to something else

The file silkweb.conf should be edited your SiLK install has default configuration file not in /data/silk.conf but other 
You can also set some special configuration as environment variables needed for silk python to work properly.

Apache/NGINX user should have read only access to Silk repos

Debug HTML/JS/CSS issues using Developer mode on Chrome/Firefox/IE/Safari

Examples:
Basic search:
http://testlab/cgi-bin/silk/silkapi.py?out_type=json&start_date=2015/07/20:00&end_date=2015/07/20:01&istart=0&iend=1000
SIP Search:
http://testlab/cgi-bin/silk/silkapi.py?out_type=json&sip=10.64.22.0/23&start_date=2015/07/20:00&end_date=2015/07/20:01&istart=0&iend=1000
Top 10 rwstats with sip,dip:
http://testlab/cgi-bin/silk/silkapi.py?out_type=json&sip=10.64.22.0/23&values=bytes&stats=sip,dip&start_date=2015/07/20:00&end_date=2015/07/20:01&istart=0&iend=10
Same as above with packets 4 or more:
http://testlab/cgi-bin/silk/silkapi.py?out_type=json&sip=10.64.22.0/23&packets=4-&sortby=bytes&stats=sip,dip&start_date=2015/07/20:00&end_date=2015/07/20:01&istart=0&iend=10
Same as above with sip grouped by /24 mask
http://testlab/cgi-bin/silk/silkapi.py?out_type=json&sip=10.64.22.0/23&packets=4-&sortby=bytes&stats=sip,dip&start_date=2015/07/20:00&end_date=2015/07/20:01&istart=0&iend=10


Output: (should be mostly obvious)
{"header":  {"timestamp": "1437405231", "version": "0.92"} ,
"query_conditions": {"sip": "10.64.22.0/23", "stats": null, "istart": "0", "end_date": "2015/07/20:01", "out_type": "json", "packets": "4-", "start_date": "2015/07/20:00", "values": "bytes", "sensors": "sensor0", "iend": "1", "class": "all", "types": "in,inweb,inicmp"} ,
"gdata": [
{"duration_secs": 0.17000000000000001, "rowid": 1, "packets": 20, "classname": "all", "tcpflags": "FSPA", "initflags": "SA", "nhip": "0.0.0.0", "duration": "0:00:00.170000", "protocol": 6, "sport": 993, "sip": "10.64.22.24", "stime_epoch_secs": 1437353654.3440001, "session_tcpflags": "FPA", "etime": "2015-07-20 00:54:14.514000", "application": 443, "initial_tcpflags": "SA", "icmpcode": 32, "icmptype": 187, "stime": "2015-07-20 00:54:14.344000", "restflags": "FPA", "sensor": "sensor0", "bytes": 4775, "typename": "in", "etime_epoch_secs": 1437353654.5139999, "classtype": ["all", "in"], "dport": 47904, "dip": "10.67.4.56"}
],"rows":1}


Copyright and license:

SilkWeb
Copyright (c) 2016 Carnegie Mellon University.
All Rights Reserved.

NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN “AS-IS” BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.

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
3. Products derived from this software may not include “Carnegie Mellon University,” "SEI” and/or “Software Engineering Institute" in the name of such derived product, nor shall “Carnegie Mellon University,” "SEI” and/or “Software Engineering Institute" be used to endorse or promote products derived from this software without prior written permission. For written permission, please contact permission@sei.cmu.edu.

ACKNOWLEDGMENTS AND DISCLAIMERS:
This material is based upon work funded and supported by the Department of Defense under Contract No. FA8721-05-C-0003 with Carnegie Mellon University for the operation of the Software Engineering Institute, a federally funded research and development center.

Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the United States Department of Defense.

NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN “AS-IS” BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.

[Distribution Statement A] This material has been approved for public release and unlimited distribution. Please see Copyright notice for non-US Government use and distribution.

CERT® is a registered mark of Carnegie Mellon University.  

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








