#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
from _elementtree import tostring
import cgitb,cgi
import urllib,json, ast
import ESPs
cgitb.enable()

print "Content-type: text/html\n\n"
# print "HELLO FROM IOS.py"
cgiinput = cgi.FieldStorage()
# print ESPs.initIPs

# print cgiinput #for debugging print all input to script from webworld



if "mode" in cgiinput: #mode/funciton selection
    # print "mode exists" + cgiinput.getvalue("mode")
    if cgiinput.getvalue("mode") == 'init': #init all ESPs
        # print "in init sequence, going to poll each ESP I know about"
        responsestr='{"ESPDB":[{"espid":"IOSMASTER"}'
        for IP in ESPs.initIPs:
            try:
                # print "<br>getting data from"+IP
                url = 'http://'+IP +"/?init"
                # print url
                urlresponse=urllib.urlopen(url)
                urlresponse=urlresponse.read()
                # print urlresponse
                # data = ast.literal_eval(urlresponse)
                responsestr += ","+urlresponse
                # print data
            except:
                False;
    elif cgiinput.getvalue("mode") == 'xact':
        IP = cgiinput.getvalue("ip")
        CH = cgiinput.getvalue("CH")
        data=cgiinput.getvalue("data")
        try:
                # print "<br>getting data from"+IP
                url = 'http://'+IP +"/?CH="+CH+"&data="+data
                print url
                urlresponse=urllib.urlopen(url)
                urlresponse=urlresponse.read()
                print urlresponse
        except:
            False



else:
    print "ERROR"

responsestr+=']}'
# print "<H3>JSON STR</H3>"
print responsestr

