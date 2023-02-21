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
        self.openFaces = [0, 0, 0, 0, 0, 0]

    def sendFirstLink(self):
        # Creating Link
        pyrosim.Send_Cube(name="Link" + str(self.id),
                            pos = [0, 0, 3],
                            size=[self.length, self.width, self.height],
                            string1 = self.string1,
                            string2 = self.string2
                            )
        
        # setting pos array at origin +3 in z direction
        self.posArray = [0, 0, 3]

    # sends Link to Pyrosim and sends Joint to Pyrosim that connects self and other Links
    def connect(self, other):
        self.directionIndex = np.random.randint(6)
        self.randomJointAxis = np.random.randint(3)
        # if there face is already taken, returns 0
        if other.openFaces[self.directionIndex] == 1:
            return 0
        # if the face is not taken, assigning position array.
        else:
            ### other link's previous relative position ###
            # 6 if other link is the 1st link
            # 0 if other link grew in positive length-direction (x)
            # 1 if other link grew in negative length-direction (-x)
            # 2 if other link grew in positive width-direction (y)
            # 3 if other link grew in negative width-direction (-y)
            # 4 if other link grew in positive height-direction (z)
            # 5 if other link grew in negative height-direction (-z)

            if other.posArray == [0, 0, 3]:
                jointPosIndicator = 6
            elif other.posArray[0] > 0:
                jointPosIndicator = 0
            elif other.posArray[0] < 0:
                jointPosIndicator = 1
            elif other.posArray[1] > 0:
                jointPosIndicator = 2
            elif other.posArray[1] < 0:
                jointPosIndicator = 3
            elif other.posArray[2] > 0:
                jointPosIndicator = 4
            elif other.posArray[2] < 0:
                jointPosIndicator = 5

            other.setFaceToUsed(self.directionIndex)

            # If growing in positive length-direction (x)
            if self.directionIndex == 0:
                self.posArray = [self.length / 2.0, 0, 0]
                if jointPosIndicator == 6:
                    self.jointPosArray = [other.length / 2.0, 0, 3]
                elif jointPosIndicator == 0:
                    self.jointPosArray = [other.length, 0, 0]
                elif jointPosIndicator == 1:
                    return 0
                elif jointPosIndicator == 2:
                    self.jointPosArray = [other.length / 2.0, other.width / 2.0, 0]
                elif jointPosIndicator == 3:
                    self.jointPosArray = [other.length / 2.0, -other.width / 2.0, 0]
                elif jointPosIndicator == 4:
                    self.jointPosArray = [other.length / 2.0, 0, other.height / 2.0]
                elif jointPosIndicator == 5:
                    self.jointPosArray = [other.length / 2.0, 0, -other.height / 2.0]

            # If growing in negative length-direction (-x)
            elif self.directionIndex == 1:
                self.posArray = [-self.length / 2.0, 0, 0]
                if jointPosIndicator == 6:
                    self.jointPosArray = [-other.length / 2.0, 0, 3]
                elif jointPosIndicator == 0:
                    return 0
                elif jointPosIndicator == 1:
                    self.jointPosArray = [-other.length, 0, 0]
                elif jointPosIndicator == 2:
                    self.jointPosArray = [-other.length / 2.0, other.width / 2.0, 0]
                elif jointPosIndicator == 3:
                    self.jointPosArray = [-other.length / 2.0, -other.width / 2.0, 0]
                elif jointPosIndicator == 4:
                    self.jointPosArray = [-other.length / 2.0, 0, other.height / 2.0]
                elif jointPosIndicator == 5:
                    self.jointPosArray = [-other.length / 2.0, 0, -other.height / 2.0]

            # If growing in positive width-direction (y)
            elif self.directionIndex == 2:
                self.posArray = [0, self.width / 2.0, 0]
                if jointPosIndicator == 6:
                    self.jointPosArray = [0, other.width / 2.0, 3]
                elif jointPosIndicator == 0:
                    self.jointPosArray = [other.length / 2.0, other.width / 2.0, 0]
                elif jointPosIndicator == 1:
                    self.jointPosArray = [-other.length / 2.0, other.width / 2.0, 0]
                elif jointPosIndicator == 2:
                    self.jointPosArray = [0, other.width, 0]
                elif jointPosIndicator == 3:
                    return 0
                elif jointPosIndicator == 4:
                    self.jointPosArray = [0, other.width / 2.0, other.height / 2.0]
                elif jointPosIndicator == 5:
                    self.jointPosArray = [0, other.width / 2.0, -other.height / 2.0]

            # If growing in negative width-direction (-y)
            elif self.directionIndex == 3:
                self.posArray = [0, -self.width / 2.0, 0]
                if jointPosIndicator == 6:
                    self.jointPosArray = [0, -other.width / 2.0, 3]
                elif jointPosIndicator == 0:
                    self.jointPosArray = [other.length / 2.0, -other.width / 2.0, 0]
                elif jointPosIndicator == 1:
                    self.jointPosArray = [-other.length / 2.0, -other.width / 2.0, 0]
                elif jointPosIndicator == 2:
                    return 0
                elif jointPosIndicator == 3:
                    self.jointPosArray = [0, -other.width, 0]
                elif jointPosIndicator == 4:
                    self.jointPosArray = [0, -other.width / 2.0, other.height / 2.0]
                elif jointPosIndicator == 5:
                    self.jointPosArray = [0, -other.width / 2.0, -other.height / 2.0]

            # If growing in positive height-direction (z)
            elif self.directionIndex == 4:
                self.posArray = [0, 0, self.height / 2.0]
                if jointPosIndicator == 6:
                    self.jointPosArray = [0, 0, other.height / 2.0 + 3]
                elif jointPosIndicator == 0:
                    self.jointPosArray = [other.length / 2.0, 0, other.height / 2.0]
                elif jointPosIndicator == 1:
                    self.jointPosArray = [-other.length / 2.0, 0, other.height / 2.0]
                elif jointPosIndicator == 2:
                    self.jointPosArray = [0, other.width / 2.0, other.height / 2.0]
                elif jointPosIndicator == 3:
                    self.jointPosArray = [0, -other.width / 2.0, other.height / 2.0]
                elif jointPosIndicator == 4:
                    self.jointPosArray = [0, 0, other.height]
                elif jointPosIndicator == 5:
                    # should not reach this case
                    return 0

            # If growing in negative height-direction (-z)
            elif self.directionIndex == 5:
                self.posArray = [0, 0, -self.height / 2.0]
                if jointPosIndicator == 6:
                    self.jointPosArray = [0, 0, -other.height / 2.0 + 3]
                elif jointPosIndicator == 0:
                    self.jointPosArray = [other.length / 2.0, 0, -other.height / 2.0]
                elif jointPosIndicator == 1:
                    self.jointPosArray = [-other.length / 2.0, 0, -other.height / 2.0]
                elif jointPosIndicator == 2:
                    self.jointPosArray = [0, other.width / 2.0, -other.height / 2.0]
                elif jointPosIndicator == 3:
                    self.jointPosArray = [0, -other.width / 2.0, -other.height / 2.0]
                elif jointPosIndicator == 4:
                    return 0
                elif jointPosIndicator == 5:
                    self.jointPosArray = [0, 0, -other.height]

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

    # returns true if the link is a sensor, false if it is not
    def isSensor(self):
        if self.isSensor == 0:
            return False
        else:
            return True

    # sets openFaces to 1 (used) for a given index
    def setFaceToUsed(self, index):
        self.openFaces[index] = 1