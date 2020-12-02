#Author-An Pirlot
#Description-addin that adds a button/function to the toolbar that allows the user to stamp 'Version Number' into a face, which serves as input for https://github.com/Orvillebe/Fusion360Scripting/tree/master/AddIns/UpdateVersionTextOnSave
import os
import sys

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
            design = adsk.fusion.Design.cast(app.activeProduct)
            if not design:
                ui.messageBox('This is not supported in the current workspace, please change to Design and try again.')
                return

            onExecute = StampCommandexecuteHandler()
            command.execute.add(onExecute)
            _handlers.append(onExecute)

            #Selection of face
            selectionInput = inputs.addSelectionInput("selectedFace", "Face", "Select an planar face")
            selectionInput.setSelectionLimits(1,1)
            selectionInput.addSelectionFilter("PlanarFaces")

            #Select size and depth
            DepthValueInput = inputs.addValueInput("stampDepth", "stampDepth", "mm", adsk.core.ValueInput.createByReal(0.04))
            HeightValueInput = inputs.addValueInput("stampHeight", "stampHeight", "mm", adsk.core.ValueInput.createByReal(0.6))
            
            #Dropdown of parameters
            dropDownInput = inputs.addDropDownCommandInput("selectedParameter", "Parameter", adsk.core.DropDownStyles.TextListDropDownStyle)
            dropDownItems = dropDownInput.listItems
            dropDownItems.add("Version Number", True)
            for parameter in design.userParameters:
                dropDownItems.add(parameter.name, False)

                
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
            design = adsk.fusion.Design.cast(app.activeProduct)
            unitsManager = design.unitsManager

            command = args.command
            inputs = command.commandInputs

            #load parameters provided by user via userinput
            selectedFace = inputs.itemById("selectedFace").selection(0).entity
            stamp = inputs.itemById("selectedParameter").selectedItem.name
            stampDepth = unitsManager.evaluateExpression(inputs.itemById("stampDepth").expression)
            stampHeight = unitsManager.evaluateExpression(inputs.itemById("stampHeight").expression)
            #do the actual stamp
            self.stampOnPlanarFace(selectedFace, stamp, stampDepth, stampHeight)

                
        except Exception as e:
            message = 'Failed:\n{}'.format(traceback.format_exc())

            if ui:
                ui.messageBox(message)

    def writeOnPlanarFace(self, planarFace, textToWrite, stampHeight):
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
        stampText.height = stampHeight
        #rename sketch to have the same name as the text (for updating)
        stampSketch.name = textToWrite

        return stampText


    def stampOnPlanarFace(self, selectedFace, stamp, stampDepth, stampHeight):
        '''
        when given a string will stamp that string 0.04 mm deep into a by the user selected planar face.
        '''

        #create sketch and text to stamp
        stamp = self.writeOnPlanarFace(selectedFace, stamp, stampHeight)

        #stamp the text
        extrudes = stamp.parentSketch.parentComponent.features.extrudeFeatures
        extrudeInput = extrudes.createInput(stamp, adsk.fusion.FeatureOperations.CutFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(-stampDepth)
        extrudeInput.setDistanceExtent(False, distance)
        extrudes.add(extrudeInput)
        

def createStampCommandButton():
    '''
    Adds a button with linked command to the add-ins toolbar to trigger a stamp into a face. This will stamp a parameter of choice into a chosen face. This can also be used to stamp the version.
    '''
    app = adsk.core.Application.get()
    ui  = app.userInterface
    
    #create button and command
    script_directory = os.path.dirname(__file__)
    stampButtonDefinition =  ui.commandDefinitions.addButtonDefinition('stampButton', 'stamp', 'This will stamp a parameter of choice into a chosen face. This can also be used to stamp the version.', script_directory+'/resources')
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
