from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            newSolution = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
            self.parents[i] = newSolution
    
    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents:
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in range(len(self.children)):
            self.children[i].Mutate()
            
    def Select(self):
        for i in self.parents:
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Print(self):
        print("\n")
        for i in self.parents:
            print("\nParent fitness: " + str(self.parents[i].fitness) + " Child fitness: " + str(self.parents[i].fitness))
        print("\n")

    def Show_Best(self):
        best_fitness = float('inf')

        for key in self.parents.keys():
            parent = self.parents[key]
            if (parent.fitness < best_fitness):
                best_parent = parent
                best_fitness = parent.fitness

        best_parent.Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for i in solutions:
            solutions[i].Start_Simulation("DIRECT")
        for i in solutions:
            solutions[i].Wait_For_Simulation_To_End()