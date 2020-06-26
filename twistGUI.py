import maya.cmds as mc

import twistJoints_03 as twist
reload(twist)

twistID = "TwistWIndow"

global jointList
global prefix
global numTwist

if mc.window(twistID, exists = True):
    mc.deleteUI(twistID)
    
mc.window(twistID, t ="Add Twists")

mc.rowColumnLayout(nc = 3)

#create joint list input
mc.text(l = "Joint List")
jointListTxt = mc.textField(w = 200, ed = False)
mc.button(l = "<<<", c = "putInTxtField()")

#create num twist input
mc.text(l = "Number of Twists")
numTwistInput = mc.intField(minValue = 2, maxValue = 10, value = 4, s = 1, cc = "getNumTwist()")    #user input for number of twist wanted
mc.button(l = "<<<", c = "getNumTwist()")

#create prefix input
mc.text(l = "Prefix")
prefixInput = mc.textField(w = 200, tx = "L_arm_", cc = "getPrefix()")
mc.button(l = "<<<", c = "getPrefix()")

#execute twist code
mc.button(l = "Create Upper Twist", w = 200, c = "twist.upperTwist(jointList, prefix, numTwist)", bgc = (0.5,0.0,1.0))
mc.button(l = "Create Lower Twist", w = 200, c = "twist.lowerTwist(jointList, prefix, numTwist)", bgc = (1.0,0.0,0.5))
mc.button(l = "Delete Twist", w = 100, c = "deleteTwist()", bgc = (1.0, 0.0, 0.0))

mc.showWindow()

#get and set functions
def putInTxtField():
    sel = mc.ls(sl = True)
    mc.textField(jointListTxt, e = True, tx = ",".join(sel))
    global jointList
    jointListTemp = str(mc.textField(jointListTxt, q = True, tx = True))
    jointList = jointListTemp.split(',')
    
def getNumTwist():
    global numTwist 
    numTwist = mc.intField(numTwistInput, q = True, value = True)
    
def getPrefix():
    global prefix
    prefix = mc.textField(prefixInput, q = True, tx = True)
    
def deleteTwist():
    twists = mc.ls("*twist*", "*Twist*")
    mc.delete(twists)
    