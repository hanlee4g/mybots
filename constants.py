import numpy as np
backLegAmplitude = np.pi / 4.0
backLegFrequency = 10.0
backLegPhaseOffset = 0.0
frontLegAmplitude = np.pi / 4.0
frontLegFrequency = 10.0
frontLegPhaseOffset = np.pi
numberOfGenerations = 3
sleepTime = 1/1000
populationSize = 3
numSensorNeurons = 2
numMotorNeurons = 2
motorJointRange = 0.5

# max links and starting height should be the same
maxLinks = 6
startingHeight = 8

iterations = 5000
maxForce = 100