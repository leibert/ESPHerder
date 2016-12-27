__author__ = 'leibert'



from ESPherder.ESPherder import *
from IOSstatemachine.IOSstatemachine import *

statesfile='resources/housestates.dat'
macrofile= 'resources/macros.dat'




# print htmlMacros()
# runMacro("2")

updateState(statesfile, "MOTIONTESTA", "1")
runAutomation()
print "RESET TEST"
updateState(statesfile, "MOTIONTESTA", "2")