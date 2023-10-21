# Implementing an interactive tool
`MAPHIS` comes with a few basic segmentation tools like **Brush**, **Bucket**, **Knife** or **Polygon**. These are mainly provided for situations when a segmentation produced by the automatic segmentation plugin needs to be manually corrected and are therefore very simple in what they do.
If you need a tool that offers a more elaborate logic, e.g. something like the **Magic wand** tool familiar from photo editing programs, you have the option to implement such logic in your own tool. 

In this tutorial, we will go through the process of implementing your own tool. This tool will segment all pixels that have a color similar to that of the pixel clicked by the tool.

**NOTE** This tutorial is still under construction.