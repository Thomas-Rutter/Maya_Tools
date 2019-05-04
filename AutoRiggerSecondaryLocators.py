import maya.cmds as cmds

############################
### 2nd Locators Script  ###
############################

class createSecondaryLocators(object):

    def __init__(self, prefix):

        #### sets variables up that user defined from UI ####

        self.locatorSize = 0.05
        self.prefix = prefix

        if cmds.objExists(self.prefix + "_" + "Secondary_Loc_Grp"):
            print 'Secondary_Loc_Grp already exists'
        else:
            cmds.group(em = True, name = self.prefix + "_" + "Secondary_Loc_Grp")
        
        self.createForearmTwist()
        self.createReverseFootRoll()

    def createForearmTwist(self, *args):

        loc_size = self.locatorSize

        cmds.select(deselect = True)

        # L Arm Twist

        L_elbow = cmds.ls(self.prefix + "_" + "Loc_L_Elbow")
        L_wrist = cmds.ls(self.prefix + "_" + "Loc_L_Wrist")

        L_elbowPos = cmds.xform(L_elbow, q=True, t=True, ws=True)
        L_wristPos = cmds.xform(L_wrist, q=True, t=True, ws=True)

        L_vectorX =  L_wristPos[0] - L_elbowPos[0]
        L_vectorY = L_wristPos[1] - L_elbowPos[1]
        L_vectorZ = L_wristPos[2] - L_elbowPos[2]

        L_twistLoc = cmds.spaceLocator(n = self.prefix + "_" + "Loc_L_ArmTwist")
        cmds.move(L_elbowPos[0] + (L_vectorX/2), L_elbowPos[1] + (L_vectorY/2), L_elbowPos[2] + (L_vectorZ/2), L_twistLoc)
        cmds.scale(loc_size,loc_size,loc_size, L_twistLoc)
        cmds.parent(L_twistLoc, self.prefix + "_" + "Secondary_Loc_Grp")

        # R Arm Twist

        R_elbow = cmds.ls(self.prefix + "_" + "Loc_R_Elbow")
        R_wrist = cmds.ls(self.prefix + "_" + "Loc_R_Wrist")

        R_elbowPos = cmds.xform(R_elbow, q=True, t=True, ws=True)
        R_wristPos = cmds.xform(R_wrist, q=True, t=True, ws=True)

        R_vectorX =  R_wristPos[0] - R_elbowPos[0]
        R_vectorY = R_wristPos[1] - R_elbowPos[1]
        R_vectorZ = R_wristPos[2] - R_elbowPos[2]

        R_twistLoc = cmds.spaceLocator(n = self.prefix + "_" + "Loc_R_ArmTwist")
        cmds.move(R_elbowPos[0] + (R_vectorX/2), R_elbowPos[1] + (R_vectorY/2), R_elbowPos[2] + (R_vectorZ/2), R_twistLoc)
        cmds.scale(loc_size,loc_size,loc_size, R_twistLoc)
        cmds.parent(R_twistLoc, self.prefix + "_" + "Secondary_Loc_Grp")

    def createReverseFootRoll(self, *args):

        loc_size = self.locatorSize

        # Heels

        cmds.select(deselect=True)

        L_ankle = cmds.ls(self.prefix + "_" + "Loc_L_Ankle")
        L_ball = cmds.ls(self.prefix + "_" + "Loc_L_Foot_Ball")
        L_anklePos = cmds.xform(L_ankle, q=True, t=True, ws=True)
        L_ballPos = cmds.xform(L_ball, q=True, t=True, ws=True)


        L_Rev_Heel = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_INV_Heel")
        cmds.scale(loc_size, loc_size, loc_size, L_Rev_Heel)
        cmds.move(L_anklePos[0], L_ballPos[1], L_anklePos[2], L_Rev_Heel)
        cmds.parent(L_Rev_Heel, self.prefix + "_" + "Secondary_Loc_Grp")

        R_ankle = cmds.ls(self.prefix + "_" + "Loc_R_Ankle")
        R_ball = cmds.ls(self.prefix + "_" + "Loc_R_Foot_Ball")
        R_anklePos = cmds.xform(R_ankle, q=True, t=True, ws=True)
        R_ballPos = cmds.xform(R_ball, q=True, t=True, ws=True)


        R_Rev_Heel = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_INV_Heel")
        cmds.scale(loc_size, loc_size, loc_size, R_Rev_Heel)
        cmds.move(R_anklePos[0], R_ballPos[1], R_anklePos[2], R_Rev_Heel)
        cmds.parent(R_Rev_Heel, self.prefix + "_" + "Secondary_Loc_Grp")

        # Toes 

        L_toeLoc = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_Toe"), q=True, t=True, ws=True)
        L_Rev_Toe = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_INV_Toe")
        cmds.scale(loc_size,loc_size,loc_size,L_Rev_Toe)
        cmds.move(L_toeLoc[0],L_toeLoc[1],L_toeLoc[2], L_Rev_Toe)
        cmds.parent(L_Rev_Toe, L_Rev_Heel)

        R_toeLoc = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_Toe"), q=True, t=True, ws=True)
        R_Rev_Toe = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_INV_Toe")
        cmds.scale(loc_size,loc_size,loc_size,R_Rev_Toe)
        cmds.move(R_toeLoc[0],R_toeLoc[1],R_toeLoc[2], R_Rev_Toe)
        cmds.parent(R_Rev_Toe, R_Rev_Heel)

        # Ball of Foot

        L_ballLoc = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_Foot_Ball"), q=True, t=True, ws=True)
        L_Rev_ball = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_INV_Foot_Ball")
        cmds.scale(loc_size,loc_size,loc_size,L_Rev_ball)
        cmds.move(L_ballLoc[0],L_ballLoc[1],L_ballLoc[2], L_Rev_ball)
        cmds.parent(L_Rev_ball, L_Rev_Toe)

        R_ballLoc = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_Foot_Ball"), q=True, t=True, ws=True)
        R_Rev_ball = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_INV_Foot_Ball")
        cmds.scale(loc_size,loc_size,loc_size,R_Rev_ball)
        cmds.move(R_ballLoc[0],R_ballLoc[1],R_ballLoc[2], R_Rev_ball)
        cmds.parent(R_Rev_ball, R_Rev_Toe)

        # Ankle

        L_ankleLoc = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_L_Ankle"), q=True, t=True, ws=True)
        L_Rev_ankle = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_INV_Ankle")
        cmds.scale(loc_size,loc_size,loc_size,L_Rev_ankle)
        cmds.move(L_ankleLoc[0],L_ankleLoc[1],L_ankleLoc[2], L_Rev_ankle)
        cmds.parent(L_Rev_ankle, L_Rev_ball)

        R_ankleLoc = cmds.xform(cmds.ls(self.prefix + "_" + "Loc_R_Ankle"), q=True, t=True, ws=True)
        R_Rev_ankle = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_INV_Ankle")
        cmds.scale(loc_size,loc_size,loc_size,R_Rev_ankle)
        cmds.move(R_ankleLoc[0],R_ankleLoc[1],R_ankleLoc[2], R_Rev_ankle)
        cmds.parent(R_Rev_ankle, R_Rev_ball)


def deleteSecondaryLocators(prefix):
    loc_nodes = cmds.ls(prefix + "_" + "Secondary_Loc_*")
    cmds.delete(loc_nodes)

