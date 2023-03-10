from parallelHillClimber import PARALLEL_HILL_CLIMBER
import random
import constants as c
import matplotlib.pyplot as plt
import numpy as np

fitness_curves = {}

# Running
for i in range(c.numOfSeeds):
    random.seed(i)
    np.random.seed(i)
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()
    fitness_curves[i] = phc.fitnessCurve

# Plotting Fitness
for i in range(c.numOfSeeds):
    plt.plot(fitness_curves[i], label='Random Seed ' + str(i))
plt.title('Fitness vs Generations for 10 Random Seeds')
plt.xlabel("Generations")
plt.ylabel("Fitness of the Best Performing Creature in Population")
plt.legend(loc = "upper left")
plt.show()