from parallelHillClimber import PARALLEL_HILL_CLIMBER
import random

random.seed(1)
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()
phc.Plot()