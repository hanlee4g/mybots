import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(c.iterations)

    def Get_Value(self, element):
        self.values[element] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if element == c.iterations - 1:
            self.Save_Values()

    def Save_Values(self):
        np.save("./data/sensor-" + self.linkName + ".npy", self.values)