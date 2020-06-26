import maya.cmds as mc

from twistClass import Twist

class TwistWindow(object):

    twistID = "TwistWindow"

    def __init__(self):

        self.jointList = []
        self.prefix = None 
        self.numTwist = None 

    def show(self):
        if mc.window(self.twistID, exists = True):
            mc.deleteUI(self.twistID)
        
        mc.window(self.twistID, t ="Add Twists")
        self.buildUI()
        mc.showWindow()

    def buildUI(self):

        mc.rowColumnLayout(nc = 3)

        #create joint list input
        mc.text(l = "Joint List")
        self.jointListTxt = mc.textField(w = 200, ed = False)
        mc.button(l = "<<<", c = "self.putInTxtField()")

        #create num twist input
        mc.text(l = "Number of Twists")
        self.numTwistInput = mc.intField(minValue = 2, maxValue = 10, value = 4, s = 1, cc = "self.getNumTwist()")    #user input for number of twist wanted
        mc.button(l = "<<<", c = "self.getNumTwist()")

        #create prefix input
        mc.text(l = "Prefix")
        self.prefixInput = mc.textField(w = 200, tx = "L_arm_", cc = "getPrefix()")
        mc.button(l = "<<<", c = "self.getPrefix()")

        #execute twist code
        mc.button(l = "Create Upper Twist", w = 200, c = "Twist().upperTwist(jointList, prefix, numTwist)", bgc = (0.5,0.0,1.0))
        mc.button(l = "Create Lower Twist", w = 200, c = "Twist().lowerTwist(jointList, prefix, numTwist)", bgc = (1.0,0.0,0.5))
        mc.button(l = "Delete Twist", w = 100, c = "self.deleteTwist()", bgc = (1.0, 0.0, 0.0))

    #get and set functions
    def putInTxtField(self):
        sel = mc.ls(sl = True)
        mc.textField(self.jointListTxt, e = True, tx = ",".join(sel))
        jointListTemp = str(mc.textField(self.jointListTxt, q = True, tx = True))
        self.jointList = jointListTemp.split(',')
        
    def getNumTwist(self):
        self.numTwist = mc.intField(self.numTwistInput, q = True, value = True)
        
    def getPrefix(self):
        self.prefix = mc.textField(self.prefixInput, q = True, tx = True)
        
    def deleteTwist(self):
        twists = mc.ls("*twist*", "*Twist*")
        mc.delete(twists)
    