__author__ = 'leibert'

import sys
import datetime
import argparse
# sys.path.append('/home/leibert/pyScripts')
sys.path.append('/home/leibert/PycharmProjects/IoSMaster/cgi-bin')
sys.path.append('/var/www/html/cgi-bin/IOS')
import ios

# sys.path.append('/home/leibert/pyScripts')
# sys.path.append('/home/leibert/Documents/gitRepos/datacollectionbot')

# from datacollectionbot.databot import *

# updateCMDCTRL()



def readstoredStates(statedb):
    d= {}
    print statedb
    try:
        with open(statedb, 'r') as file:
        # with open('housestates.dat', 'r') as file:

            for line in file:
                print line
                line=line.replace('\n','')
                state=line.split(',')
                print state
                if state[0] is None:
                        continue
                d[state[0]] = state[1]
                # try:
                #     d[state[0]][1]=state[2]
                # except:
                #     d[state[0]][1]=None
    except:
        print "error parsing states file"
        return None
    return d

def getstoredState(statedb,key):
    try:
        d=readstoredStates(statedb)
        if key in d:
            return d[key]
        else:
            return None
    except:
        print "stored state not found"
        return None

def writeStates(statedb,dict):
    try:
        f = open(statedb, 'w')
        # f = open('housestates.dat', 'w')

        f.seek(0)

        for key in dict.iteritems():
            f.write(key+","+dict[key]+", False")
            f.write('\n')

        f.truncate()
        f.close()
    except:
        print "error writing"


def updateState(statedb,key,value):
    d=readstoredStates(statedb)
    if d is None:
        d={}
    if value == "TS":
        value = str(datetime.datetime.now())
    d[key]=value
    # d[key]="None"
    # if (getstoredState(statedb,key)!= value): #don't overwrite state line if no change, there may be flags to indicate state acted upon
    writeStates(statedb, d)

def flagState(statedb,key,flag):
    d=readstoredStates(statedb)
    if d is None:
        d={}

    d[key]=str(d[key])+str(flag)
    writeStates(statedb, d)






def readstoredDelays():
    d= {}
    try:
        with open('delaytracking.dat', 'r') as file:
        # with open('housestates.dat', 'r') as file:

            for line in file:
                line=line.replace('\n','')
                (key, val) = line.split(';')
                if key is None:
                        continue
                d[key] = val
    except:
        print "error parsing states file"
        return None
    return d

def getstoredDelays(key):
    try:
        d=readstoredDelays()
        if key in d:
            return d[key]
        else:
            return None
    except:
        print "stored state not found"
        return None




def writeDelays(dict):
    try:
        f = open('delaytracking.dat', 'w')
        # f = open('housestates.dat', 'w')

        f.seek(0)

        for key, value in dict.iteritems():
            f.write(key+","+value)
            f.write('\n')

        f.truncate()
        f.close()
    except:
        print "error writing"


def updateDelay(key,value):
    d=readstoredDelays()
    if d is None:
        d={}
    if value == "TS":
        value = str(datetime.datetime.now())
    d[key]=value
    writeDelays(d)


# def checkDelays():
#     d = readstoredDelays()
#     if d != None:
#         for delay in d:
#             try:
#                 if datetime.datetime.now() > datetime.datetime.strptime(delay, "%Y-%m-%d %H:%M:%S.%f")
#                     commands=d[delay].split(":")
#                     for command in commands:
#                         command=command.split(",")
#                         print command
#                         sendESPcommand(command[0],command[1],command[2])
#
#             except:
#                 print "delay error"
#
#
#     else:
#         print "No delay file"

# def readAutomationfile(autodb):
#     d= {}
#     try:
#         with open(autodb, 'r') as file:
#         # with open('housestates.dat', 'r') as file:
#
#             for line in file:
#                 line=line.replace('\n','')
#                 (key, val) = line.split(',')
#                 if key is None:
#                         continue
#                 d[key] = val
#     except:
#         print "error parsing states file"
#         return None
#     return d



def checktimer(time, slop):
    print "in check timer"
    lcltime = datetime.datetime.now()
    try:
        # if sunset / sunrise etc
        timetocheck=datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    except:
        print "check timer error"
        timetocheck=None
        return None

    print "timecompare"
    if lcltime>timetocheck:
        print "time to check has passed"
        timedelta=timetocheck-lcltime
        if timedelta.seconds < slop:
            return True
    return False


def checkAutomation(statesfile, autodb):
    statesdict=readstoredStates(statesfile)
    pendingCommands=[]
    print "STARTING AUTOMATION RUNS"
    print statesdict
    try:
        with open(autodb, 'r') as file:
            for line in file:
                line=line.replace('\n','')
                try:
                    autoevent=line.split(":",1)
                    # print autoevent
                    eventheader=autoevent[0].split(",")
                    print eventheader
                    if eventheader[0]=="R": #this is a reaction to a state event
                        print "REACTION"
                        if eventheader[1] in statesdict: #is there a correspoinding state for the automation command
                            print "found in statedict"
                            print eventheader[2]
                            print eventheader[1]
                            print "state value"
                            print statesdict[eventheader[1]]
                            if eventheader[2] == statesdict[eventheader[1]] and statesdict[eventheader[1]][0] != True: #is the state correct for a response
                                print "APPEND COMMAND"
                                pendingCommands.append(autoevent[1])
                                flagState(statesfile,eventheader[1],"True")
                    elif eventheader[0]=="T":
                        print "TIME BASED"
                        if checktimer(eventheader[1],70): #over a minute of slop time included
                            print "APPEND TIME COMMAND"
                            pendingCommands.append([autoevent[1]])
                except:
                    print "automation error possible file format error"
                    print autoevent
    except:
        "AUTOMATION ERROR"




