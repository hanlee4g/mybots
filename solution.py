from math import frexp
import os
import pyrosim.pyrosim as pyrosim
import numpy as np
#import simulate
import random
import time
import constants as c
from creature import CREATURE

class SOLUTION:
    def __init__(self, nectAvailableID, newCreature):
        self.myID = nectAvailableID
        self.creature = newCreature
    
    ### DON'T TOUCH FROM HERE...

    def Start_Simulation(self, directOrGui):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + directOrGui + " " + str(self.myID) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        fileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fileName):
            time.sleep(0.01)
        f = open(fileName, "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm " + fileName)

    def Create_World(self):
        # Start an sdf file
        pyrosim.Start_SDF("world.sdf")

        length, width, height = 0.5, 0.5, 0.5
        x,y,z = -2, 0, 0.5
        pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height], string1 = "Green", string2 = "0 1.0 0 1.0")
        length, width, height = 0.5, 0.5, 0.5
        x,y,z = -8, 0, 0.5  
        pyrosim.Send_Cube(name="Box1", pos=[x,y,z] , size=[length, width, height], string1 = "Green", string2 = "0 1.0 0 1.0")
        
        # End Pyrosim
        pyrosim.End()

    ### ...TO HERE

    def Create_Body(self):
        # Start an sdf file
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")

        self.creature.generateCreatureBodyFile()

        # End Pyrosim
        pyrosim.End()

    def Create_Brain(self):
        # Start an sdf file
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        self.creature.generateCreatureBrainFile()

        # End Pyrosim
        pyrosim.End()

    def Mutate(self):
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

    def Set_ID(self, id):
        self.myID = id