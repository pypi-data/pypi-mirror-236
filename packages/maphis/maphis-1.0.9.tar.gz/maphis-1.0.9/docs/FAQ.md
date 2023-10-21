# FAQ

## Can I access the raw segmentation data?
Yes, the .tif files of all segmented photos are stored in the `/Labels` subdirectory of the project directory.

Each pixel in these images has a value corresponding to one node in the segmentation hierarchy. (They do not form an unbroken sequence of 1, 2, 3… If region labels starting from 1 are desired instead of the hierarchy codes, the image can be easily transformed e.g. in ImageJ, using connected component relabeling.)

Similarly, the reflections .tif files are stored in the `/Reflections` subdirectory


## What is the best way to specify the scale of the photos?
If there is a scale bar with an indicated length somewhere near the edge of the photo, you can use the automatic scale detection, which attempts to find the bar and read its label using OCR. This works best while importing photos into a project, before the photos are downsampled from their original resolution to that suitable for the segmentation.

If you forget to perform automatic scale detection when importing the photos, you can do it later, but depending on the amount of downsampling, the OCR reading the scale bar label may fail if the label got too small.

A fallback method is using the `Set scale` button on a photo's thumbnail, and then either drawing a line on the photo and specifying its length, or entering the scale numerically.

## Can I work with photos without specifying the scale?
If the scale information is missing, the application tries to work at least with the distances or sizes measured in pixels. If you export the results measured in pixels to a spreadsheet, you can add the scale information later, and recalculate your values using the real units within the spreadsheet.

## How can I speed up manual editing of the segmentation?
Familiarize yourself with the constraint system, and the controls for fast switching between different constraint levels: point the mouse cursor at any part of the photo, hold `Ctrl`, and scroll the mouse wheel. This will cycle between all constraint levels applicable to that part of the photo. For instance, when pointing at `A4-right-S2`, the constraint will cycle between `none`, `specimen`, `appendages`, `A4-right`, and `A4-right-S2`.

When the right constraints are in effect, they prevent you from “painting outside the lines”, and you can perform edits even using otherwise crude tools, such as Brush with a very large radius.

It is also helpful to familiarize yourself with the way you can zoom (scrolling the mouse wheel) and pan around the photo (holding the middle button or mouse wheel and dragging), and “pipette” labels using the right mouse button.

## What is the purpose of the “Reflections” mask?
The Reflections mask specifies the areas of the photo in which the color should be considered unreliable (not representing the actual color of the specimen), e.g., because there is a visible glare or light reflection in that place.

Such pixels still contribute to the shape and size of the regions they belong to, but are ignored when computing color or texture information. If you are not working with color or texture measurements, you may skip working with the reflections completely.

## The measurement values for some of the appendages seem to be off.
If you were editing the segmentation, make sure you used the correct labels for the left-side and the right-side appendages. (In the default color map, the left-side and the right-side versions of a label are displayed with the same color, but they are still supposed to be two distinct labels.)

You might have accidentally painted, for instance, both antennae with the `A1-left` label. In such a case, the Area of `A1-left` would correspond to the combined area of both antennae, and the Area of `A1-right` would be zero.

(When correcting this, do it on the finest hierarchy level applicable. In this case, if the antennae are divided into sections, make sure the left antenna is composed of `A1-left-S1`, `A1-left-S2`, and `A1-left-S3`, and the right antenna is composed of their `right` counterparts. The higher hierarchy levels will be corrected automatically.)

## In Measurements, what is the difference between “Geodesic length” and “Length of the oriented bounding box”?
Intuitively, geodesic length refers to the length measured along an elongated object's centerline. It is suitable for measuring long, possibly bent regions, such as legs. Even if an appendage is bent in one or more places, the geodesic length should correspond to its stretched-out length.

However, for certain shapes, this measurement is not suitable. This may be the case with non-elongated shapes, or with shapes whose “width” is greater than their “length”, such as the head of some mantis species. In such a case, geodesic length would correspond to what we would ordinarily call the “width” of the mantis' head (i.e., its greatest dimension).

For such cases, calculating the width and length of the object-oriented bounding box might be more straightforward and intuitive. “Width” then corresponds to the dimension closer to the horizontal on the photo, and “length” to the dimension closer to the vertical.

## Should I compute the color measurements in RGB, or HSV?
This depends on the purpose of the measurements. Generally speaking, the HSV (Hue, Saturation, Value) model is closer to how humans intuitively understand colors, while the RGB (Red, Green, Blue) model corresponds to the technical representation of the data. When evaluating things like “perceptual similarity”, HSV will probably be a better representation to start.
