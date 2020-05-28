#Author-An Pirlot
#Description-Update text in sketches according to a parameter with the same name. Example: the text in a sketch with name "Height" will be updated to "Height:Value" with the value from user parameter with name "Height".\t\t\t

import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import datetime

ui = None
handlers = []

def updateTextSketchesInComponent(component):
    for sketch in component.sketches:
        # Check if there is a user parameter with the same name
        design = component.parentDesign
        unitsManager = design.unitsManager
        userParameters = design.userParameters
        parameter = userParameters.itemByName(sketch.name)
        # If there is replace the text in the sketch by the name and value of the parameter
        if parameter is not None:
            value = parameter.value
            for text in sketch.sketchTexts:
                text.text = ("%s:%s%s" % (parameter.name, unitsManager.convert(parameter.value, unitsManager.internalUnits, parameter.unit), parameter.unit))



class MyDocumentSavingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Uncomment following for ui message saying the script is busy updating the sketch texts
            #ui.messageBox('Updating texts in sketches')

            eventArgs = adsk.core.DocumentEventArgs.cast(args)
            doc = adsk.fusion.FusionDocument.cast(eventArgs.document)

            design = doc.design

            if eventArgs.document.classType() != adsk.fusion.FusionDocument.classType(): 
                ui.messageBox('Not a fusion document')
                return

            for component in design.allComponents:
                updateTextSketchesInComponent(component)
                
        except Exception as e:
            message = 'Failed:\n{}'.format(traceback.format_exc())

            if ui:
                ui.messageBox(message)



def run(context):
    try:
        app = adsk.core.Application.get()
        global ui
        ui  = app.userInterface

        onDocumentSaving = MyDocumentSavingHandler()
        app.documentSaving.add(onDocumentSaving)
        handlers.append(onDocumentSaving)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        app = adsk.core.Application.get()
        for handler in handlers:
            app.documentSaving.remove(handler)

        handler.clear()
        ui = None

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
