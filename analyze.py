import numpy as np
import matplotlib.pyplot as mpl


backLegSensorValues = np.load("data/backLegData.npy")
frontLegSensorValues = np.load("data/frontLegData.npy")
backTargetAngles = np.load("data/backLegMotorData.npy")
frontTargetAngles = np.load("data/frontLegMotorData.npy")

# mpl.plot(backLegSensorValues, linewidth=3)
# mpl.plot(frontLegSensorValues)
# mpl.legend(['Back Leg', 'Front Leg'])
mpl.plot(backTargetAngles, linewidth = 4)
mpl.plot(frontTargetAngles)
mpl.legend(['Back Target Angles', 'Front Target Angles'])
mpl.show()