__author__ = 'leibert'
import threading
import urllib2
import sys, time, datetime
import argparse
from time import sleep
sys.path.append('/var/www/html/cgi-bin/IOS')

# sys.path.append('/home/leibert/PycharmProjects/IoSMaster/cgi-bin')
# sys.path.append('/home/leibert/GITprojects/IoSMaster/cgi-bin')

from IOSstatemachine.IOSstatemachine import *

statesfile='/var/www/html/cgi-bin/IOS/resources/housestates.dat'
macrofile= '/var/www/html/cgi-bin/IOS/resources/macros.dat'
routinefile= '/var/www/html/cgi-bin/IOS/resources/routines.dat'
delayfile= '/var/www/html/cgi-bin/IOS/resources/delaytracking.dat'
automationfile= '/var/www/html/cgi-bin/IOS/resources/automation.dat'


class sendESPthread (threading.Thread):
    def __init__(self, IP, CH, action):
        threading.Thread.__init__(self)
        self.IP = IP
        self.CH = CH
        self.action = action
    def run(self):
        print "Conacting " + self.IP
        url = "http://" + self.IP + "/CH=" + self.CH + "&ACTION=" + self.action
        url = url.strip()
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



def execCommand(command):

    #Allows for comments in file
    if command.startswith("/"):
        print "comment"
        return False

    #Update state with value.
    elif command.startswith("STATE"):
        print "set a state"
        key=command[5:command.index("#")].strip()
        value=command[command.index("#")+1:].strip()
        updateState(statesfile,key,value)


    #This command is a Macro (or sequence of commands)
    elif command.startswith("MACRO"):
        print "this is a macro"
        macroID=command[5:]
        runMacro(macroID)

    #This checks to see if another state is true or false. For example, were particular lights turned on manually. You may not want a time or motion based event to override that
    elif command.startswith("?X"):
        print "this is a statechecker"
        statekey=command[2:]
        sys.stderr.write("key is\n"+ statekey)

        if(getstoredState(statesfile,statekey)=="true"):
            print "This macro is locked out by another state being true"
            return False


    #Flags the value of a variable. The flag is used to denote the macro has been executed based on the value being checked by the automation script.
    #This prevents the automation scripting to repeatedly send out commands or if a sensor, light a motion sensor, has been repeatedly tripped within a short amount of time.
    #A time based delay can unflag this

    elif command.startswith("FLAG"):
        print "flag variable"
        flag=command[4:command.index("#")]
        key=command[command.index("#")+1:]
        print key + " with " + flag+"\n<BR>"
        flagState(statesfile,key,flag)

    #unflag variable
    elif command.startswith("UNFLAG"):
        print "UNflag variable"
        flag=command[6:]
        key=command[command.index("#")+1:]
        print key + " with " + flag
        unflagState(statesfile,key)

    #Adds a command to the delay file. For example you could execute a macro (or ESP command) to turn off lights in a set time period (half hour later)
    elif command.startswith("DELAY"):
        print "DELAY"
        length=command[5:command.index("@")]
        key=command[command.index("@")+1:command.index("#")]
        commands=command[command.index("#")+1:]
        addDelay(delayfile,key,length,commands)

    #nothing special, so just split the command into IP address, channel, and the action and pass it along
    else:
        instr = command.split(',')
        IP = instr[0].strip()
        CH = instr[1].strip()
        action = instr[2].strip()
        # print IP
        # print CH
        # print action
        sendESPcommand(IP, CH, action)
    return True


def getMacros():
    # print "getMacros"

    d = {}
    try:
        # print "trying"
        with open(macrofile, 'r') as macros:
            # print macrofile
            for line in macros:
                # print line
                # print "<BR>"
                (key, val) = line.split(',', 1)
                # print key
                # print val
                d[key] = val
                sys.stderr.write("macro "+ key)
                # print key
                # print val
    except:
        False
    return d


def getRoutine(routineID):
    # print "getMacros"
    sys.stderr.write("get routines")

    routineholder = []
    try:
        # print "trying"
        sys.stderr.write("TRYING")
        with open(routinefile, 'r') as routines:
            sys.stderr.write("FILE OPENED")
            sys.stderr.write(routinefile)

            readingroutine=False
            routineheader=""
            for line in routines:
                # sys.stderr.write(line)
                if line.startswith("ROUTINE,"+routineID+","):#Routin found
                    # sys.stderr.write(line)
                    routineheader=line[line.index("ROUTINE")+8:]
                    (key,routineheader)=routineheader.split(",",1)
                    readingroutine=True

                elif line.startswith("EOR"):
                    readingroutine=False

                elif readingroutine:
                    routineholder.append(line) #ADD line from routine to array

    except:
        False
    return routineholder



def getRoutineHeaders():
    # print "getMacros"
    sys.stderr.write("get routines")

    d = {}
    try:
        # print "trying"
        sys.stderr.write("TRYING")
        with open(routinefile, 'r') as routines:
            sys.stderr.write("FILE OPENED")
            sys.stderr.write(routinefile)

            routineholder=""
            routineheader=""
            for line in routines:
                # sys.stderr.write(line)
                if line.startswith("ROUTINE"):#This is the start of a new routine
                    sys.stderr.write(line)
                    routineheader=line[line.index("ROUTINE")+8:]
                    (key,routineheader)=routineheader.split(",",1)
                    # sys.stderr.write(routineheader)

                    # (key,value)=line[routineheader.index("ROUTINE,"+1):].split(",",1)
                    # key=routineheader[routineheader.index("ROUTINE,"+1):routineheader.index(",")]
                    # value=line.rsplit(",",3)
                    # sys.stderr.write("routine"+key+"@"+value)
                    d[key]=routineheader
                #     routineheader=line
                #
                # # print line
                # # print "<BR>"
                # header = routine.split(':',3)
                # key=header[1].split(',',1)
                # val=header[1].rsplit(',',1)+header[2]+header[3]
                # sys.stderr.write("routine"+key+"@"+val)
                #
                # # print val
                # d[key] = val
                # print key
                # print val
    except:
        False
    return d


def runMacro(macroID):
        d = getMacros()
        # print macroID
        macro= d[macroID].split(":")
        # print macro
        print macro
        print "<BR>COMMAND SET<BR>"
        commands=macro[2:]
        print commands
        for command in commands:
            # print command +"<BR>"
            if execCommand(command) == False:
                break

def runRoutine(routineID,steptime):
        # headers = getRoutineHeaders()
        d = getRoutine(routineID)
        # header=headers[routineID]
        # header=header.split(",")
        # print macroID
        # runBatch(d,header[2])
        # macro= d[macroID].split(":")
        runBatch(routineID,steptime)

        # print macro
        # print "<BR>COMMAND SET<BR>"
        # commands=macro[2:]
        # print commands
        # for command in commands:
        #     # print command +"<BR>"
        #     if execCommand(command) == False:
        #         break

def runBatch(batch,steptime):

        lockfile = open("locker.txt", 'w')
        lockedat = str(time.time())
        lockfile.write(lockedat)
        lockfile.close()
        locked = True
        print locked

        print "yikes, lets try this"
        # write a file with a timestamp, serves as lock file

        loopflag = False

        while (locked):
            for command in batch:
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
                    if command[4:]!='': #is a sleep value defined?
                        sleep(int(command[4:]))
                    else: #use default sleep
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


def runAutomation():
    # print "force automation run on state update"

    for command in checkAutomation(statesfile,automationfile):
        # print command
        execCommand(command)


def runDelays():
    slop = 5
    for command in checkDelays(delayfile,slop):
        # print command
        execCommand(command)




def minutelychecks():
    # print "minute check"
    runAutomation()
    runDelays()


# def sendESPcommandworker():
#     print "<br>thread sending command to"
#     # url = "http://" + IP + "/CH=" + CH + "&ACTION=" + action
#     print url
    # try:
    # urlHandler = urllib2.urlopen(url)
    # print urlHandler.read()

    # except:
    #     print "sendESP fail"


# runAutomation()


parser = argparse.ArgumentParser()

parser.add_argument('--checks', action='store_true', help='run minute checks')




args = parser.parse_args()
# print args

if args.checks:
    # print "minute check"
    runDelays()
    runAutomation()

