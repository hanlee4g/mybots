import pyrosim.pyrosim as pyrosim
import random

def Create_World():
    # Start an sdf file
    pyrosim.Start_SDF("world.sdf")

    # Create a cube
    #length, width, height = 1, 1, 1
    #x,y,z = -3, -3, 0.5  
    #pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])

    # End Pyrosim
    pyrosim.End()


def Create_Robot():
    # Start an sdf file
    pyrosim.Start_URDF("body.urdf")

    # Robot
    length, width, height = 1, 1, 1
    pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[length, width, height])
    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[length, width, height])
    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[length, width, height])

    # End Pyrosim
    pyrosim.End()


def Generate_Body():
    # Start an sdf file
    pyrosim.Start_URDF("body.urdf")

    # Robot
    length, width, height = 1, 1, 1
    pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[length, width, height])
    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[length, width, height])
    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[length, width, height])

    # End Pyrosim
    pyrosim.End()

def Generate_Brain():
    # Start an sdf file
    pyrosim.Start_NeuralNetwork("brain.nndf")

    pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

    pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")  
    pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")  

    for sn in range(3):
        for mn in range(3, 5):
            pyrosim.Send_Synapse( sourceNeuronName = sn , targetNeuronName = mn , weight = 2 * random.random() - 1)

    # End Pyrosim
    pyrosim.End()

Create_World()
Generate_Body()
Generate_Brain()