from sample_simulation import SAMPLESIMULATION
import sys
import constants as c
import time

test_folder = sys.argv[1]

solutionID1 = ''
solutionID2 = ''
solutionID3 = ''

simulation1 = SAMPLESIMULATION(solutionID1)
simulation1.Run()

time.sleep(5)

simulation2 = SAMPLESIMULATION(solutionID2)
simulation2.Run()

time.sleep(5)

simulation3 = SAMPLESIMULATION(solutionID3)
simulation3.Run()