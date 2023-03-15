# The Engineer Final Project
### Completed by [Hanjune Lee](https://www.linkedin.com/in/hanjunelee/) for Northwestern University's [CS396: Artifical Life](https://www.mccormick.northwestern.edu/computer-science/academics/courses/descriptions/396-2.html) course
 I have selected The Engineer pathway for the 44 Point Option. At a high level, I create randomly generated creatures made up of links (rectangular prisms), joints (connections between links), sensor neurons, and motor neurons. Then, I evolve them with random mutations and by replacing parents with better performing children. This project maximizes the distance that the creatures travel within a given time frame.

 ### Table of Contents
 1. [Deliverables](#deliverables)
 2. [Methods](#methods)
 3. [Results](#results)
 4. [Citations](#citations)
 5. [Acknowledgements](#acknowledgements)

---

# Deliverables <a name="deliverables"></a>

### Instructions to run your own simulation
* Set your desired number of generations, population size, and number of random seeds in `constants.py`
* Run `python3 search.py`

### Instructions to run sample simulations
* Choose one of the `sample_x` subdirectories within the `samples` directory
* Run `python3 sample_simulate.py sample_x`
    * For example, if I want to run `sample_1`, I would run `python3 sample_simulate.py sample_1`
* This command runs 3 simulations of creatures from the same lineage: (1) the first randomly generated creature, (2) the same creature after 0.5 * the total number of generations, and (3) the fully evolved version of the creature after all of the generations. These samples represent the evolution of the best performing creature of a population of 10 creatures after 500 generations.
* Please note that the second creature displayed is not necessarily better than the first; it is simply a creature picked out from the middle of the evolutionary chain and may not be a creature that replaces its parent. The third creature, though, is better than the other two since it is the ultimate best performer of all the generations of all the populations given a random seed.

### [10-second Teaser GIF](https://imgur.com/a/jb4GoXY)

### 2-Minute Summary Video: Insert Link Here

---

# Methods <a name="methods"></a>

### What is happening?
At a fundamental, single-unit level, this program creates a creature with a random number of links (rectangular prisms) that are connected to each other randomly with joints. Some of the links have sensor neurons (green links) while some links don't (blue links). All joints have a motor neuron. A neural network is then created that connects each sensor neuron with all of the motor neurons through synapses, with randomly assigned weights.

The initial randomly generated creature tends to have limited movement. We can evolve this creature to optimize on a certain behavior by rewarding good performance on a feedback function. The feedback function that I wrote maximizes the x-direction movement over a set amount of time. Every generation, we randomly mutate the creature and replace parents if the child performs better; possible mutations are synapse weight changes, adding a link, or removing a link. Over many generations, the initial creature can evolve to perform quite well.

We can run simulations with more than one creature in the population so that we can more easily find great performers. In this project, I ran 10 simulations (each with a different random seed) that each had a population size of 10 for 500 generations for a total of 10x10x500 = 50,000 sims.

> **Reminder**: You can run sample simulations with `python3 sample_simulate.py sample_x` or your own simulations with `python3 search.py`

### Program Structure
A basic program architecture of the files and classes that I implemented in this project are listed below. The files in the green box are generally used for the generation of the creatures and their evolution. Think the genotype. The files in the orange box are generally used for the representation of the creatures. Think the phenotype. This is a simplified explanation - the following sections go more in depth.

<div align="center">
  <img src="https://user-images.githubusercontent.com/22042474/225156491-02ec7a0e-9708-47e4-9fae-09a8318eac55.jpg" width="600">
</div>

### Core Data Structure
The core data structure in my project is the linkConnectionOrder array, found in `creature.py`. With the information stored in just this array and my continuous list of every link that has ever been created (including deleted links), I can generate a full creature.

<div align="center">
  <img src="https://user-images.githubusercontent.com/22042474/225160315-d3501bfb-9981-4116-b149-bc4d7f44b933.jpg" width="600">
</div>

There are 7 pieces of information stored in the linkConnectionOrder arrow: (1) the ID of a link, (2) the ID of the link that the first link is connected to, (3) the face on the second link that the first link is connecting to, (4) the relative position of the first link, (5) the relativre position of the joint between the two links, (6) the axis of the joint, and (7) the type of joint. I have a function called directConnect that can take this information and send the correct cube and joint to pyrosim; generating exactly what was stored. From this point forth, I will refer to thelinkConnectionOrder array as a sequence array that connects two links for simplicity.

### Body Generation
<div align="center">
  <img src="https://user-images.githubusercontent.com/22042474/222037758-58c9fdf1-f4b2-4d95-9e28-674067b2a771.jpeg" width="600">
</div>

As pictured in this diagram, bodies are built by placing one link at a time onto an open face. Links are placed at random on one of the open faces of any of the pre-existing links. In this diagram, there is one link with no existing connections. Thus, an additional link can be placed on any of its six faces. The rule of open faces extends to all numbers of links.

The code for body generation can be found in `creature.py` and is also listed below.
```
    def generateCreatureBodyFile(self):
        self.jointList = []
            self.linkList[0].sendFirstLink()
            for i in range(len(self.linkConnectionOrder)):
                connectReturnValue = self.linkList[self.linkConnectionOrder[i][0]].directConnect(self.linkList[self.linkConnectionOrder[i][1]], self.linkConnectionOrder[i][2], self.linkConnectionOrder[i][3], self.linkConnectionOrder[i][4], self.linkConnectionOrder[i][5], self.linkConnectionOrder[i][6])
                self.jointList.append(connectReturnValue[0])
            self.sensorLinkCount = 0
            for currentLink in self.linkList:
                if currentLink.isSensor and self.helper_is_connected(currentLink.id):
                    self.sensorLinkCount += 1
```

### Brain Generation
<div align="center">
  <img src="https://user-images.githubusercontent.com/22042474/222037903-7ab58094-5fda-4ec1-9c6e-7390d353a33a.jpeg" width="700">
</div>

As pictured in this 2D depiction, brains are built by placing a sensor neuron on every green link. Each of those sensor neuron is then connected to every motor (one for each joint). I then assign random weights to every joint. Blue links are not assigned a sensor neuron and thus not connected to any motors. The same holds for the 3D representation.

The brain / neural network is created the same way every time. The code to create the neural network can be found in `creature.py` and is listed below. I create a list of all of the links with sensors and then I use that list to create all sensor neurons. I create all motor neurons through the list of all joints I have stored from the body generation. I then connect all of the sensor neurons with all of the motor neurons that I created.

```
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
```

### Evolution
<div align="center">
  <img src="https://user-images.githubusercontent.com/22042474/222037830-7cc174b0-e37e-4d12-87b2-7bfd97d48e7a.jpeg" width="600">
</div>

This 2D diagram represents my mutation function. Every generation, I mutate each parent to create a child who I then compare to the parent to see who's fitness score is better. There are three types of mutations. First, I can randomly remove a link that has exactly one connection. I limit this to links with exactly one connection so as to not remove links that would leave a link disconnected from the rest of the creature and to not remove the original link. Second, I can add a link to a random open face. Third, I can change the weights. When I run my mutate function, I always mutate the weights. I then do one of the three things at random: (1) remove a link, (2) add a link, or (3) do nothing. The sequence array in the diagram represents how easy it is for me to add links and to track which links that I can remove - it is a simplified representation of the aforementioned linkConnectionOrder array. The body mutation code is below and can be found in `solution.py`.

```
def Mutate(self):
    self.creature.mutateWeights()
    add_or_remove = random.randint(0, 3)
    if add_or_remove == 0:
        if len(self.creature.linkConnectionOrder) < c.maxLinks:
            self.creature.addRandomLink()
        else:
            remove_or_nothing = random.randint(0,2)
            if remove_or_nothing == 0 and len(self.creature.linkConnectionOrder) > 1:
                self.creature.removeRandomLink()
    elif add_or_remove == 1:
        if len(self.creature.linkConnectionOrder) > 1:
            self.creature.removeRandomLink()
        else:
            add_or_nothing = random.randint(0,2)
            if add_or_nothing == 0 and len(self.creature.linkConnectionOrder) < c.maxLinks:
                self.creature.addRandomLink()
```

The following diagram shows the sequence through which the mutation occurs and the functions of my body generation and brain generation functions. The brain evolution can be thought of as the last step in the mutation; it takes in the modified sequence array and the mutated weights, and the body that was created from the two, and then sends all the sensor neurons, motor neurons, and synapses. All of the evolution work is done on the sequence array and the weights; the way we generate the brain does not change. In this example, the sequence array represents a simplified version of the linkConnectionOrder array.

<div align="center">
  <img src="https://user-images.githubusercontent.com/22042474/222037979-1751ab23-25ef-4216-96d1-f60ee76cfcc0.jpeg" width="600">
</div>

### Selection
I use a parallel hill climbing algorithm for my evolution and selection. The hill climbing algorithm is a greedy algorithm that seeks to optimize the results of our feedback function (in this case, the total x distance in an allotted timeframe). The parallel version of the hill climbing algorithm just means that several lineages of creatures happen simultaneously. We run several in parallel to improve our chances of evolving a creature that performs well.

More specifically, my parallel hill climber works by creating x number of initial creatures. Every generation, all x creatures are randomly mutated using the methods described in the previous section. If a child has better fitness than its parent, it replaces the parent within the parent array. Otherwise, the parent remains. This process is repeated and we slowly "hill climb" and achieve creatures with better performance according to the feedback function. The code for this algorithm can be found in `parallelHillClimber.py`. The snippet from that class for selection is listed below.

```
def Select(self):
    for i in self.parents:
        if self.parents[i].fitness > self.children[i].fitness:
            self.parents[i] = self.children[i]
```

### Genotype -> Phenotype
The cartoon below depicts the genotype-to-phenotype map (how brains/bodies are encoded and expressed to form a robot).

<div align="center">
  <img src="https://user-images.githubusercontent.com/22042474/225167626-c624ad42-cbd4-41dd-8d86-14f4021ce58a.jpeg" width="650">
</div>

The generation files (`creature.py`, `links.py`, `parallelHillClimber.py`, `solution.py` and `search.py`) all work to write creatures into two files: (1) a `body.urdf` file and (2) a `brain.nndf` file. This is the genotype. As depicted in the cartoon, the `body.urdf` file stores information about all of the links in a creature and all of the joints that connect the links. The `brain.nndf` file stores information about which links have sensor neurons and which joints have motor neurons. It also contains information about all the synapses (connections) between sensor neurons and motor neurons along with the corresponding weights. The `robot.py` file reads in these two files and creates the phenotype representation; with the help of `sensor.py` and `motor.py`, we are able to simulate what the robot looks like and how it acts within an environment (`world.py`). We can view the phenotype by running the simulation with a GUI or we can run it in the background with a Direct command.

### Morphospace
All body shapes and rotational movements between blocks are possible. Every new block that is added can be added to any open side of any pre-existing block already in the simulation. This is currently randomly determined. All rotational movements are possible; all joints are either revolute, floating, or continuous.

In terms of the brain, all sensor blocks (green) are connected to every single motor (one for each join) with randomly assigned weights. We will adjust these weights when we evolve our creatures in future assignments. Additionally, a sensor on one side of the body can affect a motor on the other side.

---

# Results <a name="results"></a>

### Findings
Plot

What did I find

In general, how did bodies/brains/behavior change over time?

### Example #1

### Example #2

### Example #3

### Additional Analysis

### Conclusion

---

## Citations <a name="citations"></a>
* [r/ludobots](https://www.reddit.com/r/ludobots/)
* [Pyrosim library](https://ccappelle.github.io/pyrosim/)

## Acknowledgements <a name="acknowledgements"></a>
Thank you to this course's instructor, Professor [Sam Kriegman](https://www.mccormick.northwestern.edu/research-faculty/directory/profiles/kriegman-sam.html) for his guidance and instruction. He is involved in groundbreaking research that is definitely worth a [read](https://skriegman.github.io/)! Additionally, thank you to TA [Donna Hooshmand](http://donnahooshmand.com/) and PM [Jack Burkhardt](https://jackburkhardt.com/) for all of the help throughout the course!
