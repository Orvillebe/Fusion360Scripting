# StampButton

This is a simple Fusion 360 Addin design to create an embossed notice on a chosen surface so that printed parts will show the file version number. It depends on the UpdateTextSketchesOnSave Addin to update the notice when the version number updates.

## Installing

1. Copy the contents of the Addins Folder into your Fusion 360 [AddIns folder](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-install-an-ADD-IN-and-Script-in-Fusion-360.html#:~:text=An%20add%2Din%20belongs%20in,Fusion%20360%5CAPI%5CAddIns).
2. Restart Fusion 360. This should add a Stamp Button and a Stamp menu item on the ***ADD-INS*** pulldown on the Utilities tab.
3. Make sure both Addins are running before saving, this should automatically update all stamps created with the StampButton Addin.

## Usage

1. Select the Stamp button from the Utilities tab. This will present a dialog.
 - Select the Object face to emboss.
 - Set/Update the Depth value for the embossment.
 - Set/Update the Height value for the lettering.
 - Select the Format
   + Version Number displays just the version number ( v41 )
   + Extended Version Number displays the version number, followed by the file name and the part number if applicible. ( v41 Widget 17 )
2. The Embossed value drops roughly centered on the chosen face with the current values for the formatted text. Open the sketch if you need to move it about
3. Saving the file will update the formatted text automatically.

## Notes

If you need to rename the sketches, be sure to include the formatting version name ( the default name for the sketch ) in the sketch name or it will break updating via UpdateTextSketchesOnSave.

## Future

A more generalized stamp feature for text layers with parameter-stored formatting.

