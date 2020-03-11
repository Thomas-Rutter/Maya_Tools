from maya import cmds
from maya.app import renderSetup


def set_timerange():
    """Set the frame range to 1001-1360."""
    cmds.playbackOptions(
        animationStartTime=1001,
        animationEndTime=1360,
        minTime=1001,
        maxTime=1360
    )


def set_rotation(model):
    """Set the rotation keyframes of the model.

    Arguments:
        model(unicode): The model to rotate.
    """
    cmds.setKeyframe(
        model,
        time=1001,
        value=0,
        attribute="rotateY"
    )
    cmds.setKeyframe(
        model,
        time=1360,
        value=360,
        attribute="rotateY"
    )


def create_camera(model):
    """Create the camera to focus on the mode.

    Arguments:
        model(unicode): Model to fit in view.
    """
    qc_camera = cmds.camera(name="QC_Camera")
    qc_camera_shape = qc_camera[1]
    cmds.select(model)
    cmds.viewFit(qc_camera_shape, fitFactor=0.8)
    return qc_camera[0]


def create_render_layers(model, camera):
    """Create the render layers.

    Arguments:
        model(unicode): Model to render.
        camera(unicode): Camera to render.
    """
    renderSetup.model.renderSetup.initialize()
    render_setup = renderSetup.model.renderSetup.instance()
    passes = ["Wireframe", "AmbientOcclusion"]
    for render_pass in passes:
        layer = render_setup.createRenderLayer(render_pass)
        collection = layer.createCollection(
            "{}_Collection".format(render_pass)
        )
        collection.getSelector().staticSelection.add([model])
        collection.getSelector().staticSelection.add([camera])
        shader = cmds.shadingNode(
            "ai{}".format(render_pass),
            asShader=True,
            name="{}_render".format(render_pass)
        )
        override = collection.createOverride(
            "{}_Override".format(render_pass),
            "shaderOverride"
        )
        override.setShader(shader)
    cmds.setAttr("Wireframe_render.edgeType", 1)


def set_render_settings(camera):
    """Set the render settings.

    Arguments:
        camera(unicode): QC Camera.
    """
    cmds.setAttr("{}.renderable".format(camera), True)
    cmds.setAttr("persp.renderable", False)
    cmds.setAttr("defaultRenderGlobals.startFrame", 1001)
    cmds.setAttr("defaultRenderGlobals.endFrame", 1360)
    cmds.setAttr("defaultRenderGlobals.outFormatControl", 0)
    cmds.setAttr("defaultRenderGlobals.animation", 1)
    cmds.setAttr("defaultResolution.width", 1280)
    cmds.setAttr("defaultResolution.height", 720)


def main():
    """Main function of script."""
    set_timerange()
    model = cmds.ls(selection=True)[0]
    set_rotation(model)
    camera = create_camera(model)
    qc_light = cmds.shadingNode(
        "aiSkyDomeLight",
        name=("QC_LightShape"),
        asLight=True
    )
    cmds.setAttr("{}.camera".format(qc_light), 0)
    cmds.select(model)
    create_render_layers(model, camera)
    set_render_settings(camera)
    cmds.currentTime(1001, edit=True)
