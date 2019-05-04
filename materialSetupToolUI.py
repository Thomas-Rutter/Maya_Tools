# Material Setup v1.4

import maya.cmds as cmds
import os, re, fnmatch, random, webbrowser, sys, difflib

class MaterialSetup(object):

    def __init__(self): ##############################
        name = "MaterialMaker_v1_4"
        self.name = name
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name, wnd=True)
            cmds.windowPref(name, r=True)
        
        self.makeUI()


    def makeUI(self): ################################
        window = cmds.window(self.name)
        cmds.window(window, e=True, resizeToFitChildren=True)
        label_colour = (0.450, 0.541, 0.858)
        column = cmds.columnLayout('MMUIColumns', adjustableColumn=True)
        cmds.setParent(column)
        # Create preset dropdown menu
        cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[ (1,260), (2,50), (3,50)])
        cmds.separator(h=15, style='none')
        cmds.separator(h=15, style='none')
        cmds.button(label='Help', command=self.onHelpClick, bgc=(.1, .1, .4))
        

        cmds.setParent(column)
        # Name Material
        cmds.frameLayout(label="Name Material", bgc=label_colour)
        self.material_Name_Field = cmds.textField(text='Tom')
        cmds.text(label=" You will select the diffuse file")
        # Renderer
        cmds.setParent(column)
        supported_engines = ['Arnold', 'Redshift']
        self.rendererOption = cmds.optionMenuGrp(label="Choose Renderer")
        for engine in supported_engines:
            cmds.menuItem(label=engine)
        # Specular or Metalness map selection
        cmds.setParent(column)
        cmds.frameLayout(label="Select Specular Maps", bgc=label_colour)
        cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[ (1,115), (2,95), (3,150)])
        cmds.radioCollection()
        self.specButton = cmds.radioButton(label="Specular Map")
        self.metalButton = cmds.radioButton(label="Metallic Map", select=True) 
        self.noSpecButton = cmds.radioButton(label="No Spec or Metallic Map")
        cmds.setParent(column)
        cmds.text(label=" Specular maps must have 'Spec' in file name"
         + '\n' + " Metallic maps must have 'Metal' in file name")
        #Roughness Map checkbox
        self.roughCheckbox = cmds.checkBox(label="Roughness Map",parent=column, value=True)
        cmds.setParent(column)
        cmds.text(label=" Roughness maps must have 'Rough' in file name")
        # Normal or Bump map selection
        cmds.setParent(column)
        cmds.frameLayout(label="Select Geometry Maps", bgc=label_colour)
        cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[ (1,115), (2,95), (3,120)])
        cmds.radioCollection()
        self.bumpButton = cmds.radioButton(label='Bump Map')
        self.normalButton = cmds.radioButton(label='Normal Map', select=True)
        self.noNormalButton = cmds.radioButton(label='No Normal or Bump Map')
        cmds.setParent(column)
        cmds.text(label=" Normal maps must have 'Nor' in file name"
         + '\n' + " Bump maps must have 'Bump' in file name")
        # Displacement or Height map selection
        cmds.setParent(column)
        cmds.frameLayout(label="Select Displacement Maps", bgc=label_colour)
        cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[ (1,115), (2,95), (3,185)])
        cmds.radioCollection()
        self.dispButton = cmds.radioButton(label='Displacement Map')
        self.heightButton = cmds.radioButton(label='Height Map', select=True)
        self.noDispButton = cmds.radioButton(label='No Displacement or Height Map')
        cmds.setParent(column)
        cmds.text(label=" Displacement maps must have 'Disp' in file name"
         + '\n' + " Height maps must have 'Height' in file name")
        # Extra map selection
        cmds.setParent(column)
        cmds.frameLayout(label="Select Extra Maps", bgc=label_colour)
        self.AOcheckBox = cmds.checkBox(label="AO Map")
        self.opacityCheckBox = cmds.checkBox(label="Opacity Map")
        # UDIM selection 
        cmds.setParent(column)
        cmds.frameLayout(label="Select UDIMs", bgc=label_colour)
        self.UDIMcheckBox = cmds.checkBox(label="Has UDIMS", parent=column)
        cmds.setParent(column)
        cmds.text(label=" Having UDIMs will cause Material to"
         + '\n' + " have absolute file paths")
        # File Type selection
        cmds.setParent(column)
        cmds.frameLayout(label="Select File Type", bgc=label_colour)
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[ (1,50), (2,50)])
        cmds.radioCollection()
        self.pngButton = cmds.radioButton(label='PNG', select=True)
        self.jpgButton = cmds.radioButton(label='JPG')
        self.exrButton = cmds.radioButton(label='EXR')
        self.tifButton = cmds.radioButton(label='TIF')

        cmds.setParent(column)
        cmds.button(label='Create', command=self.onCreateClick, bgc=(1, 1, 1))

        
        cmds.showWindow()

    def onHelpClick(self, *args):
        webbrowser.open('https://www.thomasgeorgerutter.com/uni/#/material-tool/')

    def onCreateClick(self, *args):
        # Set Material Name and allow all nodes to be correctly named.
        material_name_input = cmds.textField(self.material_Name_Field, query=True, text=True)
        material_name = material_name_input.replace(" ", "_")
        self.renderer = cmds.optionMenuGrp(self.rendererOption, q=True, v=True)
        print self.renderer
        self.material_name = material_name
        self.shader=material_name+"_Shader"
        self.shading_group=material_name+"_Shading_Group"
        self.place_2d_texture_node=material_name+"_2dtexture"
        self.file_node=material_name+"_File_Node"
        self.diffuse_file_node=material_name+"_Diffuse_File"
        
        # Link spec or metalness values
        self.specCheck = cmds.radioButton(self.specButton, q=True, select=True)
        self.metalCheck = cmds.radioButton(self.metalButton, q=True, select=True)
        
        # Link roughness values
        self.roughCheck = cmds.checkBox(self.roughCheckbox, q=True, v=True)

        # Link bump or normal values
        self.bumpCheck = cmds.radioButton(self.bumpButton, q=True, select=True)
        self.normalCheck = cmds.radioButton(self.normalButton, q=True, select=True)

        # Link Displacement or Height values
        self.dispCheck = cmds.radioButton(self.dispButton, q=True, select=True)
        self.heightCheck = cmds.radioButton(self.heightButton, q=True, select=True)

        # Link Extra Maps
        self.AOcheck = cmds.checkBox(self.AOcheckBox, q=True, v=True)
        self.opacityCheck = cmds.checkBox(self.opacityCheckBox, q=True, v=True)

        # Link UDIMS values
        self.UDIMcheck = cmds.checkBox(self.UDIMcheckBox, q=True, v=True)

        # Link File Type
        self.pngType = cmds.radioButton(self.pngButton, q=True, select=True)
        self.jpgType = cmds.radioButton(self.jpgButton, q=True, select=True)
        self.exrType = cmds.radioButton(self.exrButton, q=True, select=True)
        self.tifType = cmds.radioButton(self.tifButton, q=True, select=True)

        if self.pngType:
            fileType = '.png'
        elif self.jpgType:
            fileType = '.jp'
        elif self.exrType:
            fileType = '.exr'
        if self.tifType:
            fileType = '.tif'

        # Material is made
        self.createMaterial()
        self.createTextureFile("Diffuse")
        # Select Diffuse File
        self.selectDiffuseMap(self.material_name+"_Diffuse_File")
        # Create AO Map
        if self.AOcheck:
            self.createTextureFile("AO")
            self.getMaps("AO", fileType)
            self.connectAO()
        else:
            pass
        # Create Spec Map
        if self.specCheck:
            self.createTextureFile("Spec")
            self.getMaps("Spec", fileType)
            self.connectSpec()
        else:
            pass
        # Create Metalness Map
        if self.metalCheck:
            self.createTextureFile("Metal")
            self.getMaps("Metal", fileType)
            self.connectMetalness()
        else:
            pass
        # Create Roughness Map
        if self.roughCheck:
            self.createTextureFile("Rough")
            self.getMaps("Rough", fileType)
            self.connectRough()
        else:
            pass
        # Create Bump Map if bump map button is selected
        if self.bumpCheck:
            self.createTextureFile("Bump")
            self.getMaps("Bump", fileType)
            self.connectBump()
        else:
            pass
        # Create Normal Map if normal map button is selected
        if self.normalCheck:
            self.createTextureFile("Nor")
            self.getMaps("Nor", fileType)
            self.connectNormal()
        else:
            pass
        # Create Opacity Map if Opacity checkbox is selected
        if self.opacityCheck:
            self.createTextureFile("Opacity")
            self.getMaps("Opacity", fileType)
            self.connectOpacity()
        # Create Displacement Map if displacement button is selected
        if self.dispCheck:
            self.createTextureFile("Disp")
            self.getMaps("Disp", fileType)
            self.connectDisplacement()
        else:
            pass
        # Create Height Map if height button is selected
        if self.heightCheck:
            self.createTextureFile("Height")
            self.getMaps("Height", fileType)
            self.connectHeight()
        else:
            pass
        # Closes Window after process is complete
        if cmds.window(self.name, query=True, exists=True):
            cmds.deleteUI(self.name)

    #function to create material shader, shader group and 2d texture node
    def createMaterial(self):
        material_name=self.material_name
        #create a shader
        # Creates Arnold Shader
        if self.renderer == "Arnold":
            self.shader=cmds.shadingNode("aiStandardSurface",asShader=True, name=self.shader)
        # Creates Redshift Shader
        elif self.renderer == "Redshift":
            self.shader=cmds.shadingNode("RedshiftMaterial",asShader=True, name=self.shader)
        #create a shading group
        self.shading_group= cmds.sets(renderable=True,noSurfaceShader=True,empty=True, name=material_name+"_SG")
        #connect shader to sg surface shader
        cmds.connectAttr('%s.outColor' %self.shader ,'%s.surfaceShader' %self.shading_group)
        #create 2d texture node
        self.place_2d_texture_node=cmds.shadingNode("place2dTexture", asUtility=True, name=material_name+"_2dtexture")

    #function to create file node and attach to 2d texture node
    def createTextureFile(self, type):
        #create diffuse file texture node
        self.file_node=cmds.shadingNode("file",asTexture=True, name = self.material_name+"_"+type+"_File")
        #connect diffuse 2d texture node to diffuse file texture node
        self.place_2d_texture_node = self.material_name+"_2dtexture"
        place_2d_texture_node = self.place_2d_texture_node
        file_node = self.file_node
        cmds.connectAttr('%s.coverage' %place_2d_texture_node, '%s.coverage' %file_node)
        cmds.connectAttr('%s.translateFrame' %place_2d_texture_node, '%s.translateFrame' %file_node)
        cmds.connectAttr('%s.rotateFrame' %place_2d_texture_node, '%s.rotateFrame' %file_node)
        cmds.connectAttr('%s.mirrorU' %place_2d_texture_node, '%s.mirrorU' %file_node)
        cmds.connectAttr('%s.mirrorV' %place_2d_texture_node, '%s.mirrorV' %file_node)
        cmds.connectAttr('%s.stagger' %place_2d_texture_node, '%s.stagger' %file_node)
        cmds.connectAttr('%s.wrapU' %place_2d_texture_node, '%s.wrapU' %file_node)
        cmds.connectAttr('%s.wrapV' %place_2d_texture_node, '%s.wrapV' %file_node)
        cmds.connectAttr('%s.repeatUV' %place_2d_texture_node, '%s.repeatUV' %file_node)
        cmds.connectAttr('%s.offset' %place_2d_texture_node, '%s.offset' %file_node)
        cmds.connectAttr('%s.rotateUV' %place_2d_texture_node, '%s.rotateUV' %file_node)
        cmds.connectAttr('%s.noiseUV' %place_2d_texture_node, '%s.noiseUV' %file_node)
        cmds.connectAttr('%s.vertexUvOne' %place_2d_texture_node, '%s.vertexUvOne' %file_node)
        cmds.connectAttr('%s.vertexUvTwo' %place_2d_texture_node, '%s.vertexUvTwo' %file_node)
        cmds.connectAttr('%s.vertexUvThree' %place_2d_texture_node, '%s.vertexUvThree' %file_node)
        cmds.connectAttr('%s.vertexCameraOne' %place_2d_texture_node, '%s.vertexCameraOne' %file_node)
        cmds.connectAttr('%s.outUV' %place_2d_texture_node, '%s.uv' %file_node)
        cmds.connectAttr('%s.outUvFilterSize' %place_2d_texture_node, '%s.uvFilterSize' %file_node)
        
        
    #function to allow user to select diffuse map
    def selectDiffuseMap(self, diffuse_file_node):
        # Select diffuse map
        diffuse_map_import = cmds.fileDialog2(fileMode=1, caption="Import Diffuse Map")
        # If the user clicks the cancel button on the window, simply delete all nodes created so far and stop the script running
        if not diffuse_map_import:
            cmds.delete(self.shader, self.shading_group, self.material_name+"_Diffuse_File", self.material_name+"_2dtexture")
            sys.exit()
        else: 
            pass
        # Convert the file name into a string and edit it so the location will be relative to the projects source images folder
        # Creates variable of project directory
        projectVar = cmds.workspace(q=True, rd=True)
        if str(projectVar) in str(diffuse_map_import):
            print "Material is relative"
            diffuse_map = diffuse_map_import[0].replace(str(projectVar), '')
        else:
            print "Material is not relative"
            self.confirm = cmds.confirmDialog(title='Confirm Absolute Paths', 
            message="The file you've selected is not in your project directory." 
            + '\n' + "File Paths created will not be relative."
            + '\n' + "Do you wish to continue?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')
            if self.confirm == "Yes":
                diffuse_map = diffuse_map_import[0]
            else:
                cmds.delete(self.shader, self.shading_group, self.material_name+"_Diffuse_File", self.material_name+"_2dtexture")
                sys.exit()
        # connect diffuse map to diffuse texture node
        cmds.setAttr('%s.fileTextureName' %diffuse_file_node, diffuse_map , type='string')
        # connect file texture node to shader's color
        # Arnold Version
        if self.renderer == "Arnold":
            cmds.connectAttr('%s.outColor' %diffuse_file_node, '%s.baseColor' %self.shader)
            # Set the base colour of the shader to 1
            cmds.setAttr('%s.base' %self.shader, 1)
        # Redshift Version
        elif self.renderer == "Redshift":
            cmds.connectAttr('%s.outColor' %diffuse_file_node, '%s.diffuse_color' %self.shader)
        # If UDIM checkbox has been ticked than set the file node to read the diffuse map as UDIM
        if self.UDIMcheck:
            cmds.setAttr('%s.uvTilingMode' %diffuse_file_node, 3)
        else:
            pass
        # Search for the directory that is the folder used for this texture
        texture_folder_location=os.path.dirname(diffuse_map_import[0])
        texture_folder=os.path.dirname(texture_folder_location) + "/" + os.path.basename(texture_folder_location)
        # Make the variable accessable for other functions across class
        self.diffuse_file = diffuse_map
        self.texture_folder = texture_folder

    #function to get the maps depending on map type and file type
    def getMaps(self, type, fileType):
        #get the list of files with the file type in the texture folder
        map_list = filter(lambda fname: fileType in fname, os.listdir(self.texture_folder))
        x = False
        #sets the node to be correct node for the map type
        node = self.material_name+"_"+type+"_File"
        #Will check if maps were found with file type
        if not map_list:
            print "No files with " + fileType + " extension found."
        #Will check if maps were found for correct map type 
        else:
            #Map type with Capital first letter then lowercase
            map_import = filter(lambda fname: type in fname, map_list)
            if not map_import:
                #Map type with all lowercase
                map_import = filter(lambda fname: type.lower() in fname, map_list)
                if not map_import:
                    #Map type with all uppercase
                    map_import = filter(lambda fname: type.upper() in fname, map_list)
                    if not map_import:
                        #If no maps are found then print error
                        print "No " + type + " file found."
                    else:
                        x = True
                else: 
                    x = True
            else:
                x = True
        #If map is found, will be connected to the file node
        if x == True:
            if len(map_import) > 1:
                match_map = difflib.get_close_matches(self.diffuse_file, map_import, n=1,cutoff=0.1)
                del map_import[:]
                map_import.append(match_map[0])
            else:
                pass
            tf = self.texture_folder
            projectVar = cmds.workspace(q=True, rd=True)
            file_map = tf.replace(str(projectVar), '') + '/' + map_import[0]
            node = self.material_name+"_"+type+"_File"
            cmds.setAttr('%s.fileTextureName' %node, file_map , type='string')
            #If UDIM checkbox has been ticked than set the file node to read the diffuse map as UDIM
            if self.UDIMcheck:
                cmds.setAttr('%s.uvTilingMode' %node, 3)
                #print "Has UDIMs"
            else:
                pass
        else:
            pass
        #Sets colour space and alpha is luminance settings
        cmds.setAttr('%s.colorSpace' %node, 'Raw', type='string')
        cmds.setAttr('%s.alphaIsLuminance' %node, True)

    def connectSpec(self): 
        file_node = self.material_name+"_Spec_File"
        # Arnold Version
        if self.renderer == "Arnold":
            cmds.connectAttr('%s.outColor' %file_node, '%s.specularColor' %self.shader)
        # Redshift Version
        elif self.renderer == "Redshift":
            cmds.connectAttr('%s.outColor' %file_node, '%s.refl_color' %self.shader)
    def connectMetalness(self): 
        file_node = self.material_name+"_Metal_File"
        # Arnold Version
        if self.renderer == "Arnold":
            cmds.connectAttr('%s.outAlpha' %file_node, '%s.metalness' %self.shader)
        # Redshift Version
        elif self.renderer == "Redshift":
            cmds.setAttr('%s.refl_brdf' %self.shader, 1)
            cmds.setAttr('%s.refl_fresnel_mode' %self.shader, 2)
            cmds.connectAttr('%s.outAlpha' %file_node, '%s.refl_metalness' %self.shader)
    def connectRough(self): 
        file_node = self.material_name+"_Rough_File"
        # Arnold Version
        if self.renderer == "Arnold":
            cmds.connectAttr('%s.outAlpha' %file_node, '%s.specularRoughness' %self.shader)
        # Redshift Version
        elif self.renderer == "Redshift":
            cmds.connectAttr('%s.outAlpha' %file_node, '%s.refl_roughness' %self.shader)
    def connectBump(self): 
        file_node = self.material_name+"_Bump_File"
        bump_node = cmds.shadingNode("bump2d",asUtility=True, name=self.material_name+"_Bump2d_Node")
        cmds.connectAttr('%s.outAlpha' %file_node, '%s.bumpValue' %bump_node)
        # Arnold Version
        if self.renderer == "Arnold":    
            cmds.connectAttr('%s.outNormal' %bump_node, '%s.normalCamera' %self.shader)
        # Redshift Version
        elif self.renderer == "Redshift":
            cmds.connectAttr('%s.outNormal' %bump_node, '%s.bump_input' %self.shader)
    def connectNormal(self): 
        file_node = self.material_name+"_Nor_File"
        bump_node = cmds.shadingNode("bump2d",asUtility=True, name=self.material_name+"_Bump2d_Node")
        cmds.connectAttr('%s.outAlpha' %file_node, '%s.bumpValue' %bump_node)
        # Arnold Version
        if self.renderer == "Arnold":
            cmds.connectAttr('%s.outNormal' %bump_node, '%s.normalCamera' %self.shader)
            cmds.setAttr('%s.aiFlipR' %bump_node, False)
        # Redshift Version
        elif self.renderer == "Redshift":
            cmds.connectAttr('%s.outNormal' %bump_node, '%s.bump_input' %self.shader)
        cmds.setAttr('%s.bumpInterp' %bump_node, 1)
        cmds.setAttr('%s.alphaIsLuminance' %file_node, False)
        cmds.rename(file_node, self.material_name+"_Normal_File")

    def connectDisplacement(self):
        file_node = self.material_name+"_Disp_File"
        disp_node = cmds.shadingNode("displacementShader", asShader=True, name=self.material_name+"_Displacement_Node")
        cmds.connectAttr('%s.outAlpha' %file_node, '%s.displacement' %disp_node)
        cmds.connectAttr('%s.displacement' %disp_node, '%s.displacementShader' %self.shading_group)
        cmds.rename(file_node, self.material_name+"_Displacement_File")

    def connectHeight(self):
        file_node = self.material_name+"_Height_File"
        disp_node = cmds.shadingNode("displacementShader", asShader=True, name=self.material_name+"_Displacement_Node")
        cmds.connectAttr('%s.outAlpha' %file_node, '%s.displacement' %disp_node)
        cmds.connectAttr('%s.displacement' %disp_node, '%s.displacementShader' %self.shading_group)
        cmds.setAttr('%s.alphaOffset' %file_node, -0.5)
        cmds.rename(file_node, self.material_name+"_Height_File")

    def connectAO(self):
        file_node = self.material_name+"_AO_File"
        diffuse_node = self.material_name+"_Diffuse_File"
        # Arnold Version
        if self.renderer == "Arnold":
            cc_node = cmds.shadingNode("aiColorCorrect", asShader=True, name=self.material_name+"_AO_CC_Node")
            cmds.connectAttr('%s.outColor' %file_node, '%s.input' %cc_node)
            multiply_node = cmds.shadingNode("aiMultiply", asShader=True, name=self.material_name+"_AO_Multiply_Node")
            cmds.connectAttr('%s.outColor' %cc_node, '%s.input1' %multiply_node)
            cmds.connectAttr('%s.outColor' %diffuse_node, '%s.input2' %multiply_node)
            cmds.disconnectAttr('%s.outColor' %diffuse_node, '%s.baseColor' %self.shader)
            cmds.connectAttr('%s.outColor' %multiply_node, '%s.baseColor' %self.shader)
        # Redshift Version
        elif self.renderer == "Redshift":
            cc_node = cmds.shadingNode("RedshiftColorCorrection", asTexture=True, name=self.material_name+"_AO_CC_Node")
            cmds.connectAttr('%s.outColor' %file_node, '%s.input' %cc_node)
            multiply_node = cmds.shadingNode("RedshiftColorLayer", asTexture=True, name=self.material_name+"_AO_Multiply_Node")
            cmds.connectAttr('%s.outColor' %cc_node, '%s.layer1_color' %multiply_node)
            cmds.connectAttr('%s.outColor' %diffuse_node, '%s.base_color' %multiply_node)
            cmds.setAttr('%s.layer1_blend_mode' %multiply_node, 4)
            cmds.disconnectAttr('%s.outColor' %diffuse_node, '%s.diffuse_color' %self.shader)
            cmds.connectAttr('%s.outColor' %multiply_node, '%s.diffuse_color' %self.shader)

    def connectOpacity(self): 
        file_node = self.material_name+"_Opacity_File"
        # Arnold Version
        if self.renderer == "Arnold":
            cmds.connectAttr('%s.outColor' %file_node, '%s.opacity' %self.shader)
            cmds.setAttr('%s.thinWalled' %self.shader, True)
        # Redshift Version
        elif self.renderer == "Redshift":
            cmds.connectAttr('%s.outColor' %file_node, '%s.opacity_color' %self.shader)