import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import constants as c

class LINK:
    def __init__(self, i):
        # integer ID of link
        self.id = i

        # initializing random shape of link
        self.length = np.random.rand() * 3
        self.width = np.random.rand() * 3
        self.height = np.random.rand() * 3

        # 1 if sensor link, 0 if not sensor link
        self.isSensor = np.random.randint(2)
        if self.isSensor == 0:
            self.string1 = "Blue"
            self.string2 = "0 0 1.0 1.0"
        else:
            self.string1 = "Green"
            self.string2 = "0 1.0 0 1.0"

        # 0 if face is open, 1 if face is occupied
        # [positive x, negative x, positive y, negative y, positive z, negative z]
        self.openFaces = np.array([0, 0, 0, 0, 0, 0])

    def sendFirstLink(self):
        # Creating Link
        pyrosim.Send_Cube(name="Link" + str(self.id),
                            pos = [0, 0, 3],
                            size=[self.length, self.width, self.height],
                            string1 = self.string1,
                            string2 = self.string2
                            )

    def connect(self, other):
        self.directionIndex = np.random.randint(6)
        self.randomJointAxis = np.random.randint(3)
        # if there face is already taken, returns 0
        if other.openFaces[self.directionIndex] == 1:
            return 0
        # if the face is not taken, assigning position array.
        else:
            other.openFaces[self.directionIndex] = 1
            if self.directionIndex == 0:
                self.posArray = [self.length / 2.0, 0, 0]
                self.jointPosArray = [self.length, 0, 0]
            elif self.directionIndex == 1:
                self.posArray = [-self.length / 2.0, 0, 0]
                self.jointPosArray = [-self.length, 0, 0]
            elif self.directionIndex == 2:
                self.posArray = [0, self.width / 2.0, 0]
                self.jointPosArray = [0, self.width, 0]
            elif self.directionIndex == 3:
                self.posArray = [0, -self.width / 2.0, 0]
                self.jointPosArray = [0, -self.width, 0]
            elif self.directionIndex == 4:
                self.posArray = [0, 0, self.height / 2.0]
                self.jointPosArray = [0, 0, self.height]
            elif self.directionIndex == 5:
                self.posArray = [0, 0, -self.height / 2.0]
                self.jointPosArray = [0, 0, -self.height]

            # setting random joint axis string
            if self.randomJointAxis == 0:
                self.jointAxis = "1 0 0"
            elif self.randomJointAxis == 1:
                self.jointAxis = "0 1 0"
            else:
                self.jointAxis = "0 0 1"

            # Creating Link
            pyrosim.Send_Cube(name="Link" + str(self.id),
                                pos = self.posArray,
                                size=[self.length, self.width, self.height],
                                string1 = self.string1,
                                string2 = self.string2
                                )
            
            # Creating Joint
            pyrosim.Send_Joint(name = "Link" + str(other.id) + "_Link" + str(self.id),
                                parent= "Link" + str(other.id),
                                child = "Link" + str(self.id),
                                type = "revolute",
                                position = self.jointPosArray,
                                jointAxis = self.jointAxis)

            # if link and joint were created, return 1
            return 1

    def isSensor(self):
        if self.isSensor == 0:
            return False
        else:
            return True