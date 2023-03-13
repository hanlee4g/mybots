# The Engineer Final Project
### Completed by [Hanjune Lee](https://www.linkedin.com/in/hanjunelee/) for Northwestern University's [CS396: Artifical Life](https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/396-2.html) course
 I have selected The Engineer pathway. At a high level, I create randomly generated creatures made up of links (rectangular prisms), joints (connections between links), sensor neurons, and motor neurons. Then, I evolve them with random mutations and by replacing parents with better performing children. This project maximizes the distance that the creatures travel.

 ### Table of Contents
 1. [Deliverables](#deliverables)
 2. [Methods](#methods)
 3. [Results](#results)
 4. [Citations](#citations)
 5. [Acknowledgements](#acknowledgements)

---

# Deliverables <a name="deliverables"></a>

### Instructions to run your own simulation
* Set your desired number of generations and population size in `constants.py`
* Run `python3 search.py`

### Instructions to run sample simulations
* Insert instructions here

### 10-second Teaser GIF: Insert Link Here

### 2-Minute Summary Video: Insert Link Here

---

# Methods <a name="methods"></a>

## Body Generation:
![IMG_76C58B857164-1 2](https://user-images.githubusercontent.com/22042474/222037758-58c9fdf1-f4b2-4d95-9e28-674067b2a771.jpeg)
As pictured in this diagram, bodies are built by placing one link at a time onto an open face. Links are placed at random on one of the open faces of any of the pre-existing links. In this diagram, there is one link with no existing connections. Thus, an additional link can be placed on any of its six faces. The rule of open faces extends to all numbers of links.

Entire bodies are built through a class called Creature. The core of the Creature class is an array of tuples that records all connections in the order that they are connected. The code to create the Creature and the array of connections the first time is shown below. Later iterations will be described in a future section.
```
    self.numLinks = np.random.randint(3, 8)
    self.jointList = []
    self.linkConnectionOrder = []
    newLink = LINK(0)
    newLink.setFirstLink()
    self.linkList = [newLink]

    linkIDTracker = 1
    for i in range (1, self.numLinks):
        newLink = LINK(linkIDTracker)
        newLinkConnectingLink = random.choice(self.linkList)
        connectReturnValue = newLink.checkConnect(newLinkConnectingLink)
        if connectReturnValue[0] != "":
            self.linkConnectionOrder.append((newLink.id, newLinkConnectingLink.id, connectReturnValue[1], connectReturnValue[2], connectReturnValue[3], connectReturnValue[4]))
            self.linkList.append(newLink)
            linkIDTracker += 1
            self.jointList.append(connectReturnValue[0])
```

## Brain Generation:
![IMG_A6B1A7CEE9DC-1](https://user-images.githubusercontent.com/22042474/222037903-7ab58094-5fda-4ec1-9c6e-7390d353a33a.jpeg)
As pictured in this 2D depiction, brains are built by placing a sensor neuron on every green link. Each of those sensor neuron is then connected to every motor (one for each joint). I then assign random weights to every joint. Blue links are not assigned a sensor neuron and thus not connected to any motors. The same holds for the 3D representation.

The brain / neural network is created the same way every time (no special treatment for the first initialization. The code to create the neural net is below. I create a list of all of the links with sensors and then I use that list to create all sensor neurons. I create all motor neurons through the list of all joints I have stored from the body generation. I then connect all of the sensor neurons with all of the motor neurons that I created.
```
    listOfSensorLinks = []
    for i in range(len(self.linkList)):
        if self.linkList[i].isSensor:
            listOfSensorLinks.append(i)

    for i in range(self.sensorLinkCount):
        pyrosim.Send_Sensor_Neuron(name = i, linkName = "Link" + str(listOfSensorLinks[i]))

    for i in range(len(self.jointList)):
        pyrosim.Send_Motor_Neuron(name = self.sensorLinkCount + i, jointName = self.jointList[i])

    for i in range(self.sensorLinkCount):
        for j in range(len(self.jointList)):
            pyrosim.Send_Synapse( sourceNeuronName = i, targetNeuronName = self.sensorLinkCount + j, weight = self.weights[i, j])
```

## Body Evolution:
![IMG_74F63B4D8CC4-1](https://user-images.githubusercontent.com/22042474/222037830-7cc174b0-e37e-4d12-87b2-7bfd97d48e7a.jpeg)
This 2D diagram represents my mutation function. Every generation, I mutate each parent to create a child who I then compare to the parent to see who's fitness score is better. There are three types of mutations. First, I can randomly remove a link that has exactly one connection. I limit this to links with exactly one connection so as to not remove links that would leave a link disconnected from the rest of the creature and to not remove the original link. Second, I can add a link to a random open face. Third, I can change the weights. When I run my mutate function, I always mutate the weights. I then do one of the three things at random: (1) remove a link, (2) add a link, or (3) do nothing. The sequence array in the diagram represents how easy it is for me to add links and to track which links that I can remove. The body mutation code is below.
```
    self.creature.mutateWeights()
    add_or_remove = random.randint(0, 3)
    if add_or_remove == 0:
        self.creature.addRandomLink()
    elif add_or_remove == 1:
        if len(self.creature.linkConnectionOrder) > 1:
            self.creature.removeRandomLink()
        else:
            add_or_nothing = random.randint(0,2)
            if add_or_nothing == 0:
                self.creature.addRandomLink()
```

## Brain Evolution:
![IMG_DA946DEA76A2-1](https://user-images.githubusercontent.com/22042474/222037979-1751ab23-25ef-4216-96d1-f60ee76cfcc0.jpeg)
The diagram above shows the sequence through which the mutation occurs and the functions of my body generation and brain generation functions. The brain evolution can be thought of as the last step in the mutation; it takes in the modified sequence array and the mutated weights, and the body that was created from the two, and then sends all the sensor neurons, motor neurons, and synapses. All of the evolution work is done on the sequence array and the weights; the way we generate the brain does not change.

## Morphospace
All body shapes and rotational movements between blocks are possible. Every new block that is added can be added to any open side of any pre-existing block already in the simulation. This is currently randomly determined. All rotational movements are possible; all joints are rotational joints right now, with randomly assigned joint axes.

In terms of the brain, all sensor blocks (green) are connected to every single motor (one for each join) with randomly assigned weights. We will adjust these weights when we evolve our creatures in future assignments. Yes, a sensor on one side of the body can affect a motor on the other side.

---

# Results <a name="results"></a>

---

## Citations <a name="citations"></a>
* r/ludobots
* Pyrosim library

## Acknowledgements <a name="acknowledgements"></a>
Thank you to this course's instructor, [Professor Sam Kriegman](https://www.mccormick.northwestern.edu/research-faculty/directory/profiles/kriegman-sam.html) for his guidance and instruction. He is involved in groundbreaking research that is definitely worth a [read](https://skriegman.github.io/)!