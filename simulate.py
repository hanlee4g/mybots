from cmath import phase
import pybullet_data
import pybullet as p
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

backLegAmplitude = numpy.pi / 4.0
backLegFrequency = 10.0
backLegPhaseOffset = 0.0
frontLegAmplitude = numpy.pi / 4.0
frontLegFrequency = 10.0
frontLegPhaseOffset = numpy.pi / 4.0

iterations = 1000
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(iterations)
frontLegSensorValues = numpy.zeros(iterations)
maxForce = 20
backLegTargetAngles = backLegAmplitude * numpy.sin(backLegFrequency * numpy.linspace(0, 2*numpy.pi, iterations) + backLegPhaseOffset)
frontLegTargetAngles = frontLegAmplitude * numpy.sin(frontLegFrequency * numpy.linspace(0, 2*numpy.pi, iterations) + frontLegPhaseOffset)

numpy.save("data/backLegMotorData.npy",backLegTargetAngles)
numpy.save("data/frontLegMotorData.npy",frontLegTargetAngles)

for i in range(iterations):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = backLegTargetAngles[i],
        maxForce = maxForce)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = frontLegTargetAngles[i],
        maxForce = maxForce)
    time.sleep(1/240)

p.disconnect()
numpy.save("data/backLegData.npy",backLegSensorValues)
numpy.save("data/frontLegData.npy",frontLegSensorValues)