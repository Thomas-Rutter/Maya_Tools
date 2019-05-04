# BadGeoFinder v1.1

import maya.cmds as cmds
import os, re, fnmatch, random, webbrowser

class BadGeoFind(object):

    def __init__(self): ##############################
        name = 'BadGeoFinder_v1_1'
        self.name = name
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name)
        
        self.makeUI()

    def makeUI(self): ##############################

        # Create UI

        windowName = cmds.window(self.name)
        cmds.window(windowName, e=True, rtf=True)
        label_colour = (0.450, 0.541, 0.858)
        column = cmds.columnLayout('BGDColumns', adj=True)
        cmds.setParent(column)

        # Buttons to check geo

        cmds.frameLayout(label="Geometry Type", bgc=label_colour)

        cmds.columnLayout(adj=True)

        cmds.button(label="Triangles", h=25, c = self.bGFTriangles)
        cmds.button(label="Quads", h=25, c = self.bGFQuads)
        cmds.button(label="N-Gons", h=25, c = self.bGFNGons)
        cmds.button(label="Concave", h=25, c = self.bGFConcave)
        cmds.button(label="Lamina", h=25, c = self.bGFLamina)
        cmds.button(label="Holes", h=25, c = self.bGFHole)
        cmds.button(label="Non-Manifold", h=25, c = self.bGFNonM)
        cmds.button(label="All", h=25, c= self.bGFAll)

        # Results

        cmds.frameLayout(label="Results", bgc=label_colour)

        self.bGF_results = cmds.textField( en=True, ed=False)
    
        cmds.columnLayout(adj=True)

        cmds.button(label="Create Camera", h=25, c = self.createCamera)

        cmds.frameLayout(label="Camera Instructions", bgc=label_colour)

        cmds.columnLayout(adj=True)

        cmds.text(label="Each keyframe will have different face focused." 
        + '\n' + "All you have to is tumble around with the camera and face will be the orbit point.")

        # Show Window

        cmds.showWindow()
    
    def bGFTriangles(self, *args):

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3 ,t = 0x0008, sz=1)
        cmds.polySelectConstraint(dis=True)

        bGFPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bGF_results, e=True, tx=("%s Triangle(s)" % int(bGFPolys)))
        except:
            cmds.textField(self.bGF_results, e=True, tx=("Nothing is selected."))

    def bGFQuads(self, *args):

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3 ,t = 0x0008, sz=2)
        cmds.polySelectConstraint(dis=True)

        bGFPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bGF_results, e=True, tx=("%s Quad(s)" % int(bGFPolys)))
        except:
            cmds.textField(self.bGF_results, e=True, tx=("Nothing is selected."))

    def bGFNGons(self, *args):

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3 ,t = 0x0008, sz=3)
        cmds.polySelectConstraint(dis=True)

        bGFPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bGF_results, e=True, tx=("%s N-Gon(s)" % int(bGFPolys)))
        except:
            cmds.textField(self.bGF_results, e=True, tx=("Nothing is selected."))
    
    def bGFConcave(self, *args):

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3 ,t = 0x0008, c=1)
        cmds.polySelectConstraint(dis=True)

        bGFPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bGF_results, e=True, tx=("%s Concave(s)" % int(bGFPolys)))
        except:
            cmds.textField(self.bGF_results, e=True, tx=("Nothing is selected."))

    def bGFLamina(self, *args):

        cmds.selectMode(q=True, co=True)

        p = cmds.polyInfo(lf=True)

        if p == None:
            bGFPolys = 0
            cmds.select(d=True)
        else:
            cmds.select(p)
            bGFPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bGF_results, e=True, tx=("%s Lamina" % int(bGFPolys)))
        except:
            cmds.textField(self.bGF_results, e=True, tx=("Nothing is selected."))
    
    def bGFHole(self, *args):

        cmds.selectMode(q=True, co=True)

        cmds.polySelectConstraint(m=3 ,t = 0x0008, h=1)
        cmds.polySelectConstraint(dis=True)

        bGFPolys = cmds.polyEvaluate(fc=True)

        try:
            cmds.textField(self.bGF_results, e=True, tx=("%s Hole(s)" % int(bGFPolys)))
        except:
            cmds.textField(self.bGF_results, e=True, tx=("Nothing is selected."))

    def bGFNonM(self, *args):

        cmds.selectMode(q=True, co=True)

        p = cmds.polyInfo(nme=True)

        if p != None:
            cmds.select(p)

        bGFPolys = cmds.polyEvaluate(ec=True)

        try:
            cmds.textField(self.bGF_results, e=True, tx=("%s Non-Mainfold(s)" % int(bGFPolys)))
        except:
            cmds.textField(self.bGF_results, e=True, tx=("Nothing is selected."))

    def bGFAll(self, *args):
        
        allGeo = []
        
        cmds.selectMode(q=True, co=True)

        

        for i in range(1,4):

            cmds.polySelectConstraint(m=3 ,t = 0x0008, sz=i)
            cmds.polySelectConstraint(dis=True)

            bGFPolys = cmds.polyEvaluate(fc=True)

            allGeo.append(bGFPolys)

        print allGeo

        try:
            cmds.textField(self.bGF_results, e=True, tx=("%s Triangle(s)" % int(allGeo[0]) + '\n' + "%s Quad(s)" % int(allGeo[1]) + '\n' + "%s N-Gons(s)" % int(allGeo[2]) ))
        except:
            cmds.textField(self.bGF_results, e=True, tx=("Nothing is selected."))

    
    def createCamera(self, *args):
        selectedFaces = cmds.ls(sl=True, fl=True)
        cameraName = cmds.camera(name="BadGeoFinderCam", ncp=0.001)
        cameraShape = cameraName[1]
        cmds.currentTime(0, e=True)
        for face in range(len(selectedFaces)):
            currentTime = cmds.currentTime(q=True)
            cmds.currentTime(currentTime+1, e=True)
            print "target = " + str(selectedFaces[face])
            face_pos=cmds.xform(selectedFaces[face], q=True, bb=True, ws=True)
            x_pos = (face_pos[0]+face_pos[3])/2
            y_pos = (face_pos[1]+face_pos[4])/2
            z_pos = (face_pos[2]+face_pos[5])/2
            cube = cmds.polyCube(n = "BGF_Cube_"+str(face))
            print cube
            cmds.move(x_pos, y_pos, z_pos, cube)             
            nConstraint = cmds.normalConstraint(selectedFaces[face], cube)
            cube_pos = cmds.xform(cube, q=True, t=True, ws=True)
            cube_rot = cmds.xform(cube, q=True, ro=True, ws=True)
            cmds.xform(cameraName, t=cube_pos, ro=cube_rot, ws=True)
            cmds.rotate(0, 45, 0, cameraName, r=True)
            cmds.select(selectedFaces[face])
            cmds.viewFit(cameraShape, f=0.5) 
            cmds.select(cameraName)
            cmds.setKeyframe()
            
            cmds.delete(nConstraint, cube)
            cmds.select(selectedFaces)

    def showFace(self, *args):
        selectedFaces = cmds.ls(sl=True, fl=True)
        



        