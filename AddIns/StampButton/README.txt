HOW TO:

1.
-Copy the entire StampButton folder into your Fusion 360 addin folder, inlc .py, manifest and resources folder.
-Restart Fusion 360
-This should add the stamp button in the tools toolbar under the add-ins tab

2.
-Copy the entire UpdateTextSketchesOnSave folder into your Fusion 360 addin folder.
-Copy the entire UpdateVersionTextOnSave folder into your Fusion 360 addin folder.
-Mare sure both addins are running before saving, this should automatically update all stamps created with the stampbutton addin

USAGE:

1. The update addins update every sketch with name "Version Number" to the current Version Number and every sketch with name = one of the user parameters to the current value of the corresponding user parameter
2. The stamp button lets the user create such a sketch with the correct naming and extrudes it to create a stamp


POSSIBLE CHANGES:

Currently the user is provided with a dropdown list of all user parameters in the design plus a version number. You can find the corresponding code in the StampCommandCreatedHandler class under "#Dropdown of parameters". This can be changed to provide other parameters, some hardcoded parameters or another type of input like textInput from the user. The stamp is updated in the StampCommandexecuteHandler class' notify method via the "selectedParameter"-id 
like this:
  stamp = inputs.itemById("selectedParameter").selectedItem.name

FUTURE

The UpdateTextSketchesOnSave and UpdateVersionTextOnSave could maybe best be refactored into 1 addin maybe even including the stamp addin