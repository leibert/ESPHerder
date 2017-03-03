#access server
import os

cardrolllocation="../ESPHerder/espserve/CMDCTRL/cardroll.dat"
IDfilelocation="../ESPHerder/access/IDS/"



def updatecardroll():
    print "Updating Card roll"
    dirs = os.listdir(IDfilelocation) # returns list

    cardroll={}


    for file in dirs:
        if file.endswith(".ID"):
            ID = file[0:file.find(".ID")]
            #print ID
            with open(IDfilelocation+file, 'r') as file:
                #print file.readline()
                cardroll[ID]=file.readline().rstrip();

                
    print cardroll
    if len(cardroll) > 0:
        writecardroll(cardroll)
        


def writecardroll(cardroll):
    try:
        f = open(cardrolllocation, 'w')

        f.seek(0)

        for key, value in cardroll.iteritems():
            f.write(key+","+value)
            f.write('\n')

        f.truncate()
        f.close()
    except:
        print "error writing"


def runIDcommands(ID):
    print "run ID command"
    try:

        IDfile=IDfilelocation+str(ID)+".ID" 
        #print IDfile

        with open(IDfile, 'r') as file:
            #print file
            for line in file:
            
                if "AMD" in line:
                    print "There is a music command in here"
                    musicpath = line[line.find("AMD:")+4:]
                    print musicpath
        
    except:
        print "error opening ID card dat file";
            #print file.readline()
            #cardroll[ID]=file.readline().rstrip();



#updatecardroll()
runIDcommands(2080060114)

