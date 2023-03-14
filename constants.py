import numpy as np
# Set the following two fields to change generation + population
numberOfGenerations = 500
populationSize = 10

# Set this to change how many total runs w different random seeds
numOfSeeds = 1

# These two values should be the same
maxLinks = 6
startingHeight = 6

# Other variables (not necesarily applicable to every run)
backLegAmplitude = np.pi / 4.0
backLegFrequency = 10.0
backLegPhaseOffset = 0.0
frontLegAmplitude = np.pi / 4.0
frontLegFrequency = 10.0
frontLegPhaseOffset = np.pi
numSensorNeurons = 2
numMotorNeurons = 2
motorJointRange = 0.6
maxForce = 50

# Do not Modify
sleepTime = 1/1000
iterations = 3000