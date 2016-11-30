__author__ = 'leibert'

def loadMacros():

    print "load macros"
    d= {}
    try:
        with open('resources/macros.dat', 'r') as file:
            for line in file:
                desc=line[0:line.find(":")]
                desc=desc.split(",")
                command = line[(line.find(":")+1):].strip()
                d[desc[0]] = (desc[1],desc[2],command)
    except:
        False
    return d

def htmlMacros():
    html=""
    macrodict=loadMacros()
    for key, value in macrodict.items():
        print key
        if value[0]=="BTN":
            html+="<A HREF='/cgi-bin/ios.py?XMAC="+key+"'>"+value[1]+"</a><br>"
    return html


def runMacro(macroID):
    macrodict=loadMacros()
    macro=macrodict[macroID]
    commands=macro[2].split(":")
    for command in commands:
        command=command.split(",")
        print command
        sendESPcommand(command[0],command[1],command[2])






# print htmlMacros()
runMacro("2")
