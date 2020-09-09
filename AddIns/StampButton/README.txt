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


FUTURE

-The UpdateTextSketchesOnSave and UpdateVersionTextOnSave could maybe best be refactored into 1 addin maybe even including the stamp addin
