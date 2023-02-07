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

        # End Pyrosim
        pyrosim.End()

    def Create_Body(self):
        # Start an sdf file
        pyrosim.Start_URDF("body.urdf")

        # Robot
        length, width, height = 3, 1, 1
        pyrosim.Send_Cube(name="Torso", pos=[0,0,3] , size=[length, width, height])

        pyrosim.Send_Joint( name = "Torso_LeftLeg1" , parent= "Torso" , child = "LeftLeg1" , type = "revolute", position = [-1,-0.5,3], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLeg1", pos=[0,-0.5,0] , size=[0.2, 1, 0.2])

        pyrosim.Send_Joint( name = "Torso_RightLeg1" , parent= "Torso" , child = "RightLeg1" , type = "revolute", position = [-1,0.5,3], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLeg1", pos=[0,0.5,0] , size=[0.2, 1, 0.2])

        pyrosim.Send_Joint( name = "Torso_LeftLeg2" , parent= "Torso" , child = "LeftLeg2" , type = "revolute", position = [0,-0.5,3], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLeg2", pos=[0,-0.5,0] , size=[0.2, 1, 0.2])

        pyrosim.Send_Joint( name = "Torso_RightLeg2" , parent= "Torso" , child = "RightLeg2" , type = "revolute", position = [0,0.5,3], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLeg2", pos=[0,0.5,0] , size=[0.2, 1, 0.2])

        pyrosim.Send_Joint( name = "Torso_LeftLeg3" , parent= "Torso" , child = "LeftLeg3" , type = "revolute", position = [1,-0.5,3], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLeg3", pos=[0,-0.5,0] , size=[0.2, 1, 0.2])

        pyrosim.Send_Joint( name = "Torso_RightLeg3" , parent= "Torso" , child = "RightLeg3" , type = "revolute", position = [1,0.5,3], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLeg3", pos=[0,0.5,0] , size=[0.2, 1, 0.2])

        pyrosim.Send_Joint( name = "Torso_Tail" , parent= "Torso" , child = "Tail" , type = "revolute", position = [1,0,3], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Tail", pos=[1,0,0] , size=[2, 0.4, 0.2])

        pyrosim.Send_Joint( name = "RightLeg1_RightLowerLeg1" , parent= "RightLeg1" , child = "RightLowerLeg1" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLowerLeg1", pos=[0,0,-0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint( name = "LeftLeg1_LeftLowerLeg1" , parent= "LeftLeg1" , child = "LeftLowerLeg1" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLowerLeg1", pos=[0,0,-0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint( name = "RightLeg2_RightLowerLeg2" , parent= "RightLeg2" , child = "RightLowerLeg2" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLowerLeg2", pos=[0,0,-0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint( name = "LeftLeg2_LeftLowerLeg2" , parent= "LeftLeg2" , child = "LeftLowerLeg2" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLowerLeg2", pos=[0,0,-0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint( name = "RightLeg3_RightLowerLeg3" , parent= "RightLeg3" , child = "RightLowerLeg3" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightLowerLeg3", pos=[0,0,-0.5] , size=[0.2, 0.2, 1])

        pyrosim.Send_Joint( name = "LeftLeg3_LeftLowerLeg3" , parent= "LeftLeg3" , child = "LeftLowerLeg3" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftLowerLeg3", pos=[0,0,-0.5] , size=[0.2, 0.2, 1])

        # End Pyrosim
        pyrosim.End()

    def Create_Brain(self):
        # Start an sdf file
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LeftLeg1")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "RightLeg1")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg2")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg2")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "LeftLeg2")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "RightLeg2")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "Tail")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "LeftLowerLeg1")
        pyrosim.Send_Sensor_Neuron(name = 9 , linkName = "RightLowerLeg1")
        pyrosim.Send_Sensor_Neuron(name = 10 , linkName = "LeftLowerLeg2")
        pyrosim.Send_Sensor_Neuron(name = 11 , linkName = "RightLowerLeg2")
        pyrosim.Send_Sensor_Neuron(name = 12 , linkName = "LeftLowerLeg2")
        pyrosim.Send_Sensor_Neuron(name = 13 , linkName = "RightLowerLeg2")

        pyrosim.Send_Motor_Neuron( name = 14 , jointName = "Torso_LeftLeg1")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "Torso_RightLeg1")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "Torso_LeftLeg2")
        pyrosim.Send_Motor_Neuron( name = 17 , jointName = "Torso_RightLeg2")
        pyrosim.Send_Motor_Neuron( name = 18 , jointName = "Torso_LeftLeg3")
        pyrosim.Send_Motor_Neuron( name = 19 , jointName = "Torso_RightLeg3")
        pyrosim.Send_Motor_Neuron( name = 20 , jointName = "Torso_Tail")
        pyrosim.Send_Motor_Neuron( name = 21 , jointName = "LeftLeg1_LeftLowerLeg1")
        pyrosim.Send_Motor_Neuron( name = 22 , jointName = "RightLeg1_RightLowerLeg1")
        pyrosim.Send_Motor_Neuron( name = 23 , jointName = "LeftLeg2_LeftLowerLeg2")
        pyrosim.Send_Motor_Neuron( name = 24 , jointName = "RightLeg2_RightLowerLeg2")
        pyrosim.Send_Motor_Neuron( name = 25 , jointName = "LeftLeg3_LeftLowerLeg3")
        pyrosim.Send_Motor_Neuron( name = 26 , jointName = "RightLeg3_RightLowerLeg3")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])

        # End Pyrosim
        pyrosim.End()
 
    def Mutate(self):
        self.weights[random.randint(0, c.numSensorNeurons - 1), random.randint(0, c.numMotorNeurons - 1)] = random.random() * 2 - 1

    def Set_ID(self, id):
        self.myID = id