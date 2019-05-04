# Auto Rigger v1.1

import maya.cmds as cmds
from functools import partial

# Import Autorig Scripts 

import AutoRiggerLocators as Locators
import AutoRiggerJoints as Joints
import AutoRiggerSecondaryLocators as SecondaryLocators
import AutoRiggerControllers as Controllers
import AutoRiggerCreateIK as CreateIK
import AutoRiggerConstraints as Constraints

# Reload Autorig scripts so they are up to date.

reload(Locators)
reload(Joints)
reload(SecondaryLocators)
reload(Controllers)
reload(CreateIK)
reload(Constraints)

editMode = True

class AutoRig(object):

    #### Sets up unit size and checks if window is already open.

    def __init__(self):
        name = "AutoRigger_v1_1"
        self.name = name
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name, wnd=True)
            cmds.windowPref(name, r=True)
        
        cmds.currentUnit(linear='meter')
        #self.locatorSize = 0.1
        
        #### Runs function to create UI
        self.makeUI()
        

############ UI ############

    def makeUI(self):

        global editMode

        # Background colour for all labels.
        label_colour = (0.450, 0.541, 0.858)

        cmds.window(self.name)

        cmds.rowColumnLayout(nc = 2)

        cmds.frameLayout(label="Name Rig", bgc=label_colour)

        # Prefix to be assigned throughout Rig to all locators, joints and controls.
        cmds.text(label="Rig Name Prefix")
        self.prefixField = cmds.textField(text='Tom')

        # Creates label for Step 1 and sliders to control spine count and finger count.
        cmds.frameLayout(label="Step 1: Skeleton Options", bgc=label_colour)

        self.spineCount = cmds.intSliderGrp(l = "Spine Count (Incl. Chest)", min = 2, max = 10, value = 4, step = 1, field = True)
        self.fingerCount = cmds.intSliderGrp(l = "Finger Count (Incl. Thumb)", min = 1, max = 10, value = 5, step = 1, field = True)

        # Creates label for Step 2 and buttons to create, delete and mirror locators.
        cmds.frameLayout(label="Step 2: Create Locators", bgc=label_colour)
        
        cmds.button(l = "Create Locators", w = 200, c = self.createBaseLocators)
        cmds.button(l = "Delete Locators", w=200, c=self.deleteLocators)
        cmds.button(l = "Mirror L->R", w = 200, c = self.mirrorLocators)

        cmds.text(label="Scale Locator Group to match size of character")

        # Creates label for Step 3 and buttons to create and delete secondary locators.
        cmds.frameLayout(label="Step 3: Create Secondary Locators", bgc=label_colour)

        cmds.button(l = "Create Secondary Locators", w = 200, c = self.createSecondaryLocators)
        cmds.button(l = "Delete Secondary Locators", w = 200, c = self.deleteSecondaryLocators)

        
        #cmds.button(l = "Lock/Unlock", w = 200, c = partial(self.lockAll,editMode))

        # Creates label for Step 4 and buttons to create and delete joints
        cmds.frameLayout(label="Step 4: Create Skeleton", bgc=label_colour)

        cmds.button(l = "Create Joints", w = 200, c = self.createJoints)
        cmds.button(l = "Delete Joints", w = 200, c = self.deleteJoints)

        # Creates label for Step 5 and buttons to create and set controllers
        cmds.frameLayout(label="Step 5: Create Controllers", bgc=label_colour)

        cmds.button(l = "Create Controllers", w=200, c=self.createControllers)
        
        cmds.text(label="Use to change size of controller without affecting child controllers:")

        cmds.button(l = "Select CV's of Controller", w=200, c=self.editControllers)

        cmds.button(l = "Mirror L->R", w = 200, c = self.mirrorControllers)

        cmds.button(l = "Set Controllers", w=200, c=self.setControllers)
        cmds.text(label="Won't change or affect knee pole vector controllers.")

        # Creates label for Step 6 and buttons to create IK's and constraints
        cmds.frameLayout(label="Step 6: Create IK and Constraints", bgc=label_colour)

        cmds.button(l = "Create IK", w=200, c=self.createIK)
        cmds.button(l = "Create Constraints", w=200, c=self.createContraints)

        # Creates label for Step 7 and buttons to bind skin
        cmds.frameLayout(label="Step 7: Bind Skin", bgc=label_colour)

        cmds.button(l = "Bind Skin", w=200, c=self.bindSkin)

        # Creates label for Step 8 and buttons to finalise
        cmds.frameLayout(label="Step 8: Finalise Rig", bgc=label_colour)

        cmds.button(l = "Finalise Rig", w=200, c=self.finalizeRig)
        
        # Creates UI window
        cmds.showWindow()

############ Code ############

    def createBaseLocators(self, *args):
        # Calls to locator script to create locators
        spineCount = cmds.intSliderGrp(self.spineCount, q = True, v = True)
        fingerCount = cmds.intSliderGrp(self.fingerCount, q=True, v=True)
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        #prefix = self.prefix
        Locators.createLocators(spineCount, fingerCount, prefix)

    def deleteLocators(self, *args):

        # Calls to locator script to delete locators
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        Locators.deleteLocators(prefix)
    

    def mirrorLocators(self, *args):

        # Calls to locator script to mirror locators
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        Locators.mirrorLocators(prefix)

    def createSecondaryLocators(self, *args):

        # Calls to secondary script to create secondary locators
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        SecondaryLocators.createSecondaryLocators(prefix)

    def deleteSecondaryLocators(self, *args):

        # Calls to secondary script to delete secondary locator
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        SecondaryLocators.deleteSecondaryLocators(prefix)

    def createJoints(self, *args):

        # Calls to joints script to create joints
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        fingerCount = cmds.intSliderGrp(self.fingerCount, q=True, v=True)
        Joints.createJoints(prefix, fingerCount)

        cmds.hide( cmds.ls( prefix + "_Loc_Grp" ) )
        cmds.hide( cmds.ls( prefix + "_Secondary_Loc_Grp" ) )
        
    def deleteJoints(self, *args):

        # Calls to joints script to delete joints
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        Joints.deleteJoints(prefix)

    def createControllers(self, *args):

        # Calls to controllers script to create controllers
        spineCount = cmds.intSliderGrp(self.spineCount, q = True, v = True)
        fingerCount = cmds.intSliderGrp(self.fingerCount, q=True, v=True)
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        Controllers.createControllers(spineCount,fingerCount,prefix)

    def editControllers(self, *args):

        selectedController = cmds.ls(sl=True)

        cvList = []

        for i in range(0,20):
            controlVertex = selectedController[0] + ".cv[" + str(i) + "]"
            cvList.append(controlVertex)

        print cvList

        cmds.select(cvList)

    def mirrorControllers(self, *args):

        prefix = cmds.textField(self.prefixField, query=True, text=True)

        Controllers.mirrorControllers(prefix) 


    def setControllers(self, *args):
        
        # Calls to controllers script to set controllers
        spineCount = cmds.intSliderGrp(self.spineCount, q = True, v = True)
        fingerCount = cmds.intSliderGrp(self.fingerCount, q=True, v=True)
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        Controllers.setControllers(spineCount, fingerCount, prefix)

    def createIK(self, *args):

        # Calls to IK script to create IK
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        CreateIK.IKHandles(prefix)

    def createContraints(self, *args):

        # Calls to constraints script to create constraints
        spineCount = cmds.intSliderGrp(self.spineCount, q = True, v = True)
        fingerCount = cmds.intSliderGrp(self.fingerCount, q=True, v=True)
        prefix = cmds.textField(self.prefixField, query=True, text=True)

        Constraints.createContraints(spineCount, fingerCount, prefix)

    def bindSkin(self, *args):

        # Calls to constraints script to bind skin to mesh selected
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        Constraints.bindSkin(prefix)

    def finalizeRig(self, *args):

        # Calls to constraints script to set up inverse foot roll, set the hierarchy and to set up the display layers.
        prefix = cmds.textField(self.prefixField, query=True, text=True)
        Constraints.inverseFoot(prefix)
        Constraints.orangizeRig(prefix)
        Constraints.disLayer(prefix)


    # Function to lock locators, currently unused. 
    def lockAll(self, lockState, *args):
        global editMode
        
        axis = ['x', 'y', 'z']
        attr = ['t', 'r', 's']

        nodes = cmds.listRelatives("Loc_*", allParents=True)

        lockState = editMode

        #print lockState

        for axe in axis:
            for att in attr:
                for node in nodes:
                    cmds.setAttr(node+'.'+att+axe, lock = lockState)

        if editMode == False:
            editMode = True
        else: 
            editMode = False
