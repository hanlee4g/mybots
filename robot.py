from sensor import SENSOR
from motor import MOTOR
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim

class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

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
        for motorInstance in self.motors.values():
            motorInstance.Set_Value(self.robotId, element)