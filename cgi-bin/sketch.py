__author__ = 'leibert'



from ESPherder.ESPherder import *
from IOSstatemachine.IOSstatemachine import *

statesfile='resources/housestates.dat'
macrofile= 'resources/macros.dat'
delayfile= 'resources/delaytracking.dat'




# print htmlMacros()
# runMacro("2")

# updateState(statesfile, "MOTIONTESTA", "1")
runAutomation()
# print "RESET TEST"
# updateState(statesfile, "MOTIONTESTA", "2")
# runDelays()
# addDelay(delayfile,"ND",2,"192.168.1.241,1,SWITCHON:DELAY3@LIGHTSOFF#192.168.1.241,1,SWITCHOFF")