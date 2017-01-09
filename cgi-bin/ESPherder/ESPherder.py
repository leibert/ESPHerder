__author__ = 'leibert'
import threading
import urllib2
import sys
import argparse
sys.path.append('/var/www/html/cgi-bin/IOS')

# sys.path.append('/home/leibert/PycharmProjects/IoSMaster/cgi-bin')
# sys.path.append('/home/leibert/GITprojects/IoSMaster/cgi-bin')

from IOSstatemachine.IOSstatemachine import *

statesfile='/var/www/html/cgi-bin/IOS/resources/housestates.dat'
macrofile= '/var/www/html/cgi-bin/IOS/resources/macros.dat'
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
    # print "COMMAND IS" + command

    #Allows for comments in file
    if command.startswith("/"):
        print "comment"
        return

    #This command is a Macro (or sequence of commands)
    elif command.startswith("MACRO"):
        print "this is a macro"
        macroID=command[5:]
        runMacro(macroID)

    #This checks to see if another state is true or false. For example, were particular lights turned on manually. You may not want a time or motion based event to override that
    elif command.statswith("?X"):
        print "this is a statechecker"
        statekey=command[2:]
        if(getstoredState(statesfile,statekey)=="true"):
            print "This macro is locked out by another state being true"
            return


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
            execCommand(command)


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

