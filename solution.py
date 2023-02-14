import os
import pyrosim.pyrosim as pyrosim
import numpy as np
#import simulate
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID

        # number of total links. numlinks - 1 is number of total joints.
        self.numLinks = np.random.randint(1, 20)

        # an array of length num links with random int lengths between 0 and 10
        self.linkLengthArray = np.random.rand(self.numLinks) * 4
        self.linkWidthArray = np.random.rand(self.numLinks) * 4
        self.linkHeightArray = np.random.rand(self.numLinks) * 4

        # an array of length num links with random ints 0 or 1. 1 is a sensor, 0 is no sensor.
        self.isSensorArray = np.random.randint(2, size=self.numLinks)

        counter = 0
        for i in range(self.isSensorArray.size):
            if self.isSensorArray[i] == 1:
                counter += 1

        # the number of sensor neurons
        self.numSensorNeurons = counter

        # array of weights number of sensor neurons x number of motor neurons
        self.weights = np.random.rand(self.numSensorNeurons, self.numLinks - 1)
        self.weights = self.weights * 2 - 1
    
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

    def Create_Body(self):
        # Start an sdf file
        pyrosim.Start_URDF("body.urdf")

        for i in range(0, self.numLinks - 1):
            if i == 0 & self.isSensorArray[i] == 1:
                pyrosim.Send_Cube(name="Link" + str(i), pos=[self.linkLengthArray[i] / 2.0, 0, 5], size=[self.linkLengthArray[i], self.linkWidthArray[i], self.linkHeightArray[i]], string1 = "Green", string2 = "0 1.0 0 1.0")
                pyrosim.Send_Joint(name = "Link" + str(i) + "_Link" + str(i+1), parent= "Link" + str(i) , child = "Link" + str(i+1) , type = "revolute", position = [self.linkLengthArray[i],0,5], jointAxis = "0 0 1")
            elif i == 0 & self.isSensorArray[i] == 0:
                pyrosim.Send_Cube(name="Link" + str(i), pos=[self.linkLengthArray[i] / 2.0, 0, 5], size=[self.linkLengthArray[i], self.linkWidthArray[i], self.linkHeightArray[i]], string1 = "Blue", string2 = "0 0 1.0 1.0")
                pyrosim.Send_Joint(name = "Link" + str(i) + "_Link" + str(i+1), parent= "Link" + str(i) , child = "Link" + str(i+1) , type = "revolute", position = [self.linkLengthArray[i],0,5], jointAxis = "0 0 1")
            elif self.isSensorArray[i] == 1:
                pyrosim.Send_Cube(name="Link" + str(i), pos=[self.linkLengthArray[i] / 2.0,0,0] , size=[self.linkLengthArray[i], self.linkWidthArray[i], self.linkHeightArray[i]], string1 = "Blue", string2 = "0 0 1.0 1.0")
                pyrosim.Send_Joint(name = "Link" + str(i) + "_Link" + str(i+1), parent= "Link" + str(i) , child = "Link" + str(i+1) , type = "revolute", position = [self.linkLengthArray[i],0,0], jointAxis = "0 0 1")
            else:
                pyrosim.Send_Cube(name="Link" + str(i), pos=[self.linkLengthArray[i] / 2.0,0,0] , size=[self.linkLengthArray[i], self.linkWidthArray[i], self.linkHeightArray[i]], string1 = "Green", string2 = "0 1.0 0 1.0")
                pyrosim.Send_Joint(name = "Link" + str(i) + "_Link" + str(i+1), parent= "Link" + str(i) , child = "Link" + str(i+1) , type = "revolute", position = [self.linkLengthArray[i],0,0], jointAxis = "0 0 1")

        i = self.numLinks - 1
        if self.isSensorArray[i] == 1:
            pyrosim.Send_Cube(name="Link" + str(i), pos=[self.linkLengthArray[i] / 2.0,0,0] , size=[self.linkLengthArray[i], self.linkWidthArray[i], self.linkHeightArray[i]], string1 = "Green", string2 = "0 1.0 0 1.0")
        else:
            pyrosim.Send_Cube(name="Link" + str(i), pos=[self.linkLengthArray[i] / 2.0,0,0] , size=[self.linkLengthArray[i], self.linkWidthArray[i], self.linkHeightArray[i]], string1 = "Blue", string2 = "0 0 1.0 1.0")

        # End Pyrosim
        pyrosim.End()

    def Create_Brain(self):
        # Start an sdf file
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # adding sensor neurons where isSensorArray is 0
        sensor_iterator = 0
        for i in range(self.numLinks):
            if self.isSensorArray[i] == 1:
                pyrosim.Send_Sensor_Neuron(name = sensor_iterator, linkName = "Link" + str(i))
                sensor_iterator += 1

        # adding motor neurons at every joint
        for i in range(self.numLinks - 1):
            pyrosim.Send_Motor_Neuron( name = self.numSensorNeurons + i, jointName = "Link" + str(i) + "_Link" + str(i+1))

        # connecting each sensor neuron to all of the motor neurons
        for i in range(self.numSensorNeurons):
            for j in range(self.numLinks - 1):
                pyrosim.Send_Synapse( sourceNeuronName = i, targetNeuronName = self.numSensorNeurons + j, weight = self.weights[i, j])

        # End Pyrosim
        pyrosim.End()


    def Mutate(self):
        self.weights[random.randint(0, c.numSensorNeurons - 1), random.randint(0, c.numMotorNeurons - 1)] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id