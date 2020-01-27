import maya.cmds as cmds
import AutoRiggerLocators

############################
#######  Ik  Script  #######
############################

Locators = reload(AutoRiggerLocators)

def IKHandles(prefix):
    
    # Arms

    #cmds.makeIdentity(cmds.ls(prefix + "*Jnt"), apply = True, t = 1, r = 1, s = 1)

    cmds.ikHandle(name= prefix + "_L_Arm_IK", sj=cmds.ls(prefix + "_L_Shoulder_Jnt")[0], ee=cmds.ls(prefix + "_" + "L_ArmTwist_Jnt")[0], sol="ikRPsolver")
    cmds.ikHandle(name= prefix + "_R_Arm_IK", sj=cmds.ls(prefix + "_R_Shoulder_Jnt")[0], ee=cmds.ls(prefix + "_" + "R_ArmTwist_Jnt")[0], sol="ikRPsolver")
    
    L_WristPos = cmds.xform(cmds.ls(prefix + "_L_Wrist_Jnt"), q=True, t=True, ws=True)
    R_WristPos = cmds.xform(cmds.ls(prefix + "_R_Wrist_Jnt"), q=True, t=True, ws=True)

    leftIK = cmds.ikHandle(prefix + "_L_Arm_IK",q=True, ee=True)
    rightIK = cmds.ikHandle(prefix + "_R_Arm_IK",q=True, ee=True)

    cmds.move(L_WristPos[0],L_WristPos[1],L_WristPos[2], leftIK+".scalePivot", leftIK+".rotatePivot")
    cmds.move(R_WristPos[0],R_WristPos[1],R_WristPos[2], rightIK+".scalePivot", rightIK+".rotatePivot")

    # Legs

    cmds.ikHandle(name= prefix + "_L_Leg_IK", sj=cmds.ls(prefix + "_L_Hip_Jnt")[0], ee=cmds.ls(prefix + "_" + "L_Ankle_Jnt")[0], sol="ikRPsolver")
    cmds.ikHandle(name= prefix + "_R_Leg_IK", sj=cmds.ls(prefix + "_R_Hip_Jnt")[0], ee=cmds.ls(prefix + "_" + "R_Ankle_Jnt")[0], sol="ikRPsolver")
    
    cmds.ikHandle(name= prefix + "_L_INV_Ball_IK", sj=cmds.ls(prefix + "_L_Ankle_Jnt")[0], ee=cmds.ls(prefix + "_" + "L_Foot_Ball_Jnt")[0], sol="ikSCsolver")
    cmds.ikHandle(name= prefix + "_L_INV_Toe_IK", sj=cmds.ls(prefix + "_L_Foot_Ball_Jnt")[0], ee=cmds.ls(prefix + "_" + "L_Toe_Jnt")[0], sol="ikSCsolver")
        
    cmds.ikHandle(name= prefix + "_R_INV_Ball_IK", sj=cmds.ls(prefix + "_R_Ankle_Jnt")[0], ee=cmds.ls(prefix + "_" + "R_Foot_Ball_Jnt")[0], sol="ikSCsolver")
    cmds.ikHandle(name= prefix + "_R_INV_Toe_IK", sj=cmds.ls(prefix + "_R_Foot_Ball_Jnt")[0], ee=cmds.ls(prefix + "_" + "R_Toe_Jnt")[0], sol="ikSCsolver")

    #cmds.parent(prefix + "_L_Arm_IK", prefix + "_L_Wrist_Con")

    #cmds.poleVectorConstraint( prefix + "_L_Elbow_Con", prefix + "_L_Arm_IK")
    #cmds.poleVectorConstraint( prefix + "_R_Elbow_Con", prefix + "_R_Arm_IK")
    cmds.poleVectorConstraint( prefix + "_L_Knee_Con", prefix + "_L_Leg_IK")
    cmds.poleVectorConstraint( prefix + "_R_Knee_Con", prefix + "_R_Leg_IK")
    