from operator import index, indexOf
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import constants as c
from links import LINK

class CREATURE:
    def __init__(self):
        self.numLinks = np.random.randint(1, 20)
        self.jointList = []
        self.linkConnectionOrder = []

        # Adding our first link with no connections
        newLink = LINK(0)
        newLink.sendFirstLink()
        self.linkList = [newLink]

        # Adding and sending all of our links for the first time
        linkIDTracker = 1
        for i in range (1, self.numLinks):
            newLink = LINK(linkIDTracker)
            newLinkConnectingLink = random.choice(self.linkList)
            connectReturnValue = newLink.connect(newLinkConnectingLink)

            # if the links were successfully connected
            if connectReturnValue != "":

                # record the order of the connections in linkConnectionOrder Array
                self.linkConnectionOrder.append((newLink.id, newLinkConnectingLink.id))

                # add the link into our actual list of link objects
                self.linkList.append(newLink)
                linkIDTracker += 1

                # add the joint to our array of joints
                self.jointList.append(connectReturnValue)

        # Actual number of links (if we try to add a link to an occupied face, we skip it, reducing the number of actual links)
        self.numLinks = linkIDTracker

        # Number of links that have a sensor neuron
        self.sensorLinkCount = 0
        for currentLink in self.linkList:
            if currentLink.isSensor:
                self.sensorLinkCount += 1

        # array of weights number of sensor neurons x number of motor neurons
        self.weights = np.random.rand(self.sensorLinkCount, len(self.jointList))
        self.weights = self.weights * 2 - 1
        

    # remove a link that isn't connected to more than 1 other link (an ending link)
    def removeRandomLink(self):
        #list of links that have exactly one connection
        endLinksList = []

        for i in range(1, self.linkList):
            numConnections = 0
            for j in range(self.linkConnectionOrder):
                if self.linkConnectionOrder[j][0] == i or self.linkConnectionOrder[j][1] == i:
                    numConnections += 1
            if numConnections == 1:
                endLinksList.append[i]

        # so now endLinksList holds all the IDs of the possible remove options
        indexOflinkToRemove = random.choice(endLinksList)

        # we must remove all link connections
        for k in range(self.linkConnectionOrder):
            if self.linkConnectionOrder[k][0] == indexOflinkToRemove or self.linkConnectionOrder[k][1] == indexOflinkToRemove:
                self.linkConnectionOrder.pop(k)


    def addRandomLink(self):
        newLink = LINK(self.numLinks)
        self.linkList.append(newLink)
        connectReturnValue = ""
        while connectReturnValue == "":
            newLinkConnectingLink = random.choice(self.linkList)
            connectReturnValue = newLink.connect(newLinkConnectingLink)
        self.linkConnectionOrder.append((newLink.id, newLinkConnectingLink.id))
        self.numLinks += 1        


    def mutateWeights(self):
        self.weights[random.randint(0, self.sensorLinkCount - 1), random.randint(0, len(self.jointList) - 1)] = random.random() * 2 - 1


    def generateCreatureBodyFile(self):
        # Send the correct links in the correct order and the correct joints 
        self.jointList = []
        self.linkList[0].sendFirstLink()
        for i in range(len(self.linkConnectionOrder)):
            connectReturnValue = self.linkList[self.linkConnectionOrder[i][0]].connect(self.linkList[self.linkConnectionOrder[i][1]])
            self.jointList.append(connectReturnValue)
        
        self.sensorLinkCount = 0
        for currentLink in self.linkList:
            if currentLink.isSensor and self.helper_is_connected(currentLink.id):
                self.sensorLinkCount += 1


    def generateCreatureBrainFile(self):
        # adding sensors
        indicesOfSensorLinks = []
        sensorName = 0
        for i in range(self.linkList):
            if self.linkList[i].isSensor and self.helper_is_connected(self.linkList[i]):
                pyrosim.Send_Sensor_Neuron(name = sensorName, linkName = "Link" + str(i))
                sensorName += 1
                indicesOfSensorLinks.append(i)

        # adding motor neurons at every joint
        for i in range(len(self.jointList)):
            pyrosim.Send_Motor_Neuron(name = self.sensorLinkCount + i, jointName = self.jointList[i])

        # connecting each sensor neuron to all of the motor neurons
        for i in range(self.sensorLinkCount):
            for j in range(len(self.jointList)):
                pyrosim.Send_Synapse( sourceNeuronName = indicesOfSensorLinks[i], targetNeuronName = self.sensorLinkCount + j, weight = self.weights[i, j])


    def helper_is_connected(self, linkId):
        numConnections = 0
        for j in range(self.linkConnectionOrder):
            if self.linkConnectionOrder[j][0] == linkId or self.linkConnectionOrder[j][1] == linkId:
                numConnections += 1
        if numConnections >= 1:
            return True
        else:
            return False
