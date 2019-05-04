import maya.cmds as cmds

############################
#### Controllers Script ####
############################

class createControllers(object):

    def __init__(self, spineCount, fingerCount, prefix):

        #### sets variables up that user defined from UI ####

        self.spineCount = spineCount
        self.fingerCount = fingerCount
        self.prefix = prefix

        rigSize = cmds.xform(prefix + "_" + "Loc_Grp", q = True, s=True, ws=True)

        self.conRadius = 1 * rigSize[0]

        #### Calls all create functions in the class in correct order ####

        self.createGlobal()
        self.createCentre()
        self.createPelvis()
        self.createSpines(spineCount)
        self.createNeck()
        self.createHead()
        self.createClavicles()
        self.createWrists()
        self.createFingers()
        self.createFeet()
        self.createPolVectors()
        self.alignKneeVectors()
        
    def createGlobal(self):

        #### Creates Global control based off root joint ####
        
        rootPos = cmds.xform(cmds.ls(self.prefix + "_Root_Jnt", type='joint'), q=True, t=True, ws=True)
        global_ctrl = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, s = 8, name = self.prefix + "_Global_Con")
        selection = cmds.select(self.prefix + "_Global_Con.cv[1]", self.prefix + "_Global_Con.cv[3]", self.prefix + "_Global_Con.cv[5]", self.prefix + "_Global_Con.cv[7]")
        cmds.scale(0.7, 0.7, 0.7, selection)
        cmds.scale(0.5,0.5,0.5, global_ctrl)

        cmds.move(rootPos[0],rootPos[1],rootPos[2], global_ctrl)

        cmds.makeIdentity(global_ctrl, apply = True, t = 1, r = 1, s = 1)

    def createCentre(self):

        #### Creates Centre control shape to be square ####

        centre_ctrl = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, s = 8, name = self.prefix + "_Centre_Con")
        selection = cmds.select(self.prefix + "_Centre_Con.cv[1]", self.prefix + "_Centre_Con.cv[3]", self.prefix + "_Centre_Con.cv[5]", self.prefix + "_Centre_Con.cv[7]")
        cmds.scale(0.7, 0.7, 0.7, selection)
        cmds.scale(0.3,0.3,0.3, centre_ctrl)

        #### Moves Centre control to be around Centre joint ####

        centrePos = cmds.xform(cmds.ls(self.prefix + "_Centre_Jnt", type='joint'), q=True, t=True, ws=True)
        cmds.move(centrePos[0], centrePos[1], centrePos[2]+0.05, centre_ctrl)

        #### Sets pivot of control to be on joint, freezes transforms and parents control to global control ####

        cmds.move(centrePos[0], centrePos[1], centrePos[2], self.prefix + "_Centre_Con"+ '.scalePivot', self.prefix + "_Centre_Con" + '.rotatePivot', absolute=True)
        cmds.makeIdentity(centre_ctrl, apply = True, t = 1, r = 1, s = 1)
        cmds.parent(centre_ctrl, self.prefix + "_Global_Con")

    def createPelvis(self):

        #### Creates Pelvis control and edits shape of control ####

        pelvis_ctrl = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, s = 8, name = self.prefix + "_Pelvis_Con")
        selection = cmds.select(self.prefix + "_Pelvis_Con.cv[1]", self.prefix + "_Pelvis_Con.cv[5]")
        cmds.scale(0.7, 0.7, 0.7, selection)
        cv3Pos = cmds.xform(cmds.ls(self.prefix + "_Pelvis_Con.cv[3]"), q=True, t=True, ws=True)
        cmds.move(cv3Pos[0], -0.4, 0, self.prefix + "_Pelvis_Con.cv[3]")
        cv7Pos = cmds.xform(cmds.ls(self.prefix + "_Pelvis_Con.cv[7]"), q=True, t=True, ws=True)
        cmds.move(cv7Pos[0], -0.4, 0, self.prefix + "_Pelvis_Con.cv[7]")

        cv1Pos = cmds.xform(cmds.ls(self.prefix + "_Pelvis_Con.cv[1]"), q=True, t=True, ws=True)
        cmds.move(cv1Pos[0], -0.2, cv1Pos[2], self.prefix + "_Pelvis_Con.cv[1]")
        cv5Pos = cmds.xform(cmds.ls(self.prefix + "_Pelvis_Con.cv[5]"), q=True, t=True, ws=True)
        cmds.move(cv5Pos[0], -0.2, cv5Pos[2], self.prefix + "_Pelvis_Con.cv[5]")

        cmds.scale(0.25,0.25,0.25, pelvis_ctrl)

        #### Moves Pelvis control to be around Pelvis joint ####

        pelvisPos = cmds.xform(cmds.ls(self.prefix + "_Pelvis_Jnt", type='joint'), q=True, t=True, ws=True)
        cmds.move(pelvisPos[0], pelvisPos[1]+0.05, pelvisPos[2], pelvis_ctrl)

        #### Sets pivot of control to be on joint, freezes transforms and parents control to centre control ####

        cmds.move(pelvisPos[0], pelvisPos[1], pelvisPos[2], self.prefix + "_Pelvis_Con"+ '.scalePivot', self.prefix + "_Pelvis_Con" + '.rotatePivot', absolute=True)
        cmds.makeIdentity(pelvis_ctrl, apply = True, t = 1, r = 1, s = 1)
        cmds.parent(pelvis_ctrl, self.prefix + "_Centre_Con")

    def createSpines(self, *args):

        #### Creates spine controls based off spine joints and parents them correctly ####

        for i in range(0, self.spineCount - 1):
            spinePos = cmds.xform(cmds.ls(self.prefix + "_" + "Spine_" + str(i+1) + "_Jnt"), q=True, t=True, ws=True)
            spine = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_Spine_"+str(i+1)+"_Con")
            cmds.move(spinePos[0], spinePos[1], spinePos[2]-0.08, spine)
            cmds.scale(0.15,0.15,0.1,spine)
            cmds.move(spinePos[0], spinePos[1], spinePos[2], self.prefix + "_Spine_"+str(i+1)+"_Con" + '.scalePivot',  self.prefix + "_Spine_"+str(i+1)+"_Con" + '.rotatePivot', absolute=True)
            if i == 0:
                cmds.parent(spine, self.prefix + "_Centre_Con")
            else:
                cmds.parent(spine, self.prefix + "_Spine_"+str(i)+"_Con")

            cmds.makeIdentity(spine, apply = True, t = 1, r = 1, s = 1)

        #### Creates Chest control based off chest joint ####

        chestPos = cmds.xform(cmds.ls(self.prefix + "_" + "Chest_Jnt"), q=True, t=True, ws=True)
        chest = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_Chest_Con")
        cmds.move(chestPos[0], chestPos[1], chestPos[2]-0.08, self.prefix + "_Chest_Con")
        cmds.scale(0.15,0.15,0.1,chest)
        
        #### Sets pivot of control to be on joint, freezes transforms and parents control to spine control ####
        cmds.move(chestPos[0], chestPos[1], chestPos[2], self.prefix + "_Chest_Con"+ '.scalePivot', self.prefix + "_Chest_Con" + '.rotatePivot', absolute=True)
        cmds.parent(chest, self.prefix + "_Spine_" + str(self.spineCount -1) + "_Con")
        cmds.makeIdentity(chest, apply = True, t = 1, r = 1, s = 1)

    def createNeck(self, *args):

        #### Creates neck control based off neck joint ####
        
        neckPos = cmds.xform(cmds.ls(self.prefix + "_Neck_Jnt"), q=True, t=True, ws=True)
        neck = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_Neck_Con")
        cmds.move(neckPos[0], neckPos[1]+0.03, neckPos[2]+0.02, neck)
        cmds.rotate(23,0,0,neck)
        cmds.scale(0.07, 0.1, 0.1, neck)
        
        #### Sets pivot of control to be on joint, freezes transforms and parents control to chest control ####

        cmds.move(neckPos[0], neckPos[1], neckPos[2], self.prefix + "_Neck_Con"+ '.scalePivot', self.prefix + "_Neck_Con" + '.rotatePivot', absolute=True)
        cmds.parent(neck, self.prefix + "_Chest_Con")
        cmds.makeIdentity(neck, apply = True, t = 1, r = 1, s = 1)

    def createHead(self, *args):

        #### Creates head control based off head joint ####

        headPos = cmds.xform(cmds.ls(self.prefix + "_Head_Jnt"), q=True, t=True, ws=True)
        head = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_Head_Con")
        cmds.move(headPos[0], headPos[1]+0.09, headPos[2]+0.01, head)
        cmds.scale(0.13, 0.13, 0.13, head)

        #### Sets pivot of control to be on joint, freezes transforms and parents control to neck control ####

        cmds.move(headPos[0], headPos[1], headPos[2], self.prefix + "_Head_Con"+ '.scalePivot', self.prefix + "_Head_Con" + '.rotatePivot', absolute=True)
        cmds.parent(head, self.prefix + "_Neck_Con")
        cmds.makeIdentity(head, apply = True, t = 1, r = 1, s = 1)

        #### Creates jaw control based off jaw joint ####
        
        jawPos = cmds.xform(cmds.ls(self.prefix + "_Jaw_Jnt"), q=True, t=True, ws=True)
        jaw = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_Jaw_Con")
        cmds.move(jawPos[0], jawPos[1]-0.02, jawPos[2]+0.05, jaw)
        cmds.rotate(23,0,0,jaw)
        cmds.scale(0.08, 0.08, 0.08, jaw)

        #### Sets pivot of control to be on joint, freezes transforms and parents control to head control ####

        cmds.move(jawPos[0], jawPos[1], jawPos[2], self.prefix + "_Jaw_Con"+ '.scalePivot', self.prefix + "_Jaw_Con" + '.rotatePivot', absolute=True)
        cmds.parent(jaw, self.prefix + "_Head_Con")
        cmds.makeIdentity(jaw, apply = True, t = 1, r = 1, s = 1)

    def createClavicles(self, *args):

        # L Clavicle

        #### Creates L Clav control and edits shape of control ####

        L_clavPos = cmds.xform(cmds.ls(self.prefix + "_L_Clavicle_Jnt"), q=True, t=True, ws=True)
        L_clav = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_L_Clavicle_Con")

        cv3Pos = cmds.xform(cmds.ls(self.prefix + "_L_Clavicle_Con.cv[3]"), q=True, t=True, ws=True)
        cmds.move(cv3Pos[0], 0.2, 0, self.prefix + "_L_Clavicle_Con.cv[3]")
        cv7Pos = cmds.xform(cmds.ls(self.prefix + "_L_Clavicle_Con.cv[7]"), q=True, t=True, ws=True)
        cmds.move(cv7Pos[0], 0.2, 0, self.prefix + "_L_Clavicle_Con.cv[7]")

        cv1Pos = cmds.xform(cmds.ls(self.prefix + "_L_Clavicle_Con.cv[1]"), q=True, t=True, ws=True)
        cmds.move(cv1Pos[0], -0.3, cv1Pos[2], self.prefix + "_L_Clavicle_Con.cv[1]")
        cv5Pos = cmds.xform(cmds.ls(self.prefix + "_L_Clavicle_Con.cv[5]"), q=True, t=True, ws=True)
        cmds.move(cv5Pos[0], -0.3, cv5Pos[2], self.prefix + "_L_Clavicle_Con.cv[5]")

        #### Moves L Clav control to be around L Clav joint ####

        cmds.move(L_clavPos[0]+0.03, L_clavPos[1]+0.06, L_clavPos[2]-0.05, L_clav)
        cmds.rotate(0,0,-11,L_clav)
        cmds.scale(0.06, 0.08, 0.11, L_clav)

        #### Sets pivot of control to be on joint, freezes transforms and parents control to chest control ####

        cmds.move(L_clavPos[0], L_clavPos[1], L_clavPos[2], self.prefix + "_L_Clavicle_Con"+ '.scalePivot', self.prefix + "_L_Clavicle_Con" + '.rotatePivot', absolute=True)
        cmds.parent(L_clav, self.prefix + "_Chest_Con")
        cmds.makeIdentity(L_clav, apply = True, t = 1, r = 1, s = 1)

        # R Clavicle

        #### Creates R Clav control and edits shape of control ####

        R_clavPos = cmds.xform(cmds.ls(self.prefix + "_R_Clavicle_Jnt"), q=True, t=True, ws=True)
        R_clav = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_R_Clavicle_Con")

        cv3Pos = cmds.xform(cmds.ls(self.prefix + "_R_Clavicle_Con.cv[3]"), q=True, t=True, ws=True)
        cmds.move(cv3Pos[0], 0.2, 0, self.prefix + "_R_Clavicle_Con.cv[3]")
        cv7Pos = cmds.xform(cmds.ls(self.prefix + "_R_Clavicle_Con.cv[7]"), q=True, t=True, ws=True)
        cmds.move(cv7Pos[0], 0.2, 0, self.prefix + "_R_Clavicle_Con.cv[7]")

        cv1Pos = cmds.xform(cmds.ls(self.prefix + "_R_Clavicle_Con.cv[1]"), q=True, t=True, ws=True)
        cmds.move(cv1Pos[0], -0.3, cv1Pos[2], self.prefix + "_R_Clavicle_Con.cv[1]")
        cv5Pos = cmds.xform(cmds.ls(self.prefix + "_R_Clavicle_Con.cv[5]"), q=True, t=True, ws=True)
        cmds.move(cv5Pos[0], -0.3, cv5Pos[2], self.prefix + "_R_Clavicle_Con.cv[5]")

        #### Moves R Clav control to be around R Clav joint ####

        cmds.move(R_clavPos[0]-0.03, R_clavPos[1]+0.06, R_clavPos[2]-0.05, R_clav)
        cmds.rotate(0,0,11,R_clav)
        cmds.scale(0.06, 0.08, 0.11, R_clav)

        #### Sets pivot of control to be on joint, freezes transforms and parents control to chest control ####

        cmds.move(R_clavPos[0], R_clavPos[1], R_clavPos[2], self.prefix + "_R_Clavicle_Con"+ '.scalePivot', self.prefix + "_R_Clavicle_Con" + '.rotatePivot', absolute=True)
        cmds.parent(R_clav, self.prefix + "_Chest_Con")
        cmds.makeIdentity(R_clav, apply = True, t = 1, r = 1, s = 1)
        
    def createWrists(self, *args):

        # L Wrist

        #### Creates L Wrist control based off L Wrist joint ####

        L_wristPos = cmds.xform(cmds.ls(self.prefix + "_L_Wrist_Jnt"), q=True, t=True, ws=True)
        L_wrist = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_L_Wrist_Con")
        cmds.move(L_wristPos[0], L_wristPos[1], L_wristPos[2], L_wrist)
        cmds.rotate(0,0,90, L_wrist)
        cmds.scale(0.07, 0.07, 0.07, L_wrist)
        
        #### Sets pivot of control to be on joint, freezes transforms and parents control to L Clav control ####
        
        cmds.move(L_wristPos[0], L_wristPos[1], L_wristPos[2], self.prefix + "_L_Wrist_Con"+ '.scalePivot', self.prefix + "_L_Wrist_Con" + '.rotatePivot', absolute=True)
        cmds.parent(L_wrist, self.prefix + "_L_Clavicle_Con")
        cmds.makeIdentity(L_wrist, apply = True, t = 1, r = 1, s = 1)

        # R Wrist

        #### Creates R Wrist control based off R Wrist joint ####

        R_wristPos = cmds.xform(cmds.ls(self.prefix + "_R_Wrist_Jnt"), q=True, t=True, ws=True)
        R_wrist = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_R_Wrist_Con")
        cmds.move(R_wristPos[0], R_wristPos[1], R_wristPos[2], R_wrist)
        cmds.rotate(0,0,90, R_wrist)
        cmds.scale(0.07, 0.07, 0.07, R_wrist)
        
        #### Sets pivot of control to be on joint, freezes transforms and parents control to R Clav control ####

        cmds.move(R_wristPos[0], R_wristPos[1], R_wristPos[2], self.prefix + "_R_Wrist_Con"+ '.scalePivot', self.prefix + "_R_Wrist_Con" + '.rotatePivot', absolute=True)
        cmds.parent(R_wrist, self.prefix + "_R_Clavicle_Con")
        cmds.makeIdentity(R_wrist, apply = True, t = 1, r = 1, s = 1)

    def createFingers(self, *args):

        # Thumbs

        sides = ["L", "R"]

        for s in sides:

            allThumbs = cmds.ls(self.prefix + "_" + s + "_Thumb_*"  + "_Jnt", type='transform')

            for x, f in enumerate(allThumbs):
                pos = cmds.xform(f, q=True, t=True, ws=True)
                thumb = cmds.circle(nr = (1,0,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_" + s + "_Thumb_" + str(x+1) + "_Con")
                cmds.move(pos[0], pos[1], pos[2], thumb)
                cmds.scale(0.03, 0.03, 0.03, thumb)

                cmds.move(pos[0], pos[1], pos[2], self.prefix + "_" + s + "_Thumb_" + str(x+1) + "_Con" + '.scalePivot', self.prefix + "_" + s + "_Thumb_" + str(x+1) + "_Con" + '.rotatePivot', absolute=True)
                if x == 0:
                    cmds.parent(thumb, self.prefix + "_" + s + "_Wrist_Con")
                else:
                    cmds.parent(thumb, self.prefix + "_" + s + "_Thumb_" + str(x) + "_Con")
                cmds.makeIdentity(thumb, apply = True, t = 1, r = 1, s = 1)

        # Fingers

        for s in sides:

            for i in range(1, self.fingerCount):

                allFingers = cmds.ls(self.prefix + "_" + s + "_Finger_" + str(i) + "*_Jnt", type='transform')

                for x, f in enumerate(allFingers):
                    pos = cmds.xform(f, q=True, t=True, ws=True)
                    finger = cmds.circle(nr = (1,0,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + "_" + s + "_Finger_" + str(i) + "_" + str(x+1) + "_Con")
                    cmds.move(pos[0], pos[1], pos[2], finger)
                    cmds.scale(0.03, 0.03, 0.03, finger)

                    cmds.move(pos[0], pos[1], pos[2], self.prefix + "_" + s + "_Finger_" + str(i) + "_" + str(x+1) + "_Con" + '.scalePivot', self.prefix + "_" + s + "_Finger_" + str(i) + "_" + str(x+1) + "_Con" + '.rotatePivot', absolute=True)
                    if x == 0:
                        cmds.parent(finger, self.prefix + "_" + s + "_Wrist_Con")
                    else:
                        cmds.parent(finger, self.prefix + "_" + s + "_Finger_" + str(i) + "_" + str(x) + "_Con")
                    cmds.makeIdentity(finger, apply = True, t = 1, r = 1, s = 1)


        




    def createFeet(self, *args):

        # L Foot

        #### Creates L Foot control based off L INV heel joint ####

        L_Foot = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, s = 8, name = self.prefix + "_L_Foot_Con")
        selection = cmds.select(self.prefix + "_L_Foot_Con.cv[3]", self.prefix + "_L_Foot_Con.cv[7]")
        cmds.scale(0.7, 0.7, 0.7, selection)
        cmds.scale(0.09,0.07,0.18, L_Foot)

        L_FootPos = cmds.xform(cmds.ls(self.prefix + "_L_INV_Heel_Jnt", type='joint'), q=True, t=True, ws=True)
        cmds.move(L_FootPos[0]+0.01, L_FootPos[1], L_FootPos[2]+0.07, L_Foot)
        cmds.rotate(0,3.5,0, L_Foot)

        #### Sets pivot of control to be on joint, freezes transforms and parents control to Global control ####

        cmds.move(L_FootPos[0], L_FootPos[1], L_FootPos[2], self.prefix + "_L_Foot_Con"+ '.scalePivot', self.prefix + "_L_Foot_Con" + '.rotatePivot', absolute=True)
        cmds.makeIdentity(L_Foot, apply = True, t = 1, r = 1, s = 1)
        cmds.parent(L_Foot, self.prefix + "_Global_Con")

        # R Foot

        #### Creates R Foot control based off R INV heel joint ####

        R_Foot = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, s = 8, name = self.prefix + "_R_Foot_Con")
        selection = cmds.select(self.prefix + "_R_Foot_Con.cv[3]", self.prefix + "_R_Foot_Con.cv[7]")
        cmds.scale(0.7, 0.7, 0.7, selection)
        cmds.scale(0.09,0.07,0.18, R_Foot)

        R_FootPos = cmds.xform(cmds.ls(self.prefix + "_R_INV_Heel_Jnt", type='joint'), q=True, t=True, ws=True)
        cmds.move(R_FootPos[0]-0.01, R_FootPos[1], R_FootPos[2]+0.07, R_Foot)
        cmds.rotate(0,-3.5,0, R_Foot)

        #### Sets pivot of control to be on joint, freezes transforms and parents control to Global control ####

        cmds.move(R_FootPos[0], R_FootPos[1], R_FootPos[2], self.prefix + "_R_Foot_Con"+ '.scalePivot', self.prefix + "_R_Foot_Con" + '.rotatePivot', absolute=True)
        cmds.makeIdentity(R_Foot, apply = True, t = 1, r = 1, s = 1)
        cmds.parent(R_Foot, self.prefix + "_Global_Con")

    def createPolVectors(self, *args):

        #### Create Pole Vector Controls and set their shape ####

        polVecs = ["_L_Elbow", "_R_Elbow", "_L_Knee", "_R_Knee"]

        for i in polVecs:

            if "Elbow" in i:
                j = -0.3
            else:
                j = 0.3

            Ctrl = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = self.conRadius, degree = 3, name = self.prefix + i + "_Con")

            cmds.xform(self.prefix + i + "_Con.cv[0]", t=(-0.107, 0, 0.227), r=True)
            cmds.xform(self.prefix + i + "_Con.cv[1]", t=(0, 0, 1.084), r=True)
            cmds.xform(self.prefix + i + "_Con.cv[2]", t=(0.104, 0, 0.236), r=True)
            cmds.xform(self.prefix + i + "_Con.cv[3]", t=(0.378, 0, 0), r=True)
            cmds.xform(self.prefix + i + "_Con.cv[4]", t=(0.553, 0, 0), r=True)
            cmds.xform(self.prefix + i + "_Con.cv[5]", t=(0, 0, 0), r=True)
            cmds.xform(self.prefix + i + "_Con.cv[6]", t=(-0.508, 0, 0), r=True)
            cmds.xform(self.prefix + i + "_Con.cv[7]", t=(-0.395, 0, 0), r=True)

            cmds.scale(0.1,0.1,0.1,Ctrl)

            CtrlPos = cmds.xform(cmds.ls(self.prefix + i + "_Jnt"), q=True, t=True, ws=True)

            #### Sets pivot of control to be on joint, freezes transforms and parents control to Global control ####

            #if "Knee" in i:
                #pass
            #else:
                #cmds.move(CtrlPos[0], CtrlPos[1], CtrlPos[2] + j, Ctrl)
            
            cmds.move(CtrlPos[0], CtrlPos[1], CtrlPos[2] + j, Ctrl)
            cmds.rotate(0,0,90, Ctrl)
            cmds.makeIdentity(Ctrl, apply = True, t = 1, r = 1, s = 1)
            cmds.parent(Ctrl, self.prefix + "_Global_Con")

    def alignKneeVectors(self, *args):

        sides = ["_L_", "_R_"]

        for i in sides:

            kneeCon = cmds.ls(self.prefix + i + "Knee_Con")
            
            cmds.parent(kneeCon, w=True)

            heelPos = cmds.xform(cmds.ls(self.prefix + i + "INV_Heel_Jnt", type='joint'), q=True, t=True, ws=True)
            hipPos = cmds.xform(cmds.ls(self.prefix + i + "Hip_Jnt", type='joint'), q=True, t=True, ws=True)
            kneePos = cmds.xform(cmds.ls(self.prefix + i + "Knee_Jnt", type='joint'), q=True, t=True, ws=True)
      
            createPolyPoint = cmds.polyCreateFacet(p=[(hipPos), (kneePos), (heelPos)], ch=False)
            conPointConstraint = cmds.pointConstraint(cmds.ls(self.prefix + i + "Knee_Jnt", type='joint'), kneeCon)
            nConstraint = cmds.normalConstraint(createPolyPoint[0], kneeCon)
            cmds.delete(conPointConstraint)
            cmds.delete(nConstraint)
            cmds.delete(createPolyPoint)

            cmds.move(0,0,0.3*self.conRadius, kneeCon, os=True, r=True)
            #cmds.makeIdentity(kneeCon, apply = True, t = 1, r = 1, s = 1)
            #cmds.parent(kneeCon, self.prefix + "_Global_Con")

            





def setControllers(spineCount, fingerCount, prefix):
    
    #### Set Pivot and freeze transforms if the user has edited any of the controls to their preference ####

    controls = ["_Centre", "_Pelvis", "_Chest", "_Head", "_Neck", "_Jaw", "_L_Clavicle", "_R_Clavicle", "_L_Wrist", "_R_Wrist"]

    for i in controls:
        control = cmds.ls(prefix + i + "_Con")
        controlPos = cmds.xform(cmds.ls(prefix + i + "_Jnt", type='joint'), q=True, t=True, ws=True)
        cmds.move(controlPos[0], controlPos[1], controlPos[2], prefix + i + "_Con"+ '.scalePivot', prefix + i + "_Con" + '.rotatePivot', absolute=True)
        cmds.makeIdentity(control, apply = True, t = 1, r = 1, s = 1)

    for i in range(0, spineCount - 1):
        control = cmds.ls(prefix + "_" + "Spine_" + str(i+1) + "_Con")
        controlPos = cmds.xform(cmds.ls(prefix + "_" + "Spine_" + str(i+1) + "_Jnt", type='joint'), q=True, t=True, ws=True)
        cmds.move(controlPos[0], controlPos[1], controlPos[2], prefix + "_" + "Spine_" + str(i+1) + "_Con"+ '.scalePivot', prefix + "_" + "Spine_" + str(i+1) + "_Con" + '.rotatePivot', absolute=True)
        cmds.makeIdentity(control, apply = True, t = 1, r = 1, s = 1)


    sides = ["L", "R"]

    for s in sides:

        allThumbs = cmds.ls(prefix + "_" + s + "_Thumb_*"  + "_Jnt", type='transform')

        for x, f in enumerate(allThumbs):
            pos = cmds.xform(f, q=True, t=True, ws=True)
            cmds.move(pos[0], pos[1], pos[2], prefix + "_" + s + "_Thumb_" + str(x+1) + "_Con" + '.scalePivot', prefix + "_" + s + "_Thumb_" + str(x+1) + "_Con" + '.rotatePivot', absolute=True)
            cmds.makeIdentity(f, apply = True, t = 1, r = 1, s = 1)

        for i in range(1, fingerCount):

            allFingers = cmds.ls(prefix + "_" + s + "_Finger_" + str(i) + "*_Jnt", type='transform')

            for x, f in enumerate(allFingers):
                pos = cmds.xform(f, q=True, t=True, ws=True)
                cmds.move(pos[0], pos[1], pos[2], prefix + "_" + s + "_Finger_" + str(i) + "_" + str(x+1) + "_Con" + '.scalePivot', prefix + "_" + s + "_Finger_" + str(i) + "_" + str(x+1) + "_Con" + '.rotatePivot', absolute=True)
                cmds.makeIdentity(f, apply = True, t = 1, r = 1, s = 1)

        # Feet

        control = cmds.ls(prefix + "_" + s + "_Foot_Con")
        controlPos = cmds.xform(cmds.ls(prefix + "_" + s + "_INV_Heel_Jnt", type='joint'), q=True, t=True, ws=True)
        cmds.move(controlPos[0], controlPos[1], controlPos[2], prefix + "_" + s + "_Foot_Con"+ '.scalePivot', prefix + "_" + s + "_Foot_Con" + '.rotatePivot', absolute=True)
        cmds.makeIdentity(control, apply = True, t = 1, r = 1, s = 1)


    

    polVecs = ["_L_Elbow", "_R_Elbow"]

    for i in polVecs:
    
        if "Elbow" in i:
                j = -0.3
        else:
                j = 0.3

        control = cmds.ls(prefix + i + "_Con")
        controlPos = cmds.xform(cmds.ls(prefix + i + "_Jnt", type='joint'), q=True, t=True, ws=True)
        cmds.move(controlPos[0], controlPos[1], controlPos[2] + j, prefix + i + "_Con"+ '.scalePivot', prefix + i + "_Con" + '.rotatePivot', absolute=True)
        cmds.makeIdentity(control, apply = True, t = 1, r = 1, s = 1)

    kneeCons = ["_L_Knee", "_R_Knee"]

    for k in kneeCons:
        kneeCon = cmds.ls(prefix + k + "_Con")
        cmds.makeIdentity(kneeCon, apply = True, t = 1, r = 1, s = 1)
        cmds.parent(kneeCon, prefix + "_Global_Con")

def mirrorControllers(prefix):

        allLeftCon = cmds.ls(prefix + "_L_" + "*_Con")
        #leftCon = cmds.listRelatives(*allLeftCon, p = True, f = True)

        #print allLeftCon
        
        allRightCon = cmds.ls(prefix + "_R_" + "*_Con")
        #rightCon = cmds.listRelatives(*allRightCon, p = True, f = True)

        #print allRightCon

        for i,l in enumerate(allLeftCon):
            pos = cmds.xform(l, q = True, t=True, ws=True)
            cmds.move(-pos[0], pos[1], pos[2], allRightCon[i])

            for x in range(0,20):
                lCVPos = cmds.xform(l + ".cv[" + str(x) + "]", q=True, t=True, ws=True)
                rCV = allRightCon[i] + ".cv[" + str(x) + "]"
                cmds.move(-lCVPos[0], lCVPos[1], lCVPos[2], rCV)