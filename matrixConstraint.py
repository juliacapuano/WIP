import maya.cmds as mc


def matrixCon(driver, driven, drivenOff, offset = False):

    """
    code that uses the matrices to constrain an object instead of default contraints.
    takes in three objects: driver, driven, and driven offset
    """

    #create nodes and connect them
    mult = mc.shadingNode("multMatrix", asUtility = True)
    decomp = mc.shadingNode("decomposeMatrix", asUtility = True)

    mc.connectAttr(mult + ".matrixSum", decomp + ".inputMatrix")

    #matrix math not maintaining offset

    mc.connectAttr(driver + ".worldMatrix[0]", mult + ".matrixIn[1]", force = True) #driver
    mc.connectAttr(drivenOff + ".worldInverseMatrix[0]", mult + ".matrixIn[2]", force = True) #driven offset

    #connecting rotate, translate, and scale to driven
    mc.connectAttr(decomp + ".outputTranslate", driven + ".translate")
    mc.connectAttr(decomp + ".outputRotate", driven + ".rotate")
    mc.connectAttr(decomp + ".outputScale", driven + ".scale")

    if offset:

        mult2 = mc.shadingNode("multMatrix", asUtility = True)

        #adding attribute to driven offset to store matrix offset
        mc.addAttr(drivenOff, ln = "offsetAttr", at = "matrix")

        mc.connectAttr(mult2 + ".matrixSum", drivenOff + ".offsetAttr")

        mc.connectAttr(driven + ".worldMatrix[0]", mult2 + ".matrixIn[0]", force = True)
        mc.connectAttr(driver + ".worldInverseMatrix[0]", mult2 + ".matrixIn[1]", force = True)

        mc.connectAttr(drivenOff + ".offsetAttr", mult + ".matrixIn[0]", force = True) 

        #delete the mult since the  offset is now stored in the offset attribute
        mc.delete(mult2)
    
    

