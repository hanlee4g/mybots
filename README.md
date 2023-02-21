# CS396: Artificial Life Ludobots (Assignment #7)
###### In this assignment, I expanded the snake from Assignment #7 to 3 dimensions. Green blocks have sensors and Blue blocks don't have sensors. Currently, the block sizes, joint locations, presence of sensor, and motor weights are all randomly determined.

## Video
https://youtu.be/EN4MRTILS6g

## To Run (Button):
python3 search.py

## Body Generation:
![IMG_0050](https://user-images.githubusercontent.com/22042474/220227572-204d466c-ece1-4970-94c2-3ddbe892966b.jpg)

As pictured in this diagram, bodies are built by placing blocks one at a time. Each block can be placed on any of the open faces of any of the pre-exisiting blocks already in the simulation.

'''python
linkIDTracker = 1
        for i in range (1, self.numLinks):
            newLink = LINK(linkIDTracker)
            connectReturnValue = newLink.connect(random.choice(linkList))
            if connectReturnValue != "":
                linkList.append(newLink)
                linkIDTracker += 1
                self.jointList.append(connectReturnValue)
'''

I created a separate class for each Link and a method called connect that connects two links with the proper joint. In the code above (in solution.py) I create links and connect the valid ones until the for loop is complete.

## Brain Generation:
![IMG_0051](https://user-images.githubusercontent.com/22042474/220227592-4287f03a-50d4-4369-ad41-a70162fad6f4.jpg)

As pictured in this diagram, brains are built by placing a sensor neuron on every green block. Each sensor neuron is then connected to every motor (one for each joint).

'''python
# adding sensors
        for i in range(self.sensorLinkCount):
            pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link" + str(i))

        # adding motor neurons at every joint
        for i in range(len(self.jointList)):
            pyrosim.Send_Motor_Neuron(name = self.sensorLinkCount + i, jointName = self.jointList[i])

        # connecting each sensor neuron to all of the motor neurons
        for i in range(self.sensorLinkCount):
            for j in range(len(self.jointList)):
                pyrosim.Send_Synapse( sourceNeuronName = i, targetNeuronName = self.sensorLinkCount + j, weight = self.weights[i, j])
'''

In the code above, I add a sensor at every link that requires a sensor and a motor neuron at every joint. Then, I sent a synapse from each sensor neuron to every motor neuron.

## Morphospace
All body shapes and rotational movements between blocks are possible. Every new block that is added can be added to any open side of any pre-existing block already in the simulation. This is currently randomly determined. All rotational movements are possible; all joints are rotational joints right now, without randomly assigned joint axes.

In terms of the brain, all sensor blocks (green) are connected to every single motor (one for each join) with randomly assigned weights. We will adjust these weights when we evolve our creatures in future assignments. Yes, a snesor on one side of the body can affect a motor on the other side.

## Citation
This project is built on top of r/ludobots and pyrosim
