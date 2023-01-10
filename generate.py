import pyrosim.pyrosim as pyrosim

def Create_World():
    # Start an sdf file
    pyrosim.Start_SDF("world.sdf")

    # Create a cube
    length, width, height = 1, 1, 1
    x,y,z = -3, -3, 0.5
    pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])

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

Create_World()
Create_Robot()