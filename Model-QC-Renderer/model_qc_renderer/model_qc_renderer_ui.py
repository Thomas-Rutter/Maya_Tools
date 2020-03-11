from maya import cmds

from model_qc_renderer import core


class ModelQCRendererUI(object):
    """UI Class for model qc renderer."""
    def __init__(self):
        name = "Model_QC_Renderer"
        self.name = name
        if cmds.window(name, query=True, exists=True):
            cmds.deleteUI(name, window=True)
            cmds.windowPref(name, remove=True)
        self.create_ui()

    def create_ui(self):
        """Create the UI."""
        window_name = cmds.window(self.name)
        cmds.window(window_name, edit=True, resizeToFitChildren=True)
        label_colour = (0.450, 0.541, 0.858)
        column = cmds.columnLayout('qc_columns', adjustableColumn=True)
        cmds.setParent(column)
        cmds.frameLayout(
            label="Instructions:",
            backgroundColor=label_colour,
            width=100
        )
        instructions = (
            "Select the model.\n"
            "A 360 turntable render will be set up.\n"
            "Wireframe and AO render passes will be created."
        )
        cmds.text(label=instructions, align="left")
        cmds.button(
            label='Create',
            command=self.create_passes,
            bgc=(1, 1, 1)
        )
        cmds.showWindow()

    def create_passes(self, *args):
        """Create the render passes.

        Arguments:
            *args -- Catch the args passed from the button.
        """
        core.main()
