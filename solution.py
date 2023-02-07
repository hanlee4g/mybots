import os
import pyrosim.pyrosim as pyrosim
import numpy as np
#import simulate
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.myID = nextAvailableID
    
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
        
        pyrosim.Send_Joint( name = "Torso_Head" , parent= "Torso" , child = "Head" , type = "revolute", position = [-0.5,0,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="Head", pos=[-0.5,0,0] , size=[1, 0.2, 0.2])

        pyrosim.Send_Joint( name = "Torso_Butt" , parent= "Torso" , child = "Butt" , type = "revolute", position = [0.5,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Butt", pos=[0.5,0,0] , size=[1, 0.2, 0.2])

        # End Pyrosim
        pyrosim.End()

    def Create_Brain(self):
        # Start an sdf file
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # Worm
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Head")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Butt")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_Head")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_Butt")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])

        # End Pyrosim
        pyrosim.End()


    def Mutate(self):
        self.weights[random.randint(0, c.numSensorNeurons - 1), random.randint(0, c.numMotorNeurons - 1)] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id