from operator import index, indexOf
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import constants as c
from links import LINK

class CREATURE:
    def __init__(self):
        self.numLinks = np.random.randint(2, c.maxLinks - 1)
        self.jointList = []
        self.linkConnectionOrder = []

        # Adding our first link with no connections
        newLink = LINK(0)
        #newLink.sendFirstLink()
        newLink.setFirstLink()
        self.linkList = [newLink]

        # Adding and sending all of our links for the first time
        linkIDTracker = 1
        for i in range (1, self.numLinks):
            newLink = LINK(linkIDTracker)
            newLinkConnectingLink = random.choice(self.linkList)
            connectReturnValue = newLink.checkConnect(newLinkConnectingLink)

            # if the links were successfully connected
            if connectReturnValue[0] != "":

                # record the order of the connections in linkConnectionOrder Array
                self.linkConnectionOrder.append((newLink.id, newLinkConnectingLink.id, connectReturnValue[1], connectReturnValue[2], connectReturnValue[3], connectReturnValue[4], connectReturnValue[5]))

                # add the link into our actual list of link objects
                self.linkList.append(newLink)
                linkIDTracker += 1

                # add the joint to our array of joints
                self.jointList.append(connectReturnValue[0])

        # Actual number of links (if we try to add a link to an occupied face, we skip it, reducing the number of actual links)
        self.numLinks = linkIDTracker

        # Number of links that have a sensor neuron
        self.sensorLinkCount = 0
        for currentLink in self.linkList:
            if currentLink.isSensor:
                self.sensorLinkCount += 1

        # array of weights number of sensor neurons x number of motor neurons
        #self.weights = np.random.rand(self.sensorLinkCount, len(self.jointList))
        self.weights = np.random.rand(100, 100)
        self.weights = self.weights * 2 - 1        

    # remove a link that isn't connected to more than 1 other link (an ending link)
    def removeRandomLink(self):
        #list of links that have exactly one connection
        endLinksList = []

        for i in range(1, len(self.linkList)):
            numConnections = 0
            for j in range(len(self.linkConnectionOrder)):
                if self.linkConnectionOrder[j][0] == i or self.linkConnectionOrder[j][1] == i:
                    numConnections += 1
            if numConnections == 1:
                endLinksList.append(i)

        # so now endLinksList holds all the IDs of the possible remove options
        indexOflinkToRemove = random.choice(endLinksList)

        # we must remove all link connections
        for k in range(len(self.linkConnectionOrder)):
            if self.linkConnectionOrder[k][0] == indexOflinkToRemove or self.linkConnectionOrder[k][1] == indexOflinkToRemove:
                self.linkConnectionOrder.pop(k)
                break


    def addRandomLink(self):
        newLink = LINK(self.numLinks)
        connectReturnValue = [""]
        while connectReturnValue[0] == "":
            existingLinks = []
            for i in range(len(self.linkConnectionOrder)):
                if self.linkConnectionOrder[i][0] not in existingLinks:
                    existingLinks.append(self.linkConnectionOrder[i][0])
                if self.linkConnectionOrder[i][1] not in existingLinks:
                    existingLinks.append(self.linkConnectionOrder[i][1])

            newLinkConnectingLink = self.linkList[random.choice(existingLinks)]

            connectReturnValue = newLink.checkConnect(newLinkConnectingLink)

        self.linkConnectionOrder.append((newLink.id, newLinkConnectingLink.id, connectReturnValue[1], connectReturnValue[2], connectReturnValue[3], connectReturnValue[4], connectReturnValue[5]))
        self.linkList.append(newLink)
        self.numLinks += 1


    def mutateWeights(self):
        self.weights[random.randint(0, self.sensorLinkCount + 1), random.randint(0, len(self.jointList) + 1)] = random.random() * 2 - 1


    def generateCreatureBodyFile(self):

        # Send the correct links in the correct order and the correct joints 
        self.jointList = []
        self.linkList[0].sendFirstLink()
        for i in range(len(self.linkConnectionOrder)):
            connectReturnValue = self.linkList[self.linkConnectionOrder[i][0]].directConnect(self.linkList[self.linkConnectionOrder[i][1]], self.linkConnectionOrder[i][2], self.linkConnectionOrder[i][3], self.linkConnectionOrder[i][4], self.linkConnectionOrder[i][5], self.linkConnectionOrder[i][6])
            self.jointList.append(connectReturnValue[0])

        self.sensorLinkCount = 0
        for currentLink in self.linkList:
            if currentLink.isSensor and self.helper_is_connected(currentLink.id):
                self.sensorLinkCount += 1



    def generateCreatureBrainFile(self):
        existingLinks = []
        for i in range(len(self.linkConnectionOrder)):
            if self.linkConnectionOrder[i][0] not in existingLinks:
                existingLinks.append(self.linkConnectionOrder[i][0])
            if self.linkConnectionOrder[i][1] not in existingLinks:
                existingLinks.append(self.linkConnectionOrder[i][1])

        # adding sensors
        listOfSensorLinks = []
        for i in range(len(self.linkList)):
            if self.linkList[i].isSensor and i in existingLinks:
                listOfSensorLinks.append(i)

        for i in range(self.sensorLinkCount):
            pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link" + str(listOfSensorLinks[i]))

        # adding motor neurons at every joint
        for i in range(len(self.jointList)):
            pyrosim.Send_Motor_Neuron(name = self.sensorLinkCount + i, jointName = self.jointList[i])

        # connecting each sensor neuron to all of the motor neurons
        for i in range(self.sensorLinkCount):
            for j in range(len(self.jointList)):
                pyrosim.Send_Synapse( sourceNeuronName = i, targetNeuronName = self.sensorLinkCount + j, weight = self.weights[i, j])


    def helper_is_connected(self, linkId):
        numConnections = 0
        for j in range(len(self.linkConnectionOrder)):
            if self.linkConnectionOrder[j][0] == linkId or self.linkConnectionOrder[j][1] == linkId:
                numConnections += 1
        if numConnections >= 1:
            return True
        else:
            return False
