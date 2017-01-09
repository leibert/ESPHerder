__author__ = 'leibert'

import sys
import datetime
from datetime import timedelta
import argparse
# sys.path.append('/home/leibert/pyScripts')
sys.path.append('/home/leibert/PycharmProjects/IoSMaster/cgi-bin')
sys.path.append('/var/www/html/cgi-bin/IOS')
# import ios

# sys.path.append('/home/leibert/pyScripts')
# sys.path.append('/home/leibert/Documents/gitRepos/datacollectionbot')

# from datacollectionbot.databot import *

# updateCMDCTRL()



def readstoredStates(statedb):
    d = {}
    # print statedb
    try:
        with open(statedb, 'r') as file:
            # with open('housestates.dat', 'r') as file:

            for line in file:
                # print line
                line = line.replace('\n', '')
                if line == "" or line.startswith('/'):
                    continue
                state = line.split(',',1)
                # print state
                if state[0] is None:
                    continue
                d[state[0]] = state[1]
                # try:
                # d[state[0]][1]=state[2]
                # except:
                #     d[state[0]][1]=None
    except:
        # print "error parsing states file"
        return None
    return d


def getstoredState(statedb, key):
    try:
        d = readstoredStates(statedb)
        if key in d:
            return d[key]
        else:
            return None
    except:
        print "stored state not found"
        return None


def writeStates(statedb, dict):
    # print "Write states"
    # print statedb
    # print dict
    # print "---------\n"
    try:
        f = open(statedb, 'w')
        # print "test"
        # f = open('housestates.dat', 'r')

        f.seek(0)
        # print "DICT"
        for key,value in dict.iteritems():
            # print "<BR>\n"
            # print key
            # print dict[key]
            f.write(key + "," + value)
            f.write('\n')

        f.truncate()
        f.close()
    except:
        print "error writing"


def updateState(statedb, key, value):
    d = readstoredStates(statedb)
    key=key.strip()
    # print "\nupdating"+key
    # print value
    if d is None:
        d = {}
        d[key] = value
        writeStates(statedb, d)
        return

    # print "dict exists"

    if value == "TS":
        value = str(datetime.datetime.now())

    # print "flag check"

    try:
        # check to see if its a flagged value
        if "#" in d[key]:
            unflaggedvalue = d[key][:d[key].index("#")]
            if(unflaggedvalue!=value):
                # print "different value"
                # print "FLAGGED w/ value change"
                # print d[key][d[key].index("#"):]
                d[key] = value + d[key][d[key].index("#"):]#different unflaggedvalue update state
                # print "FINALKEY<BR>"
                # print d[key]
                writeStates(statedb, d)
                return
            else:
                # print "FLAGGED & no value change"
                return #value hasn't changed once flag removed exit funciton
    except:
        print "key doesn't exist create new key"



        # print "unflagged"
    d[key] = value
    # d[key]="None"
    # if (getstoredState(statedb,key)!= value): #don't overwrite state line if no change, there may be flags to indicate state acted upon
    writeStates(statedb, d)




def flagState(statedb, key, flag):
    d = readstoredStates(statedb)
    key=key.strip()
    # print d
    # print key
    # print flag
    try:
        # print d[key]
        if "#" in d[key]:
            print "already flagged, remove flag"
            d[key]=d[key][:d[key].index("#")]
        d[key] = str(d[key]) +"#"+str(flag)
        # print d[key]
        writeStates(statedb, d)
    except:
        print "KEY DOESNT EXIST TO FLAG"

def unflagState(statedb, key):
    d = readstoredStates(statedb)
    key=key.strip()
    # print key
    try:
        # check to see if its a flagged value
        if "#" in d[key]:
            # print d[key]
            unflaggedvalue = d[key][:d[key].index("#")]
            # print "FLAG ON "+key+" REMOVED"
            d[key] = unflaggedvalue
            writeStates(statedb,d)
    except:
        # print "key doesn't exist create new key"
        # print "WASN'T FLAGGED"
        return





def readstoredDelays(delayfile):
    d = {}
    try:
        with open(delayfile, 'r') as file:
            # with open('housestates.dat', 'r') as file:

            for line in file:
                line = line.replace('\n', '')
                if line == "" or line.startswith('/'):
                    continue
                (key, val) = line.split(',',1)
                if key is None:
                    continue
                d[key] = val
    except:
        print "error parsing delays file"
        return None
    return d


def getstoredDelays(delayfile,key):
    try:
        d = readstoredDelays(delayfile)
        if key in d:
            return d[key]
        else:
            return None
    except:
        print "stored state not found"
        return None


def writeDelays(delayfile,dict):
    try:
        f = open(delayfile, 'w')
        # f = open('housestates.dat', 'w')

        f.seek(0)

        for key, value in dict.iteritems():
            f.write(key + "," + value)
            f.write('\n')

        f.truncate()
        f.close()
    except:
        print "error writing"


def addDelay(delayfile,key, delay, commands):
    d = readstoredDelays(delayfile)
    if d is None:
        d = {}
    time = datetime.datetime.now() + timedelta(minutes=int(delay))
    # print time

    # if value == "TS":
    #     value = str(datetime.datetime.now())
    d[key] = str(time)+"#"+commands
    # print d[key]
    writeDelays(delayfile, d)


def checkDelays(delayfile, slop):
    pendingCommands=[]
    try:
        d = readstoredDelays(delayfile)
        if d != None:
            try:
                for delay in d:
                    try:
                        # print delay
                        delaystring = d[delay]
                        # print delaystring
                        delaytimestamp=delaystring[:delaystring.index("#")]
                        # print delaytimestamp
                        if checkTimer(delaytimestamp,slop):
                            # print "timer valid"
                            # print "APPEND COMMANDS"
                            commandset=delaystring[delaystring.index("#")+1:].split(":")
                            # print "<BR>COMMANDSET"
                            # print commandset
                            pendingCommands+=commandset
                            d.pop(delay,None)



                            # if datetime.datetime.now() > datetime.datetime.strptime(delay, "%Y-%m-%d %H:%M:%S.%f")
                            #     commands=d[delay].split(":")
                            #     for command in commands:
                            #         command=command.split(",")
                            #         print command
                            #         sendESPcommand(command[0],command[1],command[2])
                        # else:
                            # print "timer hasn't flipped"

                    except:
                        pass
                        # print "delay error"
            except:
                pass
            writeDelays(delayfile,d)



    except:
        print "No delay file"

    return pendingCommands





def checkTimer(time, slop):
    pendingCommands = []
    # print "in check timer"
    lcltime = datetime.datetime.now()
    try:
        # if sunset / sunrise etc
        timetocheck = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    except:
        # print "check timer error"
        timetocheck = None
        return None

    # print "timecompare"
    if lcltime > timetocheck:
        # print "time to check has passed"
        # print timetocheck
        # print lcltime
        timedelta = lcltime - timetocheck
        # print timedelta.seconds
        # print (timedelta.seconds/60)

        if (timedelta.seconds/60) < slop:
            return True
    return False


def checkAutomation(statesfile, autodb):
    statesdict = readstoredStates(statesfile)
    pendingCommands = []
    # print "STARTING AUTOMATION RUNS"
    # print statesdict
    try:
        with open(autodb, 'r') as file:
            for line in file:
                line = line.replace('\n', '')
                try:
                    autoevent = line.split(":", 1)
                    # print autoevent
                    eventheader = autoevent[0].split(",")
                    # print eventheader
                    if eventheader[0] == "R":  #this is a reaction to a state event
                        # print "REACTION"
                        if eventheader[1] in statesdict:  #is there a correspoinding state for the automation command
                            # print "found in statedict"
                            # print eventheader[2]
                            # print eventheader[1]
                            # print "state value"
                            # print statesdict[eventheader[1]]
                            if eventheader[2] == statesdict[eventheader[1]]:#is the state correct for a response
                                # print "APPEND COMMAND"
                                commandset= autoevent[1].split(":")
                                # print "<BR>COMMANDSET"
                                # print commandset


                                pendingCommands+=commandset

                    elif eventheader[0] == "T":
                        # print "TIME BASED"
                        if checktimer(eventheader[1], 70):  #over a minute of slop time included
                            # print "APPEND TIME COMMAND"
                            pendingCommands.append([autoevent[1]])
                except:
                    # print "automation error possible file format error"
                    # print autoevent
                    pass


    except:
        print "AUTOMATION ERROR"
    # print "PENDING COMMANDS"
    # print pendingCommands
    return pendingCommands



