from world import WORLD
from sample_robot import SAMPLEROBOT
import pybullet_data
import pybullet as p
import constants as c
import time

class SAMPLESIMULATION:
    def __init__(self, solutionID):
        self.physicsClient = p.connect(p.GUI)
        p.resetDebugVisualizerCamera(cameraDistance=8, cameraYaw=70, cameraPitch=-30, cameraTargetPosition=[0,0,0])
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.solutionID = solutionID
        self.world = WORLD()
        self.robot = SAMPLEROBOT(self.solutionID, self.world)

    def Run(self):
        sleepTime = c.sleepTime
        for i in range(c.iterations):
            time.sleep(sleepTime)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)

    def __del__(self):        
        p.disconnect()