import maya.cmds as cmds
import AutoRiggerLocators

############################
#####  Joints  Script  #####
############################

Locators = reload(AutoRiggerLocators)

class createJoints(object):

    def __init__(self, prefix, fingerCount):

        #### sets variables up that user defined from UI ####

        self.prefix = prefix
        self.fingerCount = fingerCount

        rigSize = cmds.xform(prefix + "_" + "Loc_Grp", q = True, s=True, ws=True)

        self.rootRadius = 2 * rigSize[0]

        self.createJoints()
        

    def createJoints(self):
        if cmds.objExists(self.prefix + "_" + "Jnt"):
            print "Rig already exists"
        else:
            jointGrp = cmds.group(em=True, name= self.prefix + "_" + "Jnt_Grp")

        ## Create spine

        Spines = cmds.ls(self.prefix + "_" + "Loc_Spine_*", type='locator')
        Chest = cmds.ls(self.prefix + "_" + "Loc_Ches*", type='locator')

        allSpines = Spines + Chest

        spine=cmds.listRelatives(*allSpines, p=True, f=True)


        self.root = cmds.ls(self.prefix + "_" + "Loc_Root")

        rootPos = cmds.xform(self.root, q = True, t=True, ws=True)
        rootJoint = cmds.joint(radius=self.rootRadius, p = rootPos, name = self.prefix + "_" + "Root_Jnt")

        Centre = cmds.ls(self.prefix + "_" + "Loc_Centre")
        L_CentrePos = cmds.xform(Centre, q=True, t=True, ws=True)
        L_CentreJoint = cmds.joint(radius=self.rootRadius, p=L_CentrePos, name=self.prefix + "_" + "Centre_Jnt")

        
        for i, s in enumerate(spine):
            if i != len(spine)-1:
                pos = cmds.xform(s, q=True, t=True, ws=True)
                j = cmds.joint(radius=self.rootRadius, p= pos, name= self.prefix + "_" + "Spine_" + str(i+1) + "_Jnt")
            else:
                pos = cmds.xform(s, q=True, t=True, ws=True)
                j = cmds.joint(radius=self.rootRadius, p= pos, name= self.prefix + "_" + "Chest_Jnt")

        self.createHead()
        self.createArms()
        self.createFingers()
        self.createLegs()
        
        if cmds.objExists(self.prefix + "_" + "Loc_L_INV_Heel"):
            self.createInverseFootRoll()
        else:
            pass
        self.setJointOrientation()
    
    def createHead(self):
        cmds.select(deselect=True)
        cmds.select(self.prefix + "_" + "Chest_Jnt")

        neckJoint = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + 'Loc_Neck'), q = True, t = True, ws = True), name = self.prefix + "_" + "Neck_Jnt")
        headJoint = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + 'Loc_Head'), q = True, t = True, ws = True), name = self.prefix + "_" + "Head_Jnt")
        jawJoint = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + 'Loc_Jaw'), q = True, t = True, ws = True), name = self.prefix + "_" + "Jaw_Jnt")

    def createArms(self):

        ## Create Left Arm
        cmds.select(deselect=True)
        cmds.select(self.prefix + "_" + "Chest_Jnt")
       
        L_Clavicle = cmds.ls(self.prefix + "_" + "Loc_L_Clavicle")
        L_ClaviclePos = cmds.xform(L_Clavicle, q=True, t=True, ws=True)
        L_ClavicleJoint = cmds.joint(radius=self.rootRadius, p=L_ClaviclePos, name=self.prefix + "_" + "L_Clavicle_Jnt")

        L_Shoulder = cmds.ls(self.prefix + "_" + "Loc_L_Shoulder")
        L_ShoulderPos = cmds.xform(L_Shoulder, q=True, t=True, ws=True)
        L_ShoulderJoint = cmds.joint(radius=self.rootRadius, p=L_ShoulderPos, name=self.prefix + "_" + "L_Shoulder_Jnt")

        L_Elbow = cmds.ls(self.prefix + "_" + "Loc_L_Elbow")
        L_ElbowPos = cmds.xform(L_Elbow, q=True, t=True, ws=True)
        L_ElbowJoint = cmds.joint(radius=self.rootRadius, p=L_ElbowPos, name=self.prefix + "_" + "L_Elbow_Jnt")

        if cmds.objExists(self.prefix + "_" + "Loc_L_ArmTwist"):
            L_ArmTwist = cmds.ls(self.prefix + "_" + "Loc_L_ArmTwist")
            L_ArmTwistPos = cmds.xform(L_ArmTwist, q=True, t=True, ws=True)
            L_ArmTwistJoint = cmds.joint(radius=self.rootRadius, p=L_ArmTwistPos, name=self.prefix + "_" + "L_ArmTwist_Jnt")
        else:
            pass

        L_Wrist = cmds.ls(self.prefix + "_" + "Loc_L_Wrist")
        L_WristPos = cmds.xform(L_Wrist, q=True, t=True, ws=True)
        L_WristJoint = cmds.joint(radius=self.rootRadius, p=L_WristPos, name=self.prefix + "_" + "L_Wrist_Jnt")

        ## Create Right Arm

        cmds.select(deselect=True)
        cmds.select(self.prefix + "_" + "Chest_Jnt")

        R_Clavicle = cmds.ls(self.prefix + "_" + "Loc_R_Clavicle")
        R_ClaviclePos = cmds.xform(R_Clavicle, q=True, t=True, ws=True)
        R_ClavicleJoint = cmds.joint(radius=self.rootRadius, p=R_ClaviclePos, name=self.prefix + "_" + "R_Clavicle_Jnt")

        R_Shoulder = cmds.ls(self.prefix + "_" + "Loc_R_Shoulder")
        R_ShoulderPos = cmds.xform(R_Shoulder, q=True, t=True, ws=True)
        R_ShoulderJoint = cmds.joint(radius=self.rootRadius, p=R_ShoulderPos, name=self.prefix + "_" + "R_Shoulder_Jnt")

        R_Elbow = cmds.ls(self.prefix + "_" + "Loc_R_Elbow")
        R_ElbowPos = cmds.xform(R_Elbow, q=True, t=True, ws=True)
        R_ElbowJoint = cmds.joint(radius=self.rootRadius, p=R_ElbowPos, name=self.prefix + "_" + "R_Elbow_Jnt")

        if cmds.objExists(self.prefix + "_" + "Loc_R_ArmTwist"):
            R_ArmTwist = cmds.ls(self.prefix + "_" + "Loc_R_ArmTwist")
            R_ArmTwistPos = cmds.xform(R_ArmTwist, q=True, t=True, ws=True)
            R_ArmTwistJoint = cmds.joint(radius=self.rootRadius, p=R_ArmTwistPos, name=self.prefix + "_" + "R_ArmTwist_Jnt")
        else:
            pass

        R_Wrist = cmds.ls(self.prefix + "_" + "Loc_R_Wrist")
        R_WristPos = cmds.xform(R_Wrist, q=True, t=True, ws=True)
        R_WristJoint = cmds.joint(radius=self.rootRadius, p=R_WristPos, name=self.prefix + "_" + "R_Wrist_Jnt")

    def createFingers(self):

        # L Thumb

        cmds.select(deselect=True)
        cmds.select(self.prefix + "_" + "L_Wrist_Jnt")

        allThumbs = cmds.ls(self.prefix + "_" + "Loc_L_Thumb*", type='transform')
        #print allThumbs

        for x, f in enumerate(allThumbs):
            pos = cmds.xform(f, q=True, t=True, ws=True)
            j = cmds.joint(radius=self.rootRadius, p = pos, name = self.prefix + "_" + "L_Thumb_" + str(x+1) + "_Jnt")

        # R Thumb

        cmds.select(deselect=True)
        cmds.select(self.prefix + "_" + "R_Wrist_Jnt")

        allThumbs = cmds.ls(self.prefix + "_" + "Loc_R_Thumb*", type='transform')
        #print allThumbs

        for x, f in enumerate(allThumbs):
            pos = cmds.xform(f, q=True, t=True, ws=True)
            j = cmds.joint(radius=self.rootRadius, p = pos, name = self.prefix + "_" + "R_Thumb_" + str(x+1) + "_Jnt")

        # L Fingers

        for i in range(1, self.fingerCount):
            cmds.select(deselect=True)
            cmds.select(self.prefix + "_" + "L_Wrist_Jnt")
            
            allFingers = cmds.ls(self.prefix + "_" + "Loc_L_Finger_" + str(i) + "_*", type='transform')

            for x, f in enumerate(allFingers):
                pos = cmds.xform(f, q=True, t=True, ws=True)
                j = cmds.joint(radius=self.rootRadius, p = pos, name = self.prefix + "_" + "L_Finger_" + str(i) + "_" + str(x+1) + "_Jnt")

        # R Fingers

        for i in range(1, self.fingerCount):
            cmds.select(deselect=True)
            cmds.select(self.prefix + "_" + "R_Wrist_Jnt")
            
            allFingers = cmds.ls(self.prefix + "_" + "Loc_R_Finger_" + str(i) + "_*", type='transform')

            for x, f in enumerate(allFingers):
                pos = cmds.xform(f, q=True, t=True, ws=True)
                j = cmds.joint(radius=self.rootRadius, p = pos, name = self.prefix + "_" + "R_Finger_" + str(i) + "_" + str(x+1) + "_Jnt")

    def createLegs(self):

        cmds.select(deselect=True)
        cmds.select(self.prefix + "_" + "Centre_Jnt")

        # Pelvis
        
        Pelvis = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_Pelvis", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "Pelvis_Jnt")

        # L Leg

        L_Hip = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_Hip", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_Hip_Jnt")
        L_Knee = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_Knee", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_Knee_Jnt")
        L_Ankle = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_Ankle", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_Ankle_Jnt")
        L_Ball = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_Foot_Ball", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_Foot_Ball_Jnt")
        L_Toe = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_Toe", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_Toe_Jnt")

        # R Leg

        cmds.select(deselect=True)
        cmds.select(self.prefix + "_" + "Pelvis_Jnt")

        R_Hip = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_Hip", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_Hip_Jnt")
        R_Knee = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_Knee", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_Knee_Jnt")
        R_Ankle = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_Ankle", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_Ankle_Jnt")
        R_Ball = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_Foot_Ball", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_Foot_Ball_Jnt")
        R_Toe = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_Toe", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_Toe_Jnt")

    def createInverseFootRoll(self):

        cmds.select(deselect=True)

        # L FootRoll

        L_InvHeel = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_INV_Heel", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_INV_Heel_Jnt")
        L_InvToe = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_INV_Toe", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_INV_Toe_Jnt")
        L_InvBall = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_INV_Foot_Ball", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_INV_Foot_Ball_Jnt")
        L_InvAnkle = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_INV_Ankle", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "L_INV_Ankle_Jnt")

        cmds.parent(L_InvHeel, self.prefix + "_" + "Jnt_Grp")

        cmds.select(deselect=True)

        # R FootRoll

        R_InvHeel = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_INV_Heel", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_INV_Heel_Jnt")
        R_InvToe = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_INV_Toe", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_INV_Toe_Jnt")
        R_InvBall = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_INV_Foot_Ball", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_INV_Foot_Ball_Jnt")
        R_InvAnkle = cmds.joint(radius = self.rootRadius, p = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_INV_Ankle", type = 'transform'), q = True, t = True, ws = True), name = self.prefix + "_" + "R_INV_Ankle_Jnt")

        cmds.parent(R_InvHeel, self.prefix + "_" + "Jnt_Grp")

    def setJointOrientation(self):

        cmds.select(self.prefix + "_" + "Root_Jnt")
        cmds.joint(e=True, ch=True, oj='xyz', secondaryAxisOrient = 'xup')

        
def deleteJoints(prefix):
    cmds.select(deselect = True)
    cmds.delete(cmds.ls(prefix + "_" + '*Jnt*'))  