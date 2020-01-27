import maya.cmds as cmds

############################
##### Locators Script  #####
############################

class createLocators(object):

    def __init__(self, spineCount, fingerCount, prefix):

        #### sets variables up that user defined from UI ####

        self.locatorSize = 0.05

        self.spineCount = spineCount
        self.fingerCount = fingerCount
        self.prefix = prefix

        self.createLocators()

    def createLocators(self, *args):

        loc_size = self.locatorSize

        if cmds.objExists(self.prefix + "_" + "Loc_Grp"):
            print 'Loc_Grp already exists'
        else:
            cmds.group(em = True, name = self.prefix + "_" + "Loc_Grp")

        self.root = cmds.spaceLocator(n = self.prefix + "_" + "Loc_Root")
        cmds.scale(loc_size,loc_size,loc_size, self.root)
        cmds.move(0, 0, 0, self.root)
        cmds.parent(self.root, self.prefix + "_" + "Loc_Grp")

        self.centre = cmds.spaceLocator(n = self.prefix + "_" + "Loc_Centre")
        cmds.scale(loc_size,loc_size,loc_size, self.centre)
        cmds.move(0, 0.92, -0.055, self.centre)
        cmds.parent(self.centre, self.root)

        self.createSpine()

    def createSpine(self, *args):

        loc_size = self.locatorSize

        
        self.spine = cmds.spaceLocator(n = self.prefix + "_" + "Loc_Spine_1")
        cmds.scale(loc_size,loc_size,loc_size, self.spine)
        cmds.move(0, 0.975, -0.038, self.spine)
        
        self.chest = cmds.spaceLocator(n=self.prefix + "_" + "Loc_Chest")
        cmds.scale(loc_size,loc_size,loc_size, self.chest)
        cmds.move(0, 1.457, -0.019, self.chest)

        spineGap = 0.482 / self.spineCount

        #print spineGap

        cmds.parent(self.spine, self.centre)

        for i in range(1, self.spineCount): 
            if i != self.spineCount-1:
                    self.spine = cmds.spaceLocator(n = self.prefix + "_" + "Loc_Spine_" + str(1+i))
                    cmds.scale(loc_size,loc_size,loc_size, self.spine)
                    cmds.move(0, 0.975 + (spineGap * i), -0.01, self.spine)
                    cmds.parent(self.spine, self.prefix + "_" + "Loc_Spine_" + str(i))    
            else:
                cmds.parent(self.chest, self.prefix + "_" + "Loc_Spine_" + str(i), a=True) 

        self.pelvis = cmds.spaceLocator(n= self.prefix + "_" + "Loc_Pelvis")
        cmds.scale(loc_size,loc_size,loc_size, self.pelvis)
        cmds.xform(t = (0, 0.878, 0.002))
        cmds.parent(self.pelvis, self.centre)


        self.createHead()
        self.createArms(1)
        self.createArms(-1)
        self.createLegs(1)
        self.createLegs(-1)

    def createHead(self, *args):

        loc_size = self.locatorSize

        neck = cmds.spaceLocator(n= self.prefix + "_" + 'Loc_Neck')
        cmds.scale(loc_size,loc_size,loc_size, neck)
        cmds.move(0, 1.528, -0.034, neck)
        cmds.parent(neck, self.prefix + "_" + 'Loc_Chest')

        head = cmds.spaceLocator(n= self.prefix + "_" + 'Loc_Head')
        cmds.scale(loc_size,loc_size,loc_size, head)
        cmds.move(0, 1.632, -0.008, head)
        cmds.parent(head, self.prefix + "_" + 'Loc_Neck')

        jaw = cmds.spaceLocator(n= self.prefix + "_" + 'Loc_Jaw')
        cmds.scale(loc_size,loc_size,loc_size, jaw)
        cmds.move(0, 1.606, 0.015, jaw)
        cmds.parent(jaw, self.prefix + "_" + 'Loc_Head')

    def createLegs(self, side):
        
        loc_size = self.locatorSize

        if side == 1:
            if cmds.objExists(self.prefix + "_" + "L_Leg_Grp"):
                pass
            else: 
                upperLegGrp = cmds.group(em = True, name = self.prefix + "_" + "L_Leg_Group")
                cmds.xform(t=(0.089, 0.851, -0.013))
                cmds.parent(upperLegGrp, self.pelvis)

            hip = cmds.spaceLocator(n = self.prefix + "_" + "Loc_L_Hip")
            cmds.scale(loc_size,loc_size,loc_size, hip)
            cmds.parent(hip, self.prefix + "_" + "L_Leg_Group")
            cmds.xform(t=(0, 0, 0))

            # Knee
            knee = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_Knee")
            cmds.scale(loc_size,loc_size,loc_size, knee)
            cmds.move(0.089, 0.54, 0.005, knee)
            cmds.parent(knee, self.prefix + "_" + "Loc_L_Hip")

            # Ankle
            ankle = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_Ankle")
            cmds.scale(loc_size,loc_size,loc_size, ankle)
            cmds.move(0.089, 0.099, -0.036, ankle)
            cmds.parent(ankle, self.prefix + "_" + "Loc_L_Knee")

            # Ball of foot
            ball = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_Foot_Ball")
            cmds.scale(loc_size,loc_size,loc_size, ball)
            cmds.move(0.089, 0, 0.07, ball)
            cmds.parent(ball, self.prefix + "_" + "Loc_L_Ankle")

            # Toe
            toe = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_Toe")
            cmds.scale(loc_size,loc_size,loc_size, toe)
            cmds.move(0.089, 0, 0.138, toe)
            cmds.parent(toe, self.prefix + "_" + "Loc_L_Foot_Ball")

        else:
            if cmds.objExists(self.prefix + "_" + "R_Leg_Grp"):
                pass
            else: 
                upperLegGrp = cmds.group(em = True, name = self.prefix + "_" + "R_Leg_Group")
                cmds.xform(t=(-0.089, 0.851, -0.013))
                cmds.parent(upperLegGrp, self.pelvis)

            hip = cmds.spaceLocator(n = self.prefix + "_" + "Loc_R_Hip")
            cmds.scale(loc_size,loc_size,loc_size, hip)
            cmds.parent(hip, self.prefix + "_" + "R_Leg_Group")
            cmds.xform(t=(0,0,0))

            # Knee
            knee = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_Knee")
            cmds.scale(loc_size,loc_size,loc_size, knee)
            cmds.move(-0.089, 0.54, 0.005, knee)
            cmds.parent(knee, self.prefix + "_" + "Loc_R_Hip")

            # Ankle
            ankle = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_Ankle")
            cmds.scale(loc_size,loc_size,loc_size, ankle)
            cmds.move(-0.089, 0.099, -0.036, ankle)
            cmds.parent(ankle, self.prefix + "_" + "Loc_R_Knee")

            # Ball of foot
            ball = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_Foot_Ball")
            cmds.scale(loc_size,loc_size,loc_size, ball)
            cmds.move(-0.089, 0, 0.07, ball)
            cmds.parent(ball, self.prefix + "_" + "Loc_R_Ankle")

            # Toe
            toe = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_Toe")
            cmds.scale(loc_size,loc_size,loc_size, toe)
            cmds.move(-0.089, 0, 0.138, toe)
            cmds.parent(toe, self.prefix + "_" + "Loc_R_Foot_Ball")

    def createArms(self, side):

        loc_size = self.locatorSize

        if side == 1: # left arm
            if cmds.objExists(self.prefix + "_" + "L_Arm_Grp"):
                pass
            else:
                L_Arm = cmds.group(em=True, n = self.prefix + "_" + "L_Arm_Grp")
                cmds.parent(self.prefix + "_" + "L_Arm_Grp", self.prefix + "_" + "Loc_Chest")
                
                # Clavicle
                Clavicle = cmds.spaceLocator(n=self.prefix + "_" + "Loc_L_Clavicle")
                cmds.scale(loc_size,loc_size,loc_size, Clavicle)
                cmds.move(0.105 * side, 1.48, 0.021, Clavicle)
                cmds.parent(Clavicle, L_Arm)
            
                # Shoulder
                Shoulder = cmds.spaceLocator(n = self.prefix + "_" + "Loc_L_Shoulder")
                cmds.scale(loc_size,loc_size,loc_size, Shoulder)
                cmds.move(0.176 * side, 1.452, -0.043 , Shoulder)
                cmds.parent(Shoulder, Clavicle)

                # Elbow
                Elbow = cmds.spaceLocator(n = self.prefix + "_" + "Loc_L_Elbow")
                cmds.scale(loc_size,loc_size,loc_size, Elbow)
                cmds.move(0.46 * side, 1.453, -0.067, Elbow)
                cmds.parent(Elbow, Shoulder)

                # Wrist
                Wrist = cmds.spaceLocator(n = self.prefix + "_" + "Loc_L_Wrist")
                cmds.scale(loc_size,loc_size,loc_size, Wrist)
                cmds.move(0.754 * side, 1.452, -0.063, Wrist)
                cmds.parent(Wrist, Elbow)
                

                self.createHands(1, Wrist)

        else: # right arm
            if cmds.objExists(self.prefix + "_" + "R_Arm_Grp"):
                pass
            else:
                R_Arm = cmds.group(em=True, n = self.prefix + "_" + "R_Arm_Grp")
                cmds.parent(self.prefix + "_" + "R_Arm_Grp", self.prefix + "_" + "Loc_Chest")

                # Clavicle
                Clavicle = cmds.spaceLocator(n=self.prefix + "_" + "Loc_R_Clavicle")
                cmds.scale(loc_size,loc_size,loc_size, Clavicle)
                cmds.move(0.105 * side, 1.48, 0.021, Clavicle)
                cmds.parent(Clavicle, R_Arm)

                # Shoulder
                Shoulder = cmds.spaceLocator(n = self.prefix + "_" + "Loc_R_Shoulder")
                cmds.scale(loc_size,loc_size,loc_size, Shoulder)
                cmds.move(0.176 * side, 1.452, -0.043 , Shoulder)
                cmds.parent(Shoulder, Clavicle)

                # Elbow
                Elbow = cmds.spaceLocator(n = self.prefix + "_" + "Loc_R_Elbow")
                cmds.scale(loc_size,loc_size,loc_size, Elbow)
                cmds.move(0.46 * side, 1.453, -0.067, Elbow)
                cmds.parent(Elbow, Shoulder)

                # Wrist
                Wrist = cmds.spaceLocator(n = self.prefix + "_" + "Loc_R_Wrist")
                cmds.scale(loc_size,loc_size,loc_size, Wrist)
                cmds.move(0.754 * side, 1.452, -0.063, Wrist)
                cmds.parent(Wrist, Elbow)

                self.createHands(-1, Wrist)

                

    def createHands(self, side, wrist):
        if side == 1:
            if cmds.objExists(self.prefix + "_" + "L_Hand_Grp"):
                pass
            else:
                hand = cmds.group(em = True, name = self.prefix + "_" + "L_Hand_Grp")
                pos = cmds.xform(wrist, q=True, t = True, ws = True)
                cmds.move(pos[0], pos[1], pos[2], hand)
                cmds.parent(hand, self.prefix + "_" + "Loc_L_Wrist")

                for i in range(0, self.fingerCount):
                    self.createFingers(1, pos, i)
        
        else:
            if cmds.objExists(self.prefix + "_" + "R_Hand_Grp"):
                pass
            else:
                hand = cmds.group(em = True, name = self.prefix + "_" + "R_Hand_Grp")
                pos = cmds.xform(wrist, q=True, t = True, ws = True)
                cmds.move(pos[0], pos[1], pos[2], hand)
                cmds.parent(hand, self.prefix + "_" + "Loc_R_Wrist")

                for i in range(0, self.fingerCount):
                    self.createFingers(-1, pos, i)

    def createFingers(self, side, handPos, count):

        loc_size = self.locatorSize

        for x in range (0,3):
            if side == 1:
                if count != 0:
                    finger = cmds.spaceLocator(n = self.prefix + "_" + "Loc_L_Finger_" + str(count) + "_" + str(x+1))
                    cmds.scale(loc_size/2,loc_size/2,loc_size/2, finger)
                    cmds.move(0.864 + (0.03 * x) * side, handPos[1] - (0.01 + (0.01 * x)), -0.007 - (0.025 * count), finger)
                    if x == 0:
                        cmds.parent(finger, self.prefix + "_" + "L_Hand_Grp")
                    else:
                        cmds.parent(finger, self.prefix + "_" + "Loc_L_Finger_" + str(count) + "_" + str(x))
                else:
                    finger = cmds.spaceLocator(n = self.prefix + "_" + "Loc_L_Thumb_" + str(x+1))
                    cmds.scale(loc_size/2,loc_size/2,loc_size/2, finger)
                    cmds.move((0.774 + (0.04*x)) * side, 1.433 - (0.033 * x), -0.024 + (0.024 * x), finger)
                    if x == 0:
                       cmds.parent(finger, self.prefix + "_" + "L_Hand_Grp")
                    else:
                       cmds.parent(finger, self.prefix + "_" + "Loc_L_Thumb_" + str(x))
            else:
                if count != 0:
                    finger = cmds.spaceLocator(n = self.prefix + "_" + "Loc_R_Finger_" + str(count) + "_" + str(x+1))
                    cmds.scale(loc_size/2,loc_size/2,loc_size/2, finger)
                    cmds.move((0.864 + (0.03 * x)) * side, handPos[1] - (0.01 + (0.01 * x)), -0.007 - (0.025 * count), finger)
                    if x == 0:
                        cmds.parent(finger, self.prefix + "_" + "R_Hand_Grp")
                    else:
                        cmds.parent(finger, self.prefix + "_" + "Loc_R_Finger_" + str(count) + "_" + str(x))
                else:
                    finger = cmds.spaceLocator(n = self.prefix + "_" + "Loc_R_Thumb_" + str(x+1))
                    cmds.scale(loc_size/2,loc_size/2,loc_size/2, finger)
                    cmds.move((0.774 + (0.04*x)) * side, 1.433 - (0.033 * x), -0.024 + (0.024 * x), finger)
                    if x == 0:
                       cmds.parent(finger, self.prefix + "_" + "R_Hand_Grp")
                    else:
                       cmds.parent(finger, self.prefix + "_" + "Loc_R_Thumb_" + str(x))

def mirrorLocators(prefix):
    allLeftLocators = cmds.ls(prefix + "_" + "Loc_L_*")
    leftLocators = cmds.listRelatives(*allLeftLocators, p = True, f = True)
    
    allRightLocators = cmds.ls(prefix + "_" + "Loc_R_*")
    rightLocators = cmds.listRelatives(*allRightLocators, p = True, f = True)

    for i,l in enumerate(leftLocators):
        pos = cmds.xform(l, q = True, t=True, ws=True)
        cmds.move(-pos[0], pos[1], pos[2], rightLocators[i])

def deleteLocators(prefix):
    loc_nodes = cmds.ls(prefix + "_" + "Loc_*")
    cmds.delete(loc_nodes)