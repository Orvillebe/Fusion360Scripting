#Author-An Pirlot
#Description-Update text in sketches according to the name of the sketch and the corresponding user parameter with the same name. 
#Example: a sketch with name "Height" will look for a user parameter with name "Height" and update any text in this sketch to "Height:value"

import adsk
import traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct

        for component in design.allComponents:
            updateTextSketchesInComponent(component)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def updateTextSketchesInComponent(component):
    for sketch in component.sketches:
        # Check if there is a user parameter with the same name
        design =component.parentDesign
        unitsManager = design.unitsManager
        userParameters = design.userParameters
        parameter = userParameters.itemByName(sketch.name)
        # If there is replace the text in the sketch by the name and value of the parameter
        if parameter is not None:
            for text in sketch.sketchTexts:
                text.text = ("%s:%s%s" % (parameter.name, unitsManager.convert(parameter.value, unitsManager.internalUnits, parameter.unit), parameter.unit))
