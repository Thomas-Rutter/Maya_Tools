import maya.cmds as cmds

############################
#### Constraints Script ####
############################

class createContraints(object):

    def __init__(self, spineCount, fingerCount, prefix):

        #### sets variables up that user defined from UI ####

        self.spineCount = spineCount
        self.fingerCount = fingerCount
        self.prefix = prefix

        self.createContraints()
    
    def createContraints(self, *args):
        #cmds.makeIdentity(cmds.ls(self.prefix + "*Jnt"), apply = True, t = 1, r = 1, s = 1)

        #### Orient Constraints ####

        orients = ["_Centre", "_Pelvis", "_Chest", "_Head", "_Neck", "_Jaw", "_L_Clavicle", "_R_Clavicle"]

        for i in range(0, self.spineCount-1):
            spine = "_Spine_" + str(i+1)
            orients.append(spine)

        sides = ["L", "R"]

        for s in sides:

            allThumbs = cmds.ls(self.prefix + "_" + s + "_Thumb_*"  + "_Jnt", type='transform')

            for x, f in enumerate(allThumbs):
                thumb = "_" + s + "_Thumb_" + str(x+1)
                orients.append(thumb)

            for i in range(1, self.fingerCount):
                allFingers = cmds.ls(self.prefix + "_" + s + "_Finger_" + str(i) + "*_Jnt", type='transform')

                for x, f in enumerate(allFingers):
                    finger = "_" + s + "_Finger_" + str(i) + "_" + str(x+1)
                    orients.append(finger)


        print orients

        for i in orients:

            cmds.orientConstraint(self.prefix + i + "_Con", self.prefix + i + "_Jnt", mo=True)

        #### Set constaints for IK's, Centre and Global controls ####

        cmds.orientConstraint(self.prefix + "_L_Wrist_Con", self.prefix + "_L_Wrist_Jnt", mo=True)
        cmds.poleVectorConstraint( self.prefix + "_L_Elbow_Con", self.prefix + "_L_Arm_IK")
        cmds.parent(self.prefix + "_L_Arm_IK", self.prefix + "_L_Wrist_Con")

        cmds.orientConstraint(self.prefix + "_R_Wrist_Con", self.prefix + "_R_Wrist_Jnt", mo=True)
        cmds.poleVectorConstraint( self.prefix + "_R_Elbow_Con", self.prefix + "_R_Arm_IK")
        cmds.parent(self.prefix + "_R_Arm_IK", self.prefix + "_R_Wrist_Con")

        cmds.pointConstraint(self.prefix + "_Centre_Con", self.prefix + "_Centre_Jnt", mo=True)
        
        cmds.pointConstraint(self.prefix + "_Global_Con", self.prefix + "_Root_Jnt", mo=True)
        cmds.orientConstraint(self.prefix + "_Global_Con", self.prefix + "_Root_Jnt", mo=True)


        cmds.parent(self.prefix + "_L_Leg_IK", self.prefix + "_L_INV_Ball_IK", self.prefix + "_L_INV_Toe_IK", self.prefix + "_L_Foot_Con")
        cmds.parent(self.prefix + "_R_Leg_IK", self.prefix + "_R_INV_Ball_IK", self.prefix + "_R_INV_Toe_IK", self.prefix + "_R_Foot_Con")
    
def inverseFoot(prefix):

    #### Sets up inverse foot roll hierarchy ####

    prefix = prefix

    side = ["_L_", "_R_"]

    for s in side:        
        cmds.parent(prefix + s + "Leg_IK", prefix + s +"INV_Ankle_Jnt")
        cmds.parent(prefix + s + "INV_Ankle_Jnt", prefix + s + "INV_Ball_IK", prefix + s + "INV_Foot_Ball_Jnt")
        cmds.parent(prefix + s + "INV_Foot_Ball_Jnt", prefix + s + "INV_Toe_IK", prefix + s + "INV_Toe_Jnt")
        cmds.parent(prefix + s + "INV_Heel_Jnt", prefix + s + "Foot_Con")

def bindSkin(prefix):

    #### Binds skin to mesh, if mesh not selected than message appears ####

    sel = cmds.ls(sl = True)
    if (len(sel) == 0):
        cmds.confirmDialog(title = "Empty Selection", message = "You have to select a mesh, cause I can't do everything for you.", button = ['Ok'])
    else:
        for i in range(0, len(sel)):
            cmds.skinCluster(sel[i], prefix + "_Root_Jnt", bm = 3, sm = 0, name = "Mesh"+str(i))
            cmds.geomBind('Mesh'+str(i), bm = 3, mi=4, gvp = [1024, 1])   

def orangizeRig(prefix):

    #### Orangise hierarchy and set global constraints ####

    if cmds.objExists(prefix + "_Rig_Grp"):
        print "Rig group already exists"
    else:
        jointGrp = cmds.group(em=True, name= prefix + "_Rig_Grp")

    controls = ["_Centre", "_L_Foot", "_R_Foot", "_L_Elbow", "_R_Elbow", "_L_Knee", "_R_Knee"]

    for i in controls:
        cmds.parent(prefix + i + "_Con", prefix + "_Rig_Grp")

    cmds.parent(prefix + "_Root_Jnt", prefix + "_Rig_Grp")
    cmds.delete(prefix + "_Jnt_Grp")

    cmds.parent(prefix + "_Loc_Grp", prefix + "_Secondary_Loc_Grp", prefix + "_Rig_Grp")
    cmds.hide(prefix + "_Loc_Grp", prefix + "_Secondary_Loc_Grp")

    cmds.parentConstraint(prefix + "_Global_Con", prefix + "_Rig_Grp", mo=True)
    cmds.scaleConstraint(prefix + "_Global_Con", prefix + "_Rig_Grp", mo=True)

    #### Display Layers ####

    if (cmds.objExists(prefix + "_Controllers_Layer")):
        cmds.editDisplayLayerMembers(prefix + "_Controllers_Layer", prefix + "_Global_Con")
    else:
        _ctrl = cmds.select(prefix + "_Global_Con")    
        cmds.createDisplayLayer(name = prefix + "_Controllers_Layer")

    for i in controls:
        cmds.editDisplayLayerMembers(prefix + "_Controllers_Layer", prefix + i + "_Con")

    if (cmds.objExists(prefix + "_Skeleton_Layer")):
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_Root_Jnt")
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_L_INV_Heel_Jnt")
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_R_INV_Heel_Jnt")
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_L_Arm_IK")
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_R_Arm_IK")

    else:
        _ctrl = cmds.select(prefix + "_Root_Jnt")    
        cmds.createDisplayLayer(name = prefix + "_Skeleton_Layer")
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_L_INV_Heel_Jnt")
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_R_INV_Heel_Jnt")
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_L_Arm_IK")
        cmds.editDisplayLayerMembers(prefix + "_Skeleton_Layer", prefix + "_R_Arm_IK")


    cmds.setAttr("%s.displayType" % (prefix + "_Skeleton_Layer"), 2)
    cmds.setAttr("%s.visibility" % (prefix + "_Skeleton_Layer"), 0)

def disLayer(prefix):

    # Enable the layer's color.
    cmds.setAttr("%s.color" % (prefix + "_Skeleton_Layer"), True)
    cmds.setAttr("%s.color" % (prefix + "_Controllers_Layer"), True)

    # Enable the layer's color to use rgb.
    cmds.setAttr("%s.overrideRGBColors" % (prefix + "_Skeleton_Layer"), True)
    cmds.setAttr("%s.overrideRGBColors" % (prefix + "_Controllers_Layer"), True)

    # Set the layer's color with values between 0-1.
    cmds.setAttr("%s.overrideColorRGB" % (prefix + "_Skeleton_Layer"), 1, 1, 1)
    cmds.setAttr("%s.overrideColorRGB" % (prefix + "_Controllers_Layer"), 1, 0.392, 0)