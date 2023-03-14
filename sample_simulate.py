from sample_simulation import SAMPLESIMULATION
import sys
import constants as c
import time
import os

test_folder = "./samples/" + sys.argv[1]

solutionID_list = []
for filename in os.listdir(test_folder):
    if "body" in filename:
        solutionID_list.append(filename)

for i in range(len(solutionID_list)):
    solutionID_list[i] = solutionID_list[i].replace("body", "")
    solutionID_list[i] = solutionID_list[i].replace(".urdf", "")

sorted_solutionID_list = []
for i in range(len(solutionID_list)):
    if 'a' in solutionID_list[i]:
        sorted_solutionID_list.append(solutionID_list[i])
for i in range(len(solutionID_list)):
    if 'b' in solutionID_list[i]:
        sorted_solutionID_list.append(solutionID_list[i])
for i in range(len(solutionID_list)):
    if 'c' in solutionID_list[i]:
        sorted_solutionID_list.append(solutionID_list[i])

solutionID1 = sorted_solutionID_list[0]
solutionID2 = sorted_solutionID_list[1]
solutionID3 = sorted_solutionID_list[2]

simulation = SAMPLESIMULATION(solutionID1, test_folder)
simulation.Run()
simulation.__del__()

simulation1 = SAMPLESIMULATION(solutionID2, test_folder)
simulation1.Run()
simulation1.__del__()

simulation2 = SAMPLESIMULATION(solutionID3, test_folder)
simulation2.Run()
simulation2.__del__()