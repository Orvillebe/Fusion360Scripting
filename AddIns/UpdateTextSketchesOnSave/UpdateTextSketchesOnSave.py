# Author-An Pirlot Description-Update text in sketches according to a either the current version or a parameter with
# the same name.
# Example for a version number: The text in a sketch with name "Version Number" will be updated to
# "V6 DesignName ComponentName"
# Example for a parameter: the text in a sketch with name "Height" will be updated to "Height:Value" with
# the value from user parameter with name "Height".


import traceback

import adsk.cam
import adsk.core
import adsk.fusion

ui = None
handlers = []


def update_parameter_sketch(sketch: adsk.fusion.Sketch) -> None:
    design = sketch.parentComponent.parentDesign
    units_manager = design.unitsManager
    user_parameters = design.userParameters
    # Check if there is a user parameter with the same name
    # there could be multiple sketches with this name parameter (1/2/...)
    # a user parameter is not allowed to have spaces
    # so just cut off everything after " "
    parameter_name = sketch.name.split(" (", 1)[0]
    parameter = user_parameters.itemByName(parameter_name)
    # If there is replace the text in the sketch by the name and value of the parameter
    if parameter is not None:
        value = units_manager.convert(parameter.value, units_manager.internalUnits, parameter.unit)
        for text in sketch.sketchTexts:
            text.text = f"{parameter.name}:{value}{parameter.unit}"


def update_version_sketch(sketch: adsk.fusion.Sketch, version: int) -> None:
    for text in sketch.sketchTexts:
        component = sketch.parentComponent
        current_partNumber = ''
        current_parent_partNumber = ''
        # If the component does not have a partNumber yet , just don't update the partnumbers and keep them empty
        # Else update text to version number + part number
        if component.partNumber != "(Unsaved)":
            current_root = component.parentDesign.rootComponent
            current_parent_partNumber = component.parentDesign.rootComponent.partNumber
            # If the component is the current component is the root of it's own design you do not need to update the
            # current_partNumber it would just result in the same thing twice e.g. V12 Parent1 Parent1 instead of V12
            # Parent1 Component1
            if component.id != current_root.id:
                current_partNumber = component.partNumber
        if sketch.name == 'Version Number Only':
            text.text = f"V{version}"
        else:
            text.text = f"V{version} {current_parent_partNumber} \n{current_partNumber}"


def update_component(component: adsk.fusion.Component, version: int) -> None:
    for sketch in component.sketches:
        # Check if the name of the sketch starts with 'Version Number',
        # there could be multiple Version Number (1/2/...) sketches
        if sketch.name.startswith('Version Number'):
            update_version_sketch(sketch, version)
        else:
            # Check if there is a user parameter with the same name
            # and if so update accordingly
            update_parameter_sketch(sketch)


class MyDocumentSavingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            # Uncomment following for ui message saying the script is busy updating the sketch texts
            # ui.messageBox('Updating texts in sketches')

            event_args = adsk.core.DocumentEventArgs.cast(args)
            doc = adsk.fusion.FusionDocument.cast(event_args.document)

            design = doc.design

            if event_args.document.classType() != adsk.fusion.FusionDocument.classType():
                # not a fusion design document, don't need to update anything
                return

            version = 1
            if design.parentDocument.isSaved:
                version = design.parentDocument.dataFile.versionNumber + 1

            for component in design.allComponents:
                if component.parentDesign == design:
                    update_component(component, version)

        except Exception as e:
            message = "Failed:\n{}".format(traceback.format_exc())

            if ui:
                ui.messageBox(message)


def run(context):
    try:
        app = adsk.core.Application.get()
        global ui
        ui = app.userInterface

        on_document_saving = MyDocumentSavingHandler()
        app.documentSaving.add(on_document_saving)
        handlers.append(on_document_saving)

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


def stop(context):
    try:
        app = adsk.core.Application.get()
        for handler in handlers:
            app.documentSaving.remove(handler)

        handler.clear()
        ui = None

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
