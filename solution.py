import os
import pyrosim.pyrosim as pyrosim
import numpy as np
#import simulate
import random
import time

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.weights = np.random.rand(3, 2)
        self.weights = self.weights * 2 - 1
        self.myID = nextAvailableID
    
    def Start_Simulation(self, directOrGui):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + directOrGui + " " + str(self.myID) + " &")

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

        # Create a cube
        length, width, height = 1, 1, 1
        x,y,z = -3, -3, 0.5  
        pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])

        # End Pyrosim
        pyrosim.End()

    def Create_Body(self):
        # Start an sdf file
        pyrosim.Start_URDF("body.urdf")

        # Robot
        length, width, height = 1, 1, 1
        pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[length, width, height])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[length, width, height])
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[length, width, height])

        # End Pyrosim
        pyrosim.End()

    def Create_Brain(self):
        # Start an sdf file
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")  
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")  

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + 3 , weight = self.weights[currentRow][currentColumn])

        # End Pyrosim
        pyrosim.End()
 
    def Mutate(self):
        self.weights[random.randint(0, 2), random.randint(0, 1)] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id