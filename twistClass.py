import maya.cmds as mc
import maya.OpenMaya as om

class Twist(object):

    """
    Adds in twist joints based on user input, based on a four joint chain. 
    """

    def __init__(self):
        
        self.startPos = []
        self.midPos = []
        self.endPos = []

    def getLocPos(self, jointList, numTwist, pos, prefix):

        startVec = om.MVector(self.startPos[0], self.startPos[1], self.startPos[2])
        midVec = om.MVector(self.midPos[0], self.midPos[1], self.midPos[2])
        endVec = om.MVector(self.endPos[0], self.endPos[1], self.endPos[2])

        startMid = midVec - startVec
        midEnd = endVec - midVec
        
        div = float(1.0/float(numTwist))  #fraction of twist joints to get even placement of joints
        
        upperList = []
        lowerList = []
        
        if pos == "upper":
            for i in range(numTwist+1):
                upperLoc = mc.spaceLocator(name = prefix + "upperTwist_LOC_0" + str(i+1))
                
                mc.move(startVec.x + ((i*div)*startMid.x), startVec.y + ((i*div)*startMid.y), 
                startVec.z + ((i*div)*startMid.z), upperLoc, ws = True)
                
                mc.setAttr(prefix + "upperTwist_LOC_0" + str(i+1) + "Shape.localScaleZ", 3)
                mc.setAttr(prefix + "upperTwist_LOC_0" + str(i+1) + "Shape.localScaleY", 3)
                mc.setAttr(prefix + "upperTwist_LOC_0" + str(i+1) + "Shape.localScaleX", 3)
                
                upperList.append(upperLoc)
                
            return upperList

        elif pos == "lower":
            for i in range(numTwist+1):
                lowerLoc = mc.spaceLocator(name = prefix + "lowerTwist_LOC_0" + str(i+1))
                
                mc.move(midVec.x + ((i*div)*midEnd.x), midVec.y + ((i*div)*midEnd.y), 
                midVec.z + ((i*div)*midEnd.z), lowerLoc, ws = True)
                
                mc.setAttr(prefix + "lowerTwist_LOC_0" + str(i+1) + "Shape.localScaleZ", 3)
                mc.setAttr(prefix + "lowerTwist_LOC_0" + str(i+1) + "Shape.localScaleY", 3)
                mc.setAttr(prefix + "lowerTwist_LOC_0" + str(i+1) + "Shape.localScaleX", 3)
                
                lowerList.append(lowerLoc)
                
            return lowerList
        
        
    #place joints
    def placeJoints(self, jointList, numTwist, pos, prefix):

        upperJointLst = []
        lowerJointLst = []

        if pos == "upper":
            
            upper = self.getLocPos(jointList, numTwist, "upper", prefix = prefix)
            
            for i in range(numTwist+1):
                
                jnts = mc.joint(radius = .1, p = mc.xform(upper[i], q = True, os = True, t = True), 
                                name = prefix + "upperTwist_JNT_0" + str(i+1))
                
                upperJointLst.append(jnts)
                
            for i in range(numTwist):
                mc.parent(upper[i], upperJointLst[i])
                
            mc.joint(upperJointLst[0], e = True, zso = True, ch = True, oj = "xyz")
            
            mc.select(upperJointLst[-1])
            mc.delete()
            
            return upperJointLst
        
        elif pos == "lower": 
        
            lower = self.getLocPos(jointList, numTwist, "lower", prefix = prefix)
            
            for i in range(numTwist+1):
                
                jnts = mc.joint(radius = .1, p = mc.xform(lower[i], q = True, os = True, t = True), 
                name = prefix + "lowerTwist_JNT_0" + str(i+1))
                
                lowerJointLst.append(jnts)
                
            for i in range(numTwist):
                mc.parent(lower[i], lowerJointLst[i])
                
            mc.joint(lowerJointLst[0], e = True, zso = True, ch = True, oj = "xyz")
            
            mc.select(lowerJointLst[-1])
            mc.delete()

            return lowerJointLst
            
    #create upper twist between joints b and c               
    def upperTwist(self, jointList, prefix, numTwist):
        
        self.startPos = mc.xform(jointList[1], q = True, ws = True, t = True)
        self.midPos = mc.xform(jointList[2], q = True, ws = True, t = True)
        self.endPos = mc.xform(jointList[3], q = True, ws = True, t = True)
        
        if mc.objExists(prefix + "upperTwist"):
            print ("object already exists")
            
        else:
        
            mc.group(em = True, name = prefix + "upperTwist")
            main_GRP = mc.parent(prefix + "upperTwist", jointList[0])  
            mc.move(0,0,0, prefix + "upperTwist", objectSpace = True)
            
            mc.group(em = True, name = prefix + "upperTwist_transform")                                       
            transform_GRP = mc.parent(prefix + "upperTwist_transform", main_GRP)
            mc.move(0,0,0, prefix + "upperTwist_transform", objectSpace = True)

            upperJointLst = self.placeJoints(jointList, numTwist, "upper", prefix)
            mc.parent(upperJointLst[0], transform_GRP)
                
            mc.parentConstraint(jointList[1], transform_GRP, mo = 1)
            mc.select(jointList[0])
            
            twistStart = mc.joint(radius = .2, p = (self.startPos[0], self.startPos[1], 
                                self.startPos[2]), name = prefix + "upper_twistStart_JNT")
            twistEnd = mc.joint(radius = .2, p = (self.midPos[0], self.midPos[1], 
                                self.midPos[2]), name = prefix + "upper_twistEnd_JNT")
            
            mc.ikHandle(n = prefix + "ikH_upperTwist_target", sol = "ikSCsolver", sj = twistStart, ee = twistEnd)[0]
            ikHdl = mc.parent(prefix + "ikH_upperTwist_target", main_GRP)
            
            mc.orientConstraint(jointList[2], twistEnd, mo = 0)
            mc.pointConstraint(jointList[2], ikHdl, mo = 0)
            
            mc.parent(twistStart, main_GRP)
            
            self.createDivNode(name = "upperTwist_MD_01")
            
            mc.connectAttr(jointList[2] + ".rotateX", "upperTwist_MD_01.i1x")
            
            for i in range(numTwist):
                if i == 0:
                    pass 
                else:
                    mc.connectAttr("upperTwist_MD_01.ox", upperJointLst[i]+".rotateX")

    #lower twist: between joints c and d
    def lowerTwist(self, jointList, prefix, numTwist):

        self.startPos = mc.xform(jointList[1], q = True, ws = True, t = True)
        self.midPos = mc.xform(jointList[2], q = True, ws = True, t = True)
        self.endPos = mc.xform(jointList[3], q = True, ws = True, t = True)
        
        if mc.objExists(prefix + "lowerTwist"):
            print ("object already exists")
            
        else:
        
            mc.group(em = True, name = prefix + "lowerTwist")
            main_GRP = mc.parent(prefix + "lowerTwist", jointList[2])  
            mc.move(0,0,0, prefix + "lowerTwist", objectSpace = True)
            
            mc.group(em = True, name = prefix + "lowerTwist_transform")                                       
            transform_GRP = mc.parent(prefix + "lowerTwist_transform", main_GRP)
            mc.move(0,0,0, prefix + "lowerTwist_transform", objectSpace = True)

            lowerJointLst = self.placeJoints(jointList, numTwist, "lower", prefix)
            mc.parent(lowerJointLst[0], transform_GRP)
                
            mc.parentConstraint(jointList[2], transform_GRP, mo = 1)
            mc.select(jointList[2])
            
            twistStart = mc.joint(radius = .2, p = (self.midPos[0], self.midPos[1], 
                                self.midPos[2]), name = prefix +  "lower_twistStart_JNT")
            twistEnd = mc.joint(radius = .2, p = (self.endPos[0], self.endPos[1], 
                                self.endPos[2]), name = prefix + "lower_twistEnd_JNT")
            
            mc.ikHandle(n = prefix + "ikH_lowerTwist_target", sol = "ikSCsolver", sj = twistStart, ee = twistEnd)[0]
            mc.parent(prefix + "ikH_lowerTwist_target", main_GRP)
            
            mc.parent(twistStart, main_GRP)
            
            self.createDivNode(name = "lowerTwist_MD_01")
            
            mc.connectAttr(jointList[3] + ".rotateX", "lowerTwist_MD_01.i1x")
            
            for i in range(numTwist):
                if i == 0:
                    pass 
                else:
                    mc.connectAttr("lowerTwist_MD_01.ox", lowerJointLst[i]+".rotateX")
                    
                    
    def createDivNode(self, name):
        divide = mc.shadingNode("multiplyDivide", asUtility = True, name = name)

        mc.setAttr(divide + ".operation", 2)
        mc.setAttr(divide + ".i2x", 4)
        
