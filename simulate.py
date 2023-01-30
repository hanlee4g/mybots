from simulation import SIMULATION
import sys

directOrGui = sys.argv[1]

simulation = SIMULATION(directOrGui)
simulation.Run()
simulation.Get_Fitness()