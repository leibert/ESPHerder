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


def checkDelays():
    d = readstoredDelays()
    if d != None:
        for delay in d:
            try:
                if datetime.datetime.now() > datetime.datetime.strptime(delay, "%Y-%m-%d %H:%M:%S.%f")
                    commands=d[delay].split(":")
                    for command in commands:
                        command=command.split(",")
                        print command
                        sendESPcommand(command[0],command[1],command[2])

            except:
                print "delay error"


    else:
        print "No delay file"


parser = argparse.ArgumentParser()

# parser.add_argument('--buses', action='store_true', help='update buses')
# parser.add_argument('--weather', action='store_true', help='update weather')
# parser.add_argument('--astronomy', action='store_true', help='update astronomy')
# parser.add_argument('--state', action='store', help='update a house state key=value')
# # parser.add_argument('--weather', action='store_true', help='update weather') Do something for coffee...action bots? pass in a CMD
parser.add_argument('--all', action='store_true', help='update all')

args = parser.parse_args()
# print args

if args.all:
    print "all"
    checkDelays()
