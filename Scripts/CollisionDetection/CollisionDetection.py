#Author-An Pirlot
#Description-Runs a number of simulations automatically 

from adsk import core
from adsk.fusion import Component, Design, BRepBody, Occurrences, DesignTypes, InterferenceResult
import traceback
import csv
import os
from typing import List


def run(context):
    try:
        # Fusion data
        global app, ui
        app = core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = Design.cast(product)

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
        logInterferenceData(filepath, results)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def logInterferenceData(filepath, interferenceResults):  # type: (str, List[InterferenceResult]) -> None
    '''
    Writes the results of an interferencesimulation to a specified csv file
    '''
    writeToFile(filepath, ['TEST', 'STATUS', 'RESULT'])

    if not len(interferenceResults):
        writeToFile(filepath, ['Interference', 'OK', 'no interference'])
    else:
        rowResult = 'interference between:'
        for result in interferenceResults:
            entity1 = BRepBody.cast(result.entityOne)
            entity2 = BRepBody.cast(result.entityTwo)
            entities = '({component1}.{body1}, {component2}.{body2})'.format(component1=entity1.parentComponent.name, body1=entity1.name, component2=entity2.parentComponent.name, body2=entity2.name)
            rowResult = ' '.join([rowResult, entities])
        writeToFile(filepath, ['Interference', 'NOK', rowResult])


def checkAssemblyForInterference(rootComponent):  # type: (Component) -> List[InterferenceResult]
    """
    checks all bodies, incl bodies from subassemblies, for interference
    Return a list of interferenceResult objects, 
    if there is no interference detected, an empty list is returned
    """
    design = rootComponent.parentDesign
    design.designType = DesignTypes.DirectDesignType
    bodies = getAllBodiesFromAssembly(rootComponent)

    inputBodies = core.ObjectCollection.create()
    for body in bodies:
        inputBodies.add(body)

    results = []
    if len(bodies) > 1:
        interferenceInput = design.createInterferenceInput(inputBodies)
        interferenceResults = design.analyzeInterference(interferenceInput)
        for j in range(interferenceResults.count):
            results.append(interferenceResults.item(j))

    # Undo 'Do not capture design history' to get the design history back
    ui.commandDefinitions.itemById('UndoCommand').execute()
    return results


def getAllBodiesFromAssembly(rootComponent):  # type: (Component) -> List[BRepBody]
    """
    Return a list of all the bodies in an assembly,
    including bodies from subassemblies,
    starting from its rootcomponent
    """
    bodies = []
    bodies.extend(rootComponent.bRepBodies)
    bodies += __getAllBodiesFromOccurences(rootComponent.occurrences)
    return bodies


def __getAllBodiesFromOccurences(occurences):  # type: (Occurrences) -> List[BRepBody]
    """
    returns a list of all the bodies in an occurences object,
    including all bodies from child occurences
    """
    bodies = []
    for j in range(occurences.count):
        occurence = occurences.item(j)
        bodies.extend(occurence.bRepBodies)
        if occurence.childOccurrences:
            bodies += __getAllBodiesFromOccurences(occurence.childOccurrences)
    return bodies


def writeToFile(filepath, row):  # type: (str, List[str]) -> None
    with open(filepath, 'a') as resultFile:
        resultWriter = csv.writer(resultFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        resultWriter.writerow(row)
