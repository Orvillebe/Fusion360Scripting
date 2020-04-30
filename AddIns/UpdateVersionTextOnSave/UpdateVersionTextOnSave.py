#Description-Update any text on sketches named "Version Number" with the latest document version and part number.

import adsk.core, adsk.fusion, adsk.cam, traceback, datetime

ui = None
handlers = []

def updateComponent(component, version):

    for sketch in component.sketches:
        # Test if the name of the sketch starts with 'Version Number', there could be multiple Version Number (1/2/...) sketches
        if sketch.name.startswith('Version Number'):
            for text in sketch.sketchTexts:
                currentPartnumber = ''
                # If the component does not have a partNumber yet (e.g. file has never been saved and component is root component) only text to version number only
                # Else update text to version number + part number
                if component.partNumber != '(Unsaved)':
                    currentPartnumber = component.partNumber
                text.text = ("%s/%s V%s %s" % (datetime.date.today().day, datetime.date.today().month, version, currentPartnumber))


class MyDocumentSavingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # Uncomment following for ui message saying the script is busy updating the version number texts
            #ui.messageBox('Applying version')

            eventArgs = adsk.core.DocumentEventArgs.cast(args)

            if eventArgs.document.classType() != adsk.fusion.FusionDocument.classType(): 
                ui.messageBox('Not a fusion document')
                return

            doc = adsk.fusion.FusionDocument.cast(eventArgs.document)

            design = doc.design
            # Check if the file has been saved before
            # If not the version number should be 1
            hasBeenSaved = design.parentDocument.isSaved
            version = 1
            if hasBeenSaved != False:
               version = design.parentDocument.dataFile.versionNumber+1

            for component in design.allComponents:
                updateComponent(component, version)
                
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
