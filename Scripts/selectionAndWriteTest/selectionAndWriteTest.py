#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox("Please select a face")
        selectedFace = ui.selectEntity("Select face", "Faces").entity
        ui.messageBox("You selected a face with area {face} cm^2".format(face = selectedFace.area) )
        parentComponent = selectedFace.body.parentComponent 
        ui.messageBox("you selected a face of component {component}".format(component = parentComponent.name))
        stampSketch = parentComponent.sketches.add(selectedFace)
        point = stampSketch.modelToSketchSpace(selectedFace.pointOnFace)
        text = stampSketch.sketchTexts.createInput("test", 1.0, point )
        stampSketch.sketchTexts.add(text)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
