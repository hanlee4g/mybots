import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

length, width, height = 1, 1, 1
x,y,z = 0, 0, 0.5

for j in range(5):
    for k in range(5):
        for i in range(10):
            pyrosim.Send_Cube(name="Box", pos=[x+j,y+k,z+i] , size=[length*(0.9**i), width*(0.9**i), height*(0.9**i)])

pyrosim.End()