#Author-An Pirlot
#Description-Automatically run collision detection for multiple positions 

import adsk.core, adsk.fusion, adsk.cam, traceback, csv, os, sys

def run(context):
    try:
        # Fusion data
        global app, ui
        app = adsk.core.Application.get()
        ui  = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        if not design:
            ui.messageBox('This is not supported in the current workspace, please change to Design and try again.')
            return

        # Data protection
        document = design.parentDocument
        if not document.isSaved:
            ui.messageBox('This is not supported for unsaved documents, please save and try again.')
            return
        if document.isModified:
            document.save('Auto save because of RunSimulations.py')
        
        # Logging data
        home_folder = os.path.expanduser('~')
        filepath = os.path.join(home_folder, "Desktop", "CollisionDetection.csv")
        
        rootComp = design.rootComponent
        results = checkAssemblyForInterference(rootComp)
        logInterferenceData(filepath,results)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def logInterferenceData(filepath, interferenceResults: list):
    '''
    Writes the results of an interferencesimulation to a specified csv file
    '''
    writeToFile(filepath, ['TEST', 'STATUS', 'RESULT'])

    if len(interferenceResults) == 0:
        writeToFile(filepath,['Interference', 'OK', 'no interference'])
    else:
        rowResult = 'interference between:'
        for result in interferenceResults:
            entity1 = adsk.fusion.BRepBody.cast(result.entityOne)
            entity2 = adsk.fusion.BRepBody.cast(result.entityTwo)
            entities = '({component1}.{body1}, {component2}.{body2})'.format(component1=entity1.parentComponent.name, body1=entity1.name, component2=entity2.parentComponent.name, body2=entity2.name)
            rowResult = ' '.join([rowResult,entities])
        writeToFile(filepath, ['Interference', 'NOK', rowResult])


def checkAssemblyForInterference(rootComponent: adsk.fusion.Component):
    """
    checks all bodies, incl bodies from subassemblies, for interference
    Return a list of interferenceResult objects, 
    if there is no interference detected, an empty list is returned
    """
    design = rootComponent.parentDesign
    design.designType = adsk.fusion.DesignTypes.DirectDesignType
    bodies = getAllBodiesFromAssembly(rootComponent)

    inputBodies = adsk.core.ObjectCollection.create()
    for body in bodies:
        inputBodies.add(body)

    results = []
    if len(bodies) > 1:
        interferenceInput = design.createInterferenceInput(inputBodies)
        interferenceResults = design.analyzeInterference(interferenceInput)
        for j in range (0, interferenceResults.count):
            results.append(interferenceResults.item(j))

    # Undo 'Do not capture design history' to get the design history back
    cmd = ui.commandDefinitions.itemById('UndoCommand').execute()
    return results


def getAllBodiesFromAssembly(rootComponent: adsk.fusion.Component):
    """
    Return a list of all the bodies in an assembly,
    including bodies from subassemblies,
    starting from its rootcomponent
    """
    bodies = []
    bodies.extend(rootComponent.bRepBodies)
    return __getAllBodiesFromOccurences(rootComponent.occurrences, bodies)


def __getAllBodiesFromOccurences(occurences: adsk.fusion.Occurrences, bodies: list):
    """
    returns a list of all the bodies in an occurences object, 
    including all bodies from child occurences
    """
    for j in range(0,occurences.count):
        occurence = occurences.item(j)
        bodies.extend(occurence.bRepBodies)
        if occurence.childOccurrences:
            __getAllBodiesFromOccurences(occurence.childOccurrences, bodies)
    return bodies


def writeToFile(filepath: str, row: list):
    with open (filepath, 'a') as resultFile:
        resultWriter = csv.writer(resultFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        resultWriter.writerow(row)
