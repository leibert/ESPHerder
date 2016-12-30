#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
from _elementtree import tostring
import cgitb, cgi
import urllib2, json, ast
import ESPs
import json
import os, time, datetime
from ESPherder.ESPherder import *
from IOSstatemachine.IOSstatemachine import *

from time import sleep


cgitb.enable()

# statesfile='/var/www/html/espserve/CMDCTRL/housestates.dat'
# statesfile='resources/housestates.dat'
statesfile='/var/www/html/cgi-bin/IOS/resources/housestates.dat'
macrofile= 'resources/macros.dat'







print "Content-type: text/html\n\n"
# print "HELLO FROM IOS.py"
cgiinput = cgi.FieldStorage()
responsestr = ""
# print ESPs.initIPs

# print cgiinput #for debugging print all input to script from webworld










if "mode" in cgiinput:  # mode/funciton selection
    # print "mode exists" + cgiinput.getvalue("mode")
    if cgiinput.getvalue("mode") == 'initscanner':  #init all ESPs
        # print "in init sequence, going to poll each ESP I know about"
        responsestr = '{"ESPDB":[{"espid":"IOSMASTER"}'
        for IP in ESPs.initIPs:
            try:
                # print "<br>getting data from"+IP
                url = 'http://' + IP + "/?init"
                # print url
                urlresponse = urllib2.urlopen(url)
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
            url = "http://" + IP + "/?CH=" + CH + "&ACTION=" + action
            print url
            urlresponse = urllib2.urlopen(url)
            urlresponse = urlresponse.read()
            print urlresponse
        except:
            False

    elif cgiinput.getvalue("mode") == 'loadmacros':
        # print "load macros"

        d = getMacros()
        responsestr = json.dumps(d)

    elif cgiinput.getvalue("mode") == 'updstate':
        print "update state"
        try:
            key = cgiinput.getvalue("KEY")
            value = cgiinput.getvalue("VALUE")
            print key
            print value
            updateState(statesfile, key, value)
            print "<BR>AUTOMATION:"
            runAutomation()
            print "DONE"


        except:
            responsestr = "UPDSTATEERROR"





    elif cgiinput.getvalue("mode") == 'execmacro':
        # print "load macros"

        macroID = cgiinput.getvalue("macroID")
        runMacro(macroID)





    elif cgiinput.getvalue("mode") == 'batch':
        print "yikes, lets try this"
        # write a file with a timestamp, serves as lock file

        lockfile = open("locker.txt", 'w')
        lockedat = str(time.time())
        lockfile.write(lockedat)
        lockfile.close()
        locked = True
        print locked
        steptime = int(cgiinput.getvalue("steptime"))
        batch = cgiinput.getvalue("commands")
        commands = batch.split(';')
        loopflag = False

        while (locked):
            for command in commands:
                print command
                lcheck = open("locker.txt", 'r')
                lcheck.seek(0)
                checkstamp = lcheck.readline()
                lcheck.close()

                if not checkstamp.startswith(lockedat):
                    print "NOTLOCKED"
                    locked = False
                    break

                elif 'zzzz' in command:
                    print "sleep"
                    sleep(steptime / 1000)

                elif 'llll' in command:
                    print "we're looping"
                    loopflag = True

                elif command == "":
                    print "empty"

                else:  #do something here
                    execCommand(command)


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

# else:
#     GET WORLD VIEW
# UPDATE WEATHER
# UPDATE MBTA
# BOTH STORED IN FLAT TEXT FILES


# UPDATE SIGN
#



    else:
        print "ERROR 3s1w"

# print "<H3>JSON STR</H3>"
print responsestr




