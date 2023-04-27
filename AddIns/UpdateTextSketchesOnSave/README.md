# About

This is a support Add-in for maintaining parameter referencing text layers.

## Installing

Place the Addins/UpdateTextSketchesOnSave folder into your Fusion 360 [AddIns folder](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-install-an-ADD-IN-and-Script-in-Fusion-360.html#:~:text=An%20add%2Din%20belongs%20in,Fusion%20360%5CAPI%5CAddIns).
2. Restart Fusion 360. 
3. Ensure the Addin is running.

## How does it work?

The Add-in works off of two assumptions

* There are sketch layers whose names match document parameters or hardcoded references to version numbering.
* ANY text objects in those sketches should be updated with the value of that parameter or hardcoded reference.

When the document is saved, the Addin runs and looks through the list of sketches and looks for matching parameters. If it finds matches it updates ***ALL*** text objects in the sketch with the current value of the parameter. Hardcoded references are similarly updated.

At this time, the hardcoded references consist of two differently formatted versions of the file version number.

## Future Enhancements

Paramaterized formatted strings?