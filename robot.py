from ntpath import join
from sensor import SENSOR
from motor import MOTOR
from world import WORLD
from pyrosim.neuralNetwork import NEURAL_NETWORK
#import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import math

class ROBOT:
    def __init__(self, solutionID, world):
        self.world = world
        self.solutionID = solutionID
        self.robotId = p.loadURDF("body" + str(self.solutionID) + ".urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain" + str(self.solutionID) + ".nndf")
        #os.system("rm brain" + str(self.solutionID) + ".nndf")
        #os.system("rm body" + str(self.solutionID) + ".urdf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, element):
        for sensorInstance in self.sensors.values():
            sensorInstance.Get_Value(element)

    def Act(self, element):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[bytes(jointName, encoding='utf-8')].Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]

        #ballCoordinates = (self.world.get_link_location(0)[0], self.world.get_link_location(0)[1])
        #targetCoordinates = (self.world.get_link_location(1)[0], self.world.get_link_location(1)[1])
        #distance = math.sqrt(math.pow(ballCoordinates[0] - targetCoordinates[0], 2) + math.pow(ballCoordinates[1] - targetCoordinates[1], 2))

        f = open("tmp" + str(self.solutionID) + ".txt", "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()
        os.system("mv tmp" + str(self.solutionID) + ".txt fitness" + str(self.solutionID) + ".txt")