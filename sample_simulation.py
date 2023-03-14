from world import WORLD
from sample_robot import SAMPLEROBOT
import pybullet_data
import pybullet as p
import constants as c
import time

class SAMPLESIMULATION:
    def __init__(self, solutionID, test_folder):
        self.physicsClient = p.connect(p.GUI)
        p.resetDebugVisualizerCamera(cameraDistance=9, cameraYaw=-40, cameraPitch=-30, cameraTargetPosition=[-3,0,0])
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.solutionID = solutionID
        self.world = WORLD()
        self.test_folder = test_folder
        self.robot = SAMPLEROBOT(self.solutionID, self.world, self.test_folder)

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