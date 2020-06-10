#Author-An Pirlot
#Description-addin that adds a button/function to the toolbar that allows the user to stamp 'Version Number' into a face, which serves as input for https://github.com/Orvillebe/Fusion360Scripting/tree/master/AddIns/UpdateVersionTextOnSave

import adsk.core, adsk.fusion, traceback

_handlers = []

class StampCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()


    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface
            command = args.command
            inputs = command.commandInputs

            onExecute = StampCommandexecuteHandler()
            command.execute.add(onExecute)
            _handlers.append(onExecute)

            selectionInput = inputs.addSelectionInput("selectedFace", "Select where to stamp", "Select an planar face")
            selectionInput.setSelectionLimits(1,1)
            selectionInput.addSelectionFilter("PlanarFaces")
            stamp = 'Version Number'

                
        except Exception as e:
            message = 'Failed:\n{}'.format(traceback.format_exc())

            if ui:
                ui.messageBox(message)

class StampCommandexecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()


    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface

            command = args.command
            inputs = command.commandInputs

            selectedFace = inputs.itemById("selectedFace").selection(0).entity
            stamp = 'Version Number'
            self.stampOnPlanarFace(selectedFace, stamp)

                
        except Exception as e:
            message = 'Failed:\n{}'.format(traceback.format_exc())

            if ui:
                ui.messageBox(message)

    def writeOnPlanarFace(self, planarFace, textToWrite):
        '''
        when given a planar face and a string, creates a sketch into the parentcomponent of the face with name and 
        text inside the sketch the same as the string provided.
        return the sketchtext that was created.
        '''
        #create sketch on face in component
        parentComponent = planarFace.body.parentComponent
        stampSketch = parentComponent.sketches.add(planarFace)
        point = stampSketch.modelToSketchSpace(planarFace.pointOnFace)
        stampText = stampSketch.sketchTexts.add(stampSketch.sketchTexts.createInput(textToWrite, 1.0, point ))
        stampText.height = 0.6
        #rename sketch to have the same name as the text (for updating)
        stampSketch.name = textToWrite

        return stampText


    def stampOnPlanarFace(self, selectedFace, stamp):
        '''
        when given a string will stamp that string 0.04 mm deep into a by the user selected planar face.
        '''
        #app = adsk.core.Application.get()
        #ui  = app.userInterface

        #select face of a component
        #selectedFace = ui.selectEntity("Select face", "PlanarFaces").entity

        #create sketch and text to stamp
        stamp = self.writeOnPlanarFace(selectedFace, stamp)

        #stamp the text
        extrudes = stamp.parentSketch.parentComponent.features.extrudeFeatures
        extrudeInput = extrudes.createInput(stamp, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(-0.04)
        extrudeInput.setDistanceExtent(False, distance)
        extrudes.add(extrudeInput)
        

def createStampCommandButton():
    '''
    Adds a button with linked command to the add-ins toolbar to trigger a stamp into a face. This will stamp a parameter of choice into a chosen face. This can also be used to stamp the version.
    '''
    app = adsk.core.Application.get()
    ui  = app.userInterface
    
    #create button and command
    stampButtonDefinition =  ui.commandDefinitions.addButtonDefinition('stampButton', 'stamp', 'This will stamp a parameter of choice into a chosen face. This can also be used to stamp the version.', 'resources')
    addInsToolbarPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
    stampButtonControl = addInsToolbarPanel.controls.addCommand(stampButtonDefinition, 'stampButtonControl')
    stampButtonControl.isPromotedByDefault = True
    stampButtonControl.isPromoted = True

    return stampButtonDefinition

def connectStampCommandButton(stampButtonDefinition):
    '''
    Connects the stamp button to the logic that needs to be execute.
    '''
    onCreate = StampCommandCreatedHandler()
    stampButtonDefinition.commandCreated.add(onCreate)
    _handlers.append(onCreate)


def run(context):

    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        stampButtonDefinition = ui.commandDefinitions.itemById('stampButton')
        if not stampButtonDefinition:
            stampButtonDefinition = createStampCommandButton()
        connectStampCommandButton(stampButtonDefinition)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        #clean up UI
        command = ui.commandDefinitions.itemById('stampButton')
        if command is not None:
            command.deleteMe()
        addinsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        control = addinsPanel.controls.itemById('stampButton')
        if control is not None:
            control.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
