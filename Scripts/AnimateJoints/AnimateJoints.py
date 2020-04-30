#Author- Orville
#Description- Animating joints

from adsk import core
from adsk.fusion import * 
import traceback
import csv
import os
from typing import List

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        product = app.activeProduct
        design = Design.cast(product)
        if not design:
            ui.messageBox('This is not supported in the current workspace, please change to Design and try again.')
            return

        # Logging data
        home_folder = os.path.expanduser('~')
        filepath = os.path.join(home_folder, "Desktop", "AnimateJoints.csv")
        
        rootComp = design.rootComponent
        joints = getAlljointsInAssembly(rootComp)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            
def getAlljointsInAssembly(rootComponent): #type: (Component) -> List[Str]
    '''
    Gets all components (these are occurences), incl child components, for an assembly from the rootComponent
    '''
    joints = []
    for joint in rootComponent.allJoints:
        joints.append(joint.name)
    return rootComponent.allJoints


def writeToFile(filepath, row):  # type: (str, List[str]) -> None
    with open(filepath, 'a') as resultFile:
        resultWriter = csv.writer(resultFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        resultWriter.writerow(row)
    