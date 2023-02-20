from math import frexp
import os
import pyrosim.pyrosim as pyrosim
import numpy as np
#import simulate
import random
import time
import constants as c
from links import LINK

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID

        # number of total links. numlinks - 1 is number of total joints.
        self.numLinks = np.random.randint(1, 20)

        # array of weights number of sensor neurons x number of motor neurons (MOVE THIS SOMEWHERE)
        # self.weights = np.random.rand(self.numSensorNeurons, self.numLinks - 1)
        # self.weights = self.weights * 2 - 1
    
    ### DON'T TOUCH FROM HERE...

    def Start_Simulation(self, directOrGui):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + directOrGui + " " + str(self.myID) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        fileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fileName):
            time.sleep(0.01)
        f = open(fileName, "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm " + fileName)

    def Create_World(self):
        # Start an sdf file
        pyrosim.Start_SDF("world.sdf")
        length, width, height = 0.5, 0.5, 0.5
        x,y,z = -2, 0, 0.5
        pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height], string1 = "Green", string2 = "0 1.0 0 1.0")
        length, width, height = 0.5, 0.5, 0.5
        x,y,z = -8, 0, 0.5  
        pyrosim.Send_Cube(name="Box1", pos=[x,y,z] , size=[length, width, height], string1 = "Green", string2 = "0 1.0 0 1.0")
        # End Pyrosim
        pyrosim.End()

    ### ...TO HERE

    def Create_Body(self):
        # Start an sdf file
        pyrosim.Start_URDF("body.urdf")

        # A list of all links that have been sent to pyrosim
        newLink = LINK(0)
        newLink.sendFirstLink()
        linkList = [newLink]

        # an integer that tracks the id of each new link
        linkIDTracker = 1

        for i in range (1, self.numLinks):
            newLink = LINK(linkIDTracker)
            if newLink.connect(random.choice(linkList)) == 1:
                linkList.append(newLink)
                linkIDTracker += 1

        # Actual number of links (if we try to add a link to an occupied face, we skip it, reducing the number of actual links)
        self.numLinks = linkIDTracker

        # End Pyrosim
        pyrosim.End()

    def Create_Brain(self):
        # Start an sdf file
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # adding sensor neurons where isSensorArray is 0
        # sensor_iterator = 0
        # for i in range(self.numLinks):
        #    if self.isSensorArray[i] == 1:
        #        pyrosim.Send_Sensor_Neuron(name = sensor_iterator, linkName = "Link" + str(i))
        #        sensor_iterator += 1

        # adding motor neurons at every joint
        # for i in range(self.numLinks - 1):
        #     pyrosim.Send_Motor_Neuron( name = self.numSensorNeurons + i, jointName = "Link" + str(i) + "_Link" + str(i+1))

        # connecting each sensor neuron to all of the motor neurons
        # for i in range(self.numSensorNeurons):
        #     for j in range(self.numLinks - 1):
        #         pyrosim.Send_Synapse( sourceNeuronName = i, targetNeuronName = self.numSensorNeurons + j, weight = self.weights[i, j])

        # End Pyrosim
        pyrosim.End()


    def Mutate(self):
        #self.weights[random.randint(0, c.numSensorNeurons - 1), random.randint(0, c.numMotorNeurons - 1)] = random.random() * 2 - 1
        pass

    def Set_ID(self, id):
        self.myID = id