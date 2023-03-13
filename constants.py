import numpy as np
# Set the following two fields to change generation + population
numberOfGenerations = 500
populationSize = 10

backLegAmplitude = np.pi / 4.0
backLegFrequency = 10.0
backLegPhaseOffset = 0.0
frontLegAmplitude = np.pi / 4.0
frontLegFrequency = 10.0
frontLegPhaseOffset = np.pi
sleepTime = 1/1000
numSensorNeurons = 2
numMotorNeurons = 2
motorJointRange = 0.6

# max links and starting height should be the same
maxLinks = 6
startingHeight = 6

iterations = 3000
maxForce = 50