#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
from _elementtree import tostring
import cgitb, cgi
import urllib, json, ast
import ESPs
import os, time
from time import sleep

cgitb.enable()

print "Content-type: text/html\n\n"
# print "HELLO FROM IOS.py"
cgiinput = cgi.FieldStorage()
responsestr = ""
# print ESPs.initIPs

# print cgiinput #for debugging print all input to script from webworld


if "mode" in cgiinput:  # mode/funciton selection
    # print "mode exists" + cgiinput.getvalue("mode")
    if cgiinput.getvalue("mode") == 'init':  #init all ESPs
        # print "in init sequence, going to poll each ESP I know about"
        responsestr = '{"ESPDB":[{"espid":"IOSMASTER"}'
        for IP in ESPs.initIPs:
            try:
                # print "<br>getting data from"+IP
                url = 'http://' + IP + "/?init"
                # print url
                urlresponse = urllib.urlopen(url)
                urlresponse = urlresponse.read()
                # print urlresponse
                # data = ast.literal_eval(urlresponse)
                responsestr += "," + urlresponse
                # print data
            except:
                False
        responsestr += ']}'

    elif cgiinput.getvalue("mode") == 'xact':
        print "in xact"
        IP = cgiinput.getvalue("ESPID")
        CH = cgiinput.getvalue("CH")
        action = cgiinput.getvalue("ACTION")
        print action
        try:
            # print "<br>getting data from"+IP
            url = "http://" + IP + "/?CH=" + CH+"&ACTION="+action
            print url
            urlresponse = urllib.urlopen(url)
            urlresponse = urlresponse.read()
            print urlresponse
        except:
            False
    elif cgiinput.getvalue("mode") == 'batch':
        print "yikes, lets try this"
        #write a file with a timestamp, serves as lock file

        lockfile = open("locker.txt", 'w')
        lockedat = str(time.time())
        lockfile.write(lockedat)
        lockfile.close()
        locked=True
        print locked
        steptime = int(cgiinput.getvalue("steptime"))
        batch = cgiinput.getvalue("commands")
        commands = batch.split(';')
        loopflag = False

        while(locked):
            for command in commands:
                print command
                lcheck= open("locker.txt", 'r')
                lcheck.seek(0)
                checkstamp=lcheck.readline()
                lcheck.close()

                if not checkstamp.startswith(lockedat):
                    print "NOTLOCKED"
                    locked = False
                    break

                elif 'zzzz' in command:
                    print "sleep"
                    sleep(steptime/1000)

                elif 'llll' in command:
                    print "we're looping"
                    loopflag=True

                elif command =="":
                    print "empty"

                else: #do something here
                    print "COMMAND IS"+command
                    instr = command.split(',')

                    IP = instr[0].strip()
                    CH = instr[1].strip()
                    action = instr[2].strip()
                    # print IP
                    # print CH
                    # print action
                    try:
                        # print "<br>getting data from"+IP
                        url = "http://" + IP + "/?CH=" + CH+"&ACTION="+action
                        print url
                        urllib.urlcleanup()
                        urlresponse = urllib.urlopen(url)
                        # print urlresponse
                        # urlresponse = urlresponse.read()
                        # print urlresponse
                    except:
                        False

            if not loopflag:
                locked = False
                break









        # print action
        # try:
        #     # print "<br>getting data from"+IP
        #     url = "http://" + IP + "/?CH=" + CH+"&ACTION="+action
        #     print url
        #     urlresponse = urllib.urlopen(url)
        #     urlresponse = urlresponse.read()
        #     print urlresponse
        # except:
        #     False



else:
    print "ERROR"

# print "<H3>JSON STR</H3>"
print responsestr

