import os
import pyrosim.pyrosim as pyrosim
import numpy as np
#import simulate
import random
import time
import constants as c
import copy

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.numLinks = np.random.randint(0, 20)
        self.linkLengthArray = np.random.rand(self.numLinks) * 10
        self.isSensorArray = np.random.randint(2, size=self.numLinks)
    
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
        pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])

        length, width, height = 0.5, 0.5, 0.5
        x,y,z = -8, 0, 0.5  
        pyrosim.Send_Cube(name="Box1", pos=[x,y,z] , size=[length, width, height])

        # End Pyrosim
        pyrosim.End()

    def Create_Body(self):
        # Start an sdf file
        pyrosim.Start_URDF("body.urdf")

        # Worm
        pyrosim.Send_Cube(name="Torso", pos=[0,0,0] , size=[1, 0.2, 0.2])

        for i in range(self.numLinks):
            if i == 0:
                pyrosim.Send_Joint( name = "Joint" + str(i) , parent= "Torso" , child = "Link" + str(i) , type = "revolute", position = [0.5,0,0], jointAxis = "0 1 0")
                pyrosim.Send_Cube(name="Link" + str(i), pos=[self.linkLengthArray[i]/2.0,0,0] , size=[self.linkLengthArray[i], 0.2, 0.2])
            else:
                pyrosim.Send_Joint( name = "Joint" + str(i) , parent= "Link" + str(i - 1) , child = "Link" + str(i) , type = "revolute", position = [self.linkLengthArray[i],0,0], jointAxis = "0 1 0")
                pyrosim.Send_Cube(name="Link" + str(i), pos=[self.linkLengthArray[i]/2.0,0,0] , size=[self.linkLengthArray[i], 0.2, 0.2])

        # End Pyrosim
        pyrosim.End()

    def Create_Brain(self):
        # Start an sdf file
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # For Torso
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")

        self.localNumSensorNeurons = 1
        for i in range(self.numLinks):
            if self.isSensorArray[i] == 1:
                pyrosim.Send_Sensor_Neuron(name = self.localNumSensorNeurons , linkName = "Link" + str(i))
                self.localNumSensorNeurons += 1
        
        localMotorNeuronCode = copy.deepcopy(self.localNumSensorNeurons)

        for i in range(self.numLinks):
            if i == 0:
                pyrosim.Send_Motor_Neuron( name = localMotorNeuronCode, jointName = "Torso_Link" + str(i))
                localMotorNeuronCode += 1
            else:
                pyrosim.Send_Motor_Neuron( name = localMotorNeuronCode, jointName = "Link" + str(i-1) + "_Link" + str(i))
                localMotorNeuronCode += 1

        self.weights = np.random.rand(self.numLinks + 1, self.numLinks) * 2 - 1

        pyrosim.Send_Synapse( sourceNeuronName = 0 , targetNeuronName = self.localNumSensorNeurons, weight = self.weights[0][0])

        sensorCounter = 1
        for i in range(1, self.numLinks):
            if self.isSensorArray[i] == 1:
                targetIndex = self.localNumSensorNeurons
                counter = 0
                for j in range(self.isSensorArray.size):
                    if j < i:
                        counter += 1
                targetIndex += counter

                pyrosim.Send_Synapse( sourceNeuronName = sensorCounter , targetNeuronName =  targetIndex, weight = self.weights[i][i])
                sensorCounter += 1

        # End Pyrosim
        pyrosim.End()


    def Mutate(self):
        self.weights[random.randint(0, self.self.numLinks + 1), random.randint(0, self.numLinks)] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id