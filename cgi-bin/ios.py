#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
from _elementtree import tostring
import cgitb, cgi
import urllib2, json, ast
import ESPs
import json
import os, time
import threading
from time import sleep

cgitb.enable()


class sendESPthread (threading.Thread):
    def __init__(self, IP, CH, action):
        threading.Thread.__init__(self)
        self.IP = IP
        self.CH = CH
        self.action = action
    def run(self):
        print "Conacting " + self.IP
        url = "http://" + self.IP + "/CH=" + self.CH + "&ACTION=" + self.action
        print url
        urlHandler = urllib2.urlopen(url)
        print urlHandler.read()

        self.exit()


        print "Exiting " + self.name



def sendESPcommand(IP, CH, action):
    print "ThreadESPsend"
#     thread.start_new_threa/d(sendESPcommandworker, (IP,))
    thread=sendESPthread(IP,CH,action)
    print thread
    thread.start()


# def sendESPcommandworker():
#     print "<br>thread sending command to"
#     # url = "http://" + IP + "/CH=" + CH + "&ACTION=" + action
#     print url
    # try:
    # urlHandler = urllib2.urlopen(url)
    # print urlHandler.read()

    # except:
    #     print "sendESP fail"


print "Content-type: text/html\n\n"
# print "HELLO FROM IOS.py"
cgiinput = cgi.FieldStorage()
responsestr = ""
# print ESPs.initIPs

# print cgiinput #for debugging print all input to script from webworld







def getMacros():
    # print "getMacros"

    d = {}
    try:
        # print "trying"
        with open('resources/macros.dat', 'r') as macrofile:
            # print macrofile
            for line in macrofile:
                # print line
                # print "<BR>"
                (key, val) = line.split(',', 1)
                # print key
                # print val
                d[key] = val
                # print key
                # print val
    except:
        False
    return d


def execCommand(command):
    print "COMMAND IS" + command
    instr = command.split(',')

    IP = instr[0].strip()
    CH = instr[1].strip()
    action = instr[2].strip()
    # print IP
    # print CH
    # print action
    sendESPcommand(IP, CH, action)




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
            url = "http://" + IP + "/?CH=" + CH + "&ACTION=" + action
            print url
            urlresponse = urllib.urlopen(url)
            urlresponse = urlresponse.read()
            print urlresponse
        except:
            False

    elif cgiinput.getvalue("mode") == 'loadmacros':
        # print "load macros"

        d = getMacros()
        responsestr = json.dumps(d)

    elif cgiinput.getvalue("mode") == 'execmacro':
        # print "load macros"

        d = getMacros()
        macroID = cgiinput.getvalue("macroID")
        print macroID
        macro= d[macroID].split(":")
        print macro
        print macro
        commands=macro[2:]
        print commands
        for command in commands:
            execCommand(command)







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

