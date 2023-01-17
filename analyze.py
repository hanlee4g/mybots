import numpy as np
import matplotlib.pyplot as mpl

backLegSensorValues = np.load("data/backLegData.npy")
frontLegSensorValues = np.load("data/frontLegData.npy")

mpl.plot(backLegSensorValues, linewidth=3)
mpl.plot(frontLegSensorValues)
mpl.legend(['Back Leg', 'Front Leg'])
mpl.show()