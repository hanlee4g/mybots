import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        self.amplitude = c.backLegAmplitude
        self.offset = c.backLegPhaseOffset
        if self.jointName == b"Torso_BackLeg":
            self.frequency = c.backLegFrequency / 2
        else:
            self.frequency = c.backLegFrequency

        self.motorValues = self.amplitude * np.sin(self.frequency * np.linspace(0, 2*np.pi, c.iterations) + self.offset)

    def Set_Value(self, robot, element):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robot,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motorValues[element],
            maxForce = c.maxForce)
        if element == c.iterations - 1:
            self.Save_Values()

    def Save_Values(self):
        np.save("./data/motor-" + self.jointName + ".npy", self.motorValues)