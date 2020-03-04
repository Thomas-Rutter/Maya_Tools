from maya import cmds

from model_qc_renderer import core


class Model_QC_Renderer_UI(object):

    def __init__(self):
        name = "Model_QC_Renderer"
        self.name = name
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name, window=True)
            cmds.windowPref(name, remove=True)
        self.create_UI()

    def create_UI(self):
        window_name = cmds.window(self.name)
        cmds.window(window_name, edit=True)#, resizeToFitChildren=True)
        label_colour = (0.450, 0.541, 0.858)
        column = cmds.columnLayout('qc_columns', adjustableColumn=True)
        cmds.setParent(column)
        cmds.frameLayout(label="Select passes", backgroundColor=label_colour)
        self.ao_checkbox = cmds.checkBox(label="AO Pass", value=True)
        self.wireframe_checkbox = cmds.checkBox(
            label="Wireframe Pass",
            value=True
        )
        cmds.setParent(column)
        cmds.button(
            label='Create',
            command=self.create_passes,
            bgc=(1, 1, 1)
        )
        cmds.showWindow()

    def create_passes(self, *args):
        core.main()
