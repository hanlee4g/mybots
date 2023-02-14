from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, newstring1, newstring2):

        self.depth  = 3

        self.string1 = '<material name="' + newstring1 + '">'

        # HERE
        self.string2 = '    <color rgba="' + newstring2 + '"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
