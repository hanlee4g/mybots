import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim

class WORLD:
    def __init__(self):
        self.planeId = p.loadURDF("plane.urdf")
        self.objects = p.loadSDF("world.sdf")