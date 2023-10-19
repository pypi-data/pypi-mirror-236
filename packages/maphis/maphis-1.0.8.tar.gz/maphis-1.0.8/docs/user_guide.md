# User guide
    
In this manual/tutorial, we will go through a common workflow analysing photos of two bug species, _Graphosoma lineatum_ and _Pyrrhocoris apterus_ (download links are provided below).

We will segment the photos, learn how to manually edit the segmentations, and extract various measurements of individual body parts.

At the end of the tutorial, two advanced topics will be discussed: comparing the body profiles of different     specimen groups (which can be used, e.g., when studying mimics and their models, or shape variations in different populations), and quantification of the texture/pattern.

- If you want to work with the photos used in this tutorial, you can download [MAPHISTutorialPhotos.zip](https://cbia.fi.muni.cz/files/software/maphis/MAPHISTutorialPhotos.zip) — this 78 MB archive contains high-resolution photos of the same two species (though not necessarily the same specimens).

- Alternatively, you can download [MAPHISTutorialPhotosDownsampled.zip](https://cbia.fi.muni.cz/files/software/maphis/MAPHISTutorialPhotosDownsampled.zip) — this 6.6 MB archive contains low-resolution photos for which some functions (such as automatic scale detection) may not perform ideally.

The sets contain photos of _Graphosoma lineatum_ and _Pyrrhocoris apterus_. The _Graphosoma_ specimens have been included specifically because the automatic segmentation plugin has not been trained to segment photos of this species — you will be able to examine what incorrect segmentations look like, and practice manual editing using the provided tools. In contrast, the automatic segmentation of the _Pyrrhocoris_ photos should be reliable.
    
---
    
1. ### Create a new project
	To work with specimen photos in MAPHIS, you need to have the photos organized in projects. We will start the tutorial by creating one:
	1. Start the MAPHIS application.
	2. From the menu bar, select `File/New project... (Ctrl+N)`. A “Create a new project” dialog will appear. Fill in the name of the project you want to create (such as “TutorialProject”), and choose where to save the project's data using the upper `Browse...` button, or type a location (such as “C:/MAPHIS/Projects”) directly:<br />
    ![Setting the project name and save location](../images/user_guide/CreateANewProject1.png "Setting the project name and save location")	
    3. Choose some photos to import into the project: click the lower `Browse...` button, navigate to a folder containing your photos, and confirm the selection. If the photos in the selected folder are further organized in subfolders, increase the `Folder scan depth`. In our case, we will navigate to the “MAPHISTutorialPhotos” folder, select it, and set the scan depth to 1, so that photos inside both the “Graphosoma” and the “Pyrrhocoris” subfolders will be used:<br />
    ![Browsing for the photos to import](../images/user_guide/CreateANewProject2.png "Browsing for the photos to import")<br />
    (If there were further subfolders inside these, such as “Graphosoma/Male”, “Graphosoma/Female” etc., we would set the scan depth to 2.)
	4. After the photo folder has been selected, a list of photo thumbnails found inside will be displayed:<br />
    ![Photos ready for import](../images/user_guide/CreateANewProject3.png "Photos ready for import")
		- Above the photo list, you can choose to downsample all photos to a specified maximum height for the purposes of the application (copies will be created; your original photos will remain untouched). The automatic segmentation plugin supplied with MAPHIS tends to work best on images approximately 700 pixels high.
		- To downsample an individual photo, double-click its `New size (px)` cell in the list.
		- If your images contain scale markers such as these ![Example scale bar](../images/user_guide/ScaleBar1.png "Example scale bar"), scale can be automatically determined by clicking `Extract scale from scale markers` (this may take a moment, and may fail if the scale bars are too small or too blurred in the photos). If the detection is successful, the detected scale bars will be displayed in the list together with the reference lengths extracted from them (for quick verification). If any of the scale values are incorrect or missing, they can be edited later.
		- To specify the scale of an individual photo, double-click its `Scale` cell in the list. The process of individual scale setting is described below.
		- Above the photo list, you can also choose how to assign initial tags to your photos. Each photo in a project can have several tags that allow you to organize them into various groups — typical tags would be for instance “Graphosoma”, “Female”, or “FoundAtLocation1”. You can either have the tags assigned automatically based on which subfolder a particular photo was stored in (default), or you can assign a specific set of initial tags, separated by commas, to all photos (such as “Graphosoma, Female”). Tags can also be freely edited later.
		- To set the tags of an individual photo, double-click its `Tags` cell in the list and enter the tags separated by commas.
		- In the checkbox column on the left, you can select which photos to import, and which ones to skip.
	5. When you have selected the photos you want to import into the newly created project, click `Create`. More photos can be added to a project later by selecting `File/Import Photos... (Ctrl+I)`.

    ---

2. ### Browse, adjust, and organize photos in a project
	1. After you create a new project or open an existing one, you will see the thumbnails of all photos in the project on the left side of the screen. 
		- To navigate between photos, simply click the thumbnails, or use the arrow buttons ![Photo navigation buttons](../images/user_guide/NavigationButtons1.png "Photo navigation buttons")	below the main photo display.
		- If you need to select multiple photos (for instance to apply a plugin to a specific subset of the photos), you can select multiple photos by Ctrl+clicking, or Shift+clicking to select an interval. 
    2. When you hover the mouse cursor over any of the thumbnails, additional controls will appear:<br />
    ![Photo thumbnails with additional controls](../images/user_guide/MainWindowThumbnails1.png "Photo thumbnails with additional controls")
    These buttons allow you to:
		-  Delete ![Delete icon](../images/user_guide/Delete1.png "Delete icon") individual photos and associated data (such as segmentations and measurements) from the project.
		- Rotate photos counter-clockwise ![Rotate counter-clockwise icon](../images/user_guide/Rotate1.png "Rotate counter-clockwise icon") or clockwise ![Rotate clockwise icon](../images/user_guide/Rotate2.png "Rotate clockwise icon") (the supplied segmentation plugin assumes a canonical orientation with the arthropod's head pointing up).
		- Shrink ![Shrink icon](../images/user_guide/Shrink1.png "Shrink icon") the photo if its pixel dimensions are too large.
		- Set the scale ![Set scale icon](../images/user_guide/SetScale3.png "Set scale icon") of the photo (if it hasn't been already determined, or if it needs to be corrected).
	3. Next to the name of each photo, you can also see a field displaying all tags of that photo.
		- If you hover the mouse cursor over the field, a small panel will pop up and let you add or remove the tags. To add a brand new tag, type it into the text field and press Enter:<br />
        ![Photo thumbnails with additional controls](../images/user_guide/MainWindowThumbnails2.png "Photo thumbnails with additional controls")
		- Above the thumbnail list, there is a `Tag filter` field that allows you to display only the photos with a particular combination of tags. You can use this to view, for instance, only the photos that have the “Pyrrhocoris” tag (or a combination, such as “Pyrrhocoris, Male”):
![Using tag filter to display only the “Pyrrhocoris” photos](../images/user_guide/MainWindowThumbnails3.png 'Using tag filter to display only the “Pyrrhocoris” photos')
		- You can also filter the photos based on the availability of the scale information.
		- To remove the current filter and show all photos again, click the `Clear` button next to the filter.
	4. To set a scale of a photo, use the small button with the icon of a ruler ![Set scale icon](../images/user_guide/SetScale3.png "Set scale icon") in the bottom right corner of a photo's thumbnail. A new window will open.
		- In this window, zoom (scrolling the mouse wheel) and pan (holding the middle button or mouse wheel and dragging) to a scale bar or a ruler present in the photo:<br />
        ![Zooming to the scale bar in the Set scale window](../images/user_guide/SetScale1.png "Zooming to the scale bar in the Set scale window")
		- After that, draw a line from one end of the scale bar to the other (holding the left mouse button and dragging). Then specify the real-world length of the line you have drawn using the controls at the top (in this case, “200 μm”):<br />
        ![Manually specified reference line to set the scale of 60 pixels = 200 micrometers](../images/user_guide/SetScale2.png "Manually specified reference line to set the scale of 60 pixels = 200 micrometers")
		- When you are satisfied with the reference line drawn and the length entered, click `Accept changes for this photo` to set this scale for this photo, or `Accept changes for all photos` to set it for all photos in the project.
		- Automatic detection of the scale can be attempted by clicking the buttons in the `Automatic scale extraction from markers` box (this could have been done also when importing the photos). 
		- If you want, you can also specify the scale explicitly with the `Enter scale numerically` button (this numerically specified scale can also be assigned either just to the current photo, or to all photos in the project).

    ---
    
3. ### Use automatic segmentation & detection of reflections
	1. Once all photos are ready (reasonable size and the specimens in a “head upwards” orientation, ideally also with the scale values specified), you can use the automatic segmentation plugin to divide the photo into regions corresponding to individual body parts. MAPHIS is distributed with a segmentation plugin based on a U-Net. To select it, pick `Arthropod segmentation` from the drop-down list in the upper right corner of the screen:<br />
![Selecting the segmentation plugin](../images/user_guide/Segmentation1.png "Selecting the segmentation plugin")
	2. To start the computations, click the `Apply to all` button below the drop-down list. Alternatively, you can apply the segmentation only to the currently selected subset of the photos (often just the one photo being displayed); or, using the small drop-down arrow, to all those photos that do not have a segmentation yet. Once started, the segmentation may take some time to finish.<br />
    ![Segmentation in progress](../images/user_guide/OperationRunning1.png "Segmentation in progress")<br />
    After the segmentation is computed, you can examine the regions into which the photo has been divided:<br />
    ![Selecting the segmentation plugin](../images/user_guide/Segmentation2.png "Selecting the segmentation plugin")
    You can adjust the display by using the `Mask style & opacity` controls above the photo.
	3. Often, the photos may contain areas where glare or light reflections are visible. Those areas can still be parts of the specimen mask, but the colour information there is unreliable (i.e., not suitable for colour or texture analysis). To detect such areas in a segmented photo, you can use the supplied `Reflections` plugin from the same drop-down list, again using `Apply to all`:<br />
![Reflections mask, with reflections indicated in purple](../images/user_guide/Reflections1.png "Reflections mask, with reflections indicated in purple")
		- Note that the detection of reflections works only within the mask of a specimen. That means that the photo has to be segmented first. Otherwise, no reflections will be marked.

		In the `Active mask` panel above the photo, you can switch between the display of the individual specimen regions (`Labels`), and the reflections (`Reflections`; here, the areas with reflections are indicated with purple, unless otherwise specified).

	4. An important aspect of the segmentation is its hierarchy, which specifies the relationship between individual body parts.

		- By default, the photo is divided into the background, and the specimen. The specimen is divided into the body, and the appendages. The body is divided into head, thorax, and abdomen. And each appendage is divided into three segments. The whole default hierarchy is shown here:<br />
![Default segmentation hierarchy](../images/user_guide/Hierarchy1.png "Default segmentation hierarchy")
		- Each region is indicated by a different “label”. The labels may or may not be shown in different colours; in the default hierarchy for instance, appendages on the left and on the right side have the same colours, but the left and the right version of each are two distinct regions.
		- You can quickly examine what label each part of the photo has by hovering the mouse cursor over the photo and looking at the status text below. Here, for instance, the mouse cursor is hovering over the tip of the right antenna, which has the “A1-right-S3” label, and is shown in dark purple:<br />
![Hovering over a region](../images/user_guide/HoveredLabel1.png "Hovering over a region")

	5. You can examine different levels of the hierarchy by clicking the individual labels in the list on the right. When you click a label, the main view will switch to the lowest hierarchy level that contains that label.
		- When you click the `specimen` label, you will see the photo segmented into the specimen and the background:<br />	![First level of the segmentation hierarchy](../images/user_guide/HierarchyLevel1.png "First level of the segmentation hierarchy")
		- 	When you click the `body` or `appendages` labels, you will see the specimen divided into the body and the appendages:<br />	![Second level of the segmentation hierarchy](../images/user_guide/HierarchyLevel2.png "Second level of the segmentation hierarchy")
		- When you click a label of an individual whole appendage, such as `A1-left`, you will see the photo segmented so that each appendage forms one region:<br />	![Third level of the segmentation hierarchy](../images/user_guide/HierarchyLevel3.png "Third level of the segmentation hierarchy")
		- When you click a label of an appendage segment, such as `A1-left-S1`, or the `head`, `thorax`, or `abdomen` labels, you will see the photo segmented at the finest hierarchy level:<br />	![Fourth level of the segmentation hierarchy](../images/user_guide/HierarchyLevel4.png "Fourth level of the segmentation hierarchy")

	6. If you want, you can change the displayed colours and names of the labels by double-clicking them in the list on the right, and using the dialog that pops up:<br />
![Colour and name of a label can be edited by double-clicking the label in the list](../images/user_guide/ModifyLabel1.png "Colour and name of a label can be edited by double-clicking the label in the list")<br />
When the `Active mask` is set to `Reflections`, you can use this to change the colour used to indicate the reflections.

    ---
    
4. ### Make manual adjustments

    After running the automatic segmentation, it is possible to manually edit the segmentation masks in case any corrections are necessary. It is also possible to create an entire segmentation from scratch this way — that can be useful when working with photos for which no automated segmentation plugin is available (e.g., photos of plants, fish, or even photos from  entirely different domains, such as material science).
    
    You can manually edit both the hierarchical segmentation of a specimen into regions, and the reflection mask.
    
    We will demonstrate the edits on the segmentation of the `Pyrrhocoris2.tif` photo. We see that the tip of the right antenna hasn't been detected properly (area labeled as “1”), and the subdivision of some legs into the segments needs improvement (areas “2”, “3”):<br />
    ![Automatically segmented Pyrrhocoris2.tif and areas that need manual adjustments](../images/user_guide/PlacesToEdit1.png "Automatically segmented Pyrrhocoris2.tif and areas that need manual adjustments")<br />
    (You can zoom by scrolling the mouse wheel, and pan around by holding the middle button or mouse wheel and dragging.)
    
    ---
#### Editing tools & constraint system
    
    To make manual edits, the application offers a set of tools that should be familiar from common image editing programs. The tools can be selected from this toolbar on the right side of the window:<br />
    ![Brush tool icon](../images/user_guide/ToolBrush1.png "Brush tool icon") ![Bucket tool icon](../images/user_guide/ToolBucket1.png "Bucket tool icon") ![Knife tool icon](../images/user_guide/ToolKnife1.png "Knife tool icon") ![Polygon tool icon](../images/user_guide/ToolPolygon1.png "Polygon tool icon") ![Ruler tool icon](../images/user_guide/ToolRuler1.png "Ruler tool icon") ![Landmarks tool icon](../images/user_guide/ToolLandmarks1.png "Landmarks tool icon")<br />
    
    The application offers a simple “constraint system” that allows you to limit any edits to within a specified area, helping you “stay inside the lines” as in a coloring book. We will demonstrate its functionality in a moment, together with the Polygon tool.
    
    When editing, you should generally select the “active” or “current” label by clicking on it in the region hierarchy panel. To fix the missing tip of the right antenna, we will need to select the `A1-right-S3` label:<br />
    ![Selecting the A1-right-S3 label](../images/user_guide/SelectLabelA1-right-S3.png "Selecting the A1-right-S3 label")<br />
    
    (Be careful: the selected label is not the same as “color” — for instance, the `A1-left-S3` and `A1-right-S3` labels might both be displayed using the same purple color, but they are two distinct labels, and must be treated as such.)
    
    When a tool is active, you can also “pipette” a label directly from the segmentation mask by right-clicking the mouse. After the right-click, you should see the selection change in the hierarchy panel. Right-clicking the background will select the `nothing` label.
    
    ---
    
    1. The Brush tool is selected using this icon:  ![Brush tool icon](../images/user_guide/ToolBrush1.png "Brush tool icon")
    
        We will correct the tip of the right antenna (area “1”) with the Brush. Click the tool icon, and set `Radius` below it to something small, like 3. You can also change the Brush radius by holding down `Shift` and scrolling the mouse wheel.
    
        If you haven't selected the `A1-right-S3` label yet, do it either by clicking it in the hierarchy panel, or by right-clicking the existing part of the antenna's last segment to “pipette” it. The cursor should now indicate the selected label and the brush size:<br /> ![Brush cursor](../images/user_guide/BrushCursor1.png "Brush cursor")<br />
    
        Draw the tip of the antenna as you would in any image editing program. If you make a mistake, you can use `Ctrl+Z` and `Ctrl+Y` as “undo” and “redo” (these work also with other tools). To shrink a region, mark a part of the photo as background using the `nothing` label (you can “pipette” it by right-clicking the background).
    
        (In general, you should always use the most specific applicable label of the hierarchy, such as `A1-right-S3` or `head`. It is however possible to use also the less-specific ones, if needed. You can, for instance, use the `body` label to mark the pixels that should belong to the specimen's body, but shouldn't be for some reason counted as part of its `head`, `thorax`, or `abdomen`.)
    
    2. The Bucket tool is selected using this icon:  ![Bucket tool icon](../images/user_guide/ToolBucket1.png "Bucket tool icon")
    
        When using the paint bucket, you can fill a contiguous area of the segmentation mask with the active label.
        
    3. The Knife tool is selected using this icon:  ![Knife tool icon](../images/user_guide/ToolKnife1.png "Knife tool icon")
        
        This tools lets you slice the regions using straight cuts of a specified width. We will correct the subdivision of the middle right leg (area “2”) into segments by using the Knife and the Bucket to expand the middle segment of the leg.
        
        First, select the Knife tool. Then pipette the `A3-right-S2` label by right-clicking the middle segment of the leg. Then draw a cut across the joint by dragging the mouse:<br />
        ![Using Knife tool](../images/user_guide/UsingKnife1.png "Using Knife tool")<br />
        
        Finally, select the Bucket tool and click the area between the cut and the rest of the middle leg segment to change its label from `A3-right-S1` to `A3-right-S2`:<br />
        ![Using Bucket tool](../images/user_guide/UsingKnife2.png "Using Bucket tool")<br />
    
    4. The Polygon tool is selected using this icon:  ![Polygon tool icon](../images/user_guide/ToolPolygon1.png "Polygon tool icon")
    
        The Polygon tool lets you fill a polygonal area by marking its circumference with a combination of clicking (to place individual vertices) and dragging/drawing (to draw free-hand parts).
        
        We will demonstrate this tool by fixing the subdivision of the bottom right leg (area “3”). To do that, we will also use the application's “constraint system”. We will need to expand the leg's middle segment:<br />
        ![Bottom right leg to be fixed](../images/user_guide/ConstraintsAndPolygon1.png "Bottom right leg to be fixed")<br />
        
        First, select the Polygon tool and the `A4-right-S2` label corresponding to the middle segment of the leg. We see that the leg itself is segmented correctly, only its subdivision needs to be adjusted. To limit any further edits to within the bottom right leg, move your mouse to the `A4-right` label in the region hierarchy panel, and click the `Set constraint` button that appears next to it:<br />
        ![Constraining edits to the bottom right leg](../images/user_guide/ConstraintsAndPolygon2.png "Constraining edits to the bottom right leg")<br />
        
        The display will indicate that any edits made now will be limited to within the `A4-right` region, i.e., the bottom right leg:<br />
        ![Active constraint limiting edits to the bottom right leg](../images/user_guide/ConstraintsAndPolygon3.png "Active constraint limiting edits to the bottom right leg")<br />
        
        With the `A4-right-S2` label selected, and the constraint set to `A4-right`, draw any polygon that fixes the leg subdivision. You don't need to care about intersecting any other regions. You can combine clicking and dragging. To finish drawing the polygon, double-click:<br />
        ![Drawing a polygon](../images/user_guide/ConstraintsAndPolygon4.png "Drawing a polygon")<br />
        
        To remove the constraint, click the `Remove constraint` button in the hierarchy panel.
        
        **Notes on efficient using of the constraint system**:
        
        The constraint system can be used together with any tool. For instance, the same result as above could be achieved also with a single click using an oversized Brush:<br />
        ![Using a large brush with active constraint](../images/user_guide/ConstraintsAndPolygon5.png "Using a large brush with active constraint")<br />
        
        If you want to quickly switch between different constraints, you can point the mouse cursor at any part of the photo, hold  `Ctrl`, and scroll the mouse wheel. This will cycle between all constraint levels applicable to this part of the photo. For instance, when pointing at `A4-right-S2`, the constraint will cycle between none, `specimen`, `appendages`, `A4-right`, and `A4-right-S2`:<br />
	    ![Constraints: none](../images/user_guide/ConstraintLevels1.png "Constraints: none") ![Constraints: specimen](../images/user_guide/ConstraintLevels2.png "Constraints: specimen") ![Constraints: appendages](../images/user_guide/ConstraintLevels3.png "Constraints: appendages") ![Constraints: A4-right](../images/user_guide/ConstraintLevels4.png "Constraints: A4-right") ![Constraints: A4-right-S2](../images/user_guide/ConstraintLevels5.png "Constraints: A4-right-S2")<br />
	    
    5. The Ruler tool is selected using this icon: ![Ruler tool icon](../images/user_guide/ToolRuler1.png "Ruler tool icon")
    
        This tool is not used for editing, but for quick measurements. To measure a distance, select the Ruler and drag a line from one point to another. If you tick the `Multi-ruler` box, you can place multiple rulers in the photo and see their total length as `Total measurements`. Right-clicking removes all rulers.<br />
        ![Using the Ruler tool](../images/user_guide/UsingRuler1.png "Using the Ruler tool")<br />
	    
    6. The Landmarks tool is selected using this icon: ![Landmarks tool icon](../images/user_guide/ToolLandmarks1.png "Landmarks tool icon")
    
        This tool is not used for editing, but for specifying arbitrary points of interest in the photos, which are saved together with your project. To place a landmark, select the tool and click anywhere in the photo. You can also move existing landmarks by dragging them. Each landmark has its [X, Y] coordinates within the photo, and its label, which you can select from a pre-made set, or type in your own, such as “Tip of the left antenna”.<br />
        
        When you later export computed measurements, the landmark coordinates will be exported too, and you will be able to do processing such as calculating their pairwise distances, etc.<br /> 
        ![Using the Landmarks tool](../images/user_guide/UsingLandmarks1.png "Using the Landmarks tool")<br />

    ---
#### Indicating approvals
    
    To keep track of which photos have had their segmentations examined and manually corrected, you can mark each photo with the “approval” buttons above the main view:<br />
    ![Approval buttons](../images/user_guide/Approvals1.png "Approval buttons")<br />
    
    Each button corresponds to one level of the hierarchy. To indicate that you consider the segmentation up to a certain hierarchy level “satisfactory” or “done”, simply tick the corresponding box. The approval status of each photo is indicated with small icons in the corner of its thumbnail.
    
    In the following example, the `Specimen` level of the `Pyrrhocoris1.tif` has been approved, but its division into `Body/Appendages` (and further) is still marked as “work in progress”. `Pyrrhocoris2.tif` has been approved except the finest subdivision of the appendages into sections, and `Pyrrhocoris3.tif` probably hasn't been checked yet:<br />
    ![Approval icons](../images/user_guide/Approvals2.png "Approval icons")<br />
    
    Be careful: editing the segmentation can invalidate the approvals. After any edits, it is good to verify if the approvals still reflect your satisfaction with the segmentation.
    
    <div style="display:none">---
Editing the whole segmentation hierarchy
    
    You have seen that you can adjust the name and the colour of each label in the hierarchy (allowing changes such as renaming “A1-left” to “Left Antenna”). The hierarchy itself is defined by the plugin that created the segmentation.
    
    However, if you wish to manually draw a segmentation of a specimen type for which no segmentation plugin exists, you can define your own region hierarchy. To do this, right-click a node in the hierarchy tree, and click `Remove label` or `Remove label and children` to remove that region from the hierarchy, or click `New child label` to add a new sub-region with a desired name and colour. (Note that the root of the hierarchy cannot be removed, and the hierarchy cannot be deeper than 4 levels.)
    
    For instance, if you wanted to manually segment microscopic cell images and then use the program to perform some measurements, you could define a hierarchy with a region called “cell”, which would divided into “cytoplasm” and “nucleus”, etc.</div>
    
    ---
    
5. ### Take and export measurements
    1. When the photos are segmented to your satisfaction (which you can indicate using the Approvals described above), you can proceed to taking the measurements. To do this, switch to the Measurements tab. Initially, it contains an empty table:<br />
    ![Measurements tab](../images/user_guide/ComputeMeasurements1.png "Measurements tab")<br />

    2. After clicking `Compute new measurements`, a new window will open. Here you can select which measurements should be computed for which regions. For instance, you can select `body` in the list of regions, and `Area`, `Oriented bounding box dimensions`, `Circularity`, `Profile`, and `Mean HSV` in the list of available measurements:<br />
    ![Selecting measurements to compute](../images/user_guide/ComputeMeasurements2.png "Selecting measurements to compute")<br />
        Then click `Assign ->` to add these combinations to the list of measurements to be computed:<br />
        ![Selected measurements](../images/user_guide/ComputeMeasurements3.png "Selected measurements")<br />
    
    3. This can be repeated until you have specified all “region + measurement” combinations you want computed. Different measurements make sense for different regions. For instance, `Geodesic length` is useful to measure the length of appendages, because it measures the regions along the centerline, taking any bends into account. For a more compact region such as `body`, `Oriented bounding box dimensions` would be more appropriate. The full list of available measurements with explanations is provided below.
        
        In this tutorial, we will also select `Geodesic length` and `Mean width` for each of the individual appendages `A1-left` through `A4-right`, and `GLCM properties` (measuring pattern/texture) for `abdomen`. If any of the selected measurements have any parameters, you can adjust them in the rightmost panel. In our example, tick `contrast` in the `GLCM properties` panel to include this property in the results:<br />
        ![Selected measurements](../images/user_guide/ComputeMeasurements4.png "Selected measurements")<br />
        
        If you want to re-use a list of “region + measurement” combinations that you have prepared, you can use `Save configuration...` and `Load configuration...`. To remove a combination from the list, select it and click `Remove`.
    
    4. When everything is set up, click `Apply` to perform the selected measurements. Provided the segmentation was correct, you should see something like this after the computation finishes:<br />
    ![Table of computed measurements](../images/user_guide/ComputeMeasurements5.png "Table of computed measurements")<br />
        In this view, we can briefly examine the results. Already just looking at the table, we can see that, for instance:
        - The _Pyrrhocoris_ specimens were smaller than the _Graphosoma_ ones.
        - The bodies of the _Graphosoma_ specimens were slightly more circular than those of the _Pyrrhocoris_ specimens (which were narrower).
        - The mean color of the _Graphosoma_ specimens was more varied.
        - The body profile of the _Graphosoma_ specimens differs from the _Pyrrhocoris_ ones, with a narrowing between the thorax and the abdomen (head is to the left).
        - No antennae were segmented for one of the _Graphosoma_ specimens.
    
    5. To examine a compound measurement result in detail, double-click its cell. In our example, we can do this with the `Profile` vectors, or with the matrices that form the results of the `Contrast` measurement:<br />
    ![Details of the Contrast measurement](../images/user_guide/ContrastMatrices1.png "Details of the Contrast measurement")<br />
        (In the `GLCM properties` measurements like `Contrast`, the results quantify the pattern in different directions and over different distances, forming a matrix for each of the Hue, Saturation, and Value channels. We will show how these values can be processed and understood below.)
    
    6. Finally, you can export the table of all computed measurements and landmark positions to a spreadsheet format, to process the data in other software. Click `Export measurements`, and then choose whether you want to save the results in the `.xlsx` format for Microsoft Excel and compatible, or as `.csv` (comma separated values) for more general processing (e.g., by your own scripts):<br />
    ![Exporting the measurements](../images/user_guide/ExportMeasurements1.png "Exporting the measurements")<br />
    
    ---
    
6. ### Available measurements
    
    <style>
    table {
        width: 100%;
        margin-bottom: 3ex;
    }
    th {
        display: none;
    }
    th:first-of-type, td:first-of-type {
        width: 20%;
    }
    th, td {
        padding: 5px 10px 5px 10px;
    }
    td {
        border: 1px solid black;
    }
    </style>

    ** Size (in pixels or SI units) **
    
    |   |   |
    | --------------------------------- | ----------- |
    | Area                              | Total area of the region. |
    | Geodesic length                   | Along-the-centerline length. Suitable for elongated regions such as appendages (takes any bends into account).        |
    | Max feret diameter                | Maximum “caliper” size of the region. |
    | Mean width                        | Mean width. Suitable for elongated regions such as appendages. |
    | Oriented bounding box dimensions  | <p>Size of the minimum-area bounding box of the region. Suitable for more compact regions such as the specimen body, its head, etc.</p><p>In the parameter settings, select which dimensions to include: `width` is the dimension closer to horizontal, `length` is the dimension closer to vertical.</p> |
    
    ** Shape **
    
    |   |   |
    | --------------------------------- | ----------- |
    | Circularity                       | Value from 0.0 to 1.0, where 1.0 means a perfect circle. |
    | Profile                           | <p>Vector of 40 distances between the region outline and its main axis, spaced at regular intervals, describing the overall shape of the region.</p><p>When exported to a spreadsheet application, you can plot these values as a graph, with results similar to the small graphic preview shown in the Measurements table.</p><p>The profiles can also be used for more elaborate comparisons directly inside MAPHIS (see the next chapter).</p> |
    
    ** Pattern/texture ** (These measurements ignore pixels in areas marked as reflections.)
    
    |   |   |
    | --------------------------------- | ----------- |
    | GLCM properties                   | <p>Properties calculated from a Gray-Level Co-occurrence Matrix (GLCM), based on _“Haralick, R. M., Dinstein, I., & Shanmugam, K. (1973). Textural Features for Image Classification. IEEE Transactions on Systems, Man and Cybernetics, 3(6), 610–621. [https://doi.org/10.1109/TSMC.1973.4309314](https://doi.org/10.1109/TSMC.1973.4309314)”_.</p><p>To use these, you should select which properties you want to compute, and then specify a list of distances and a list of angles. `Distances in mm` should contain a list of distances separated by commas, such as “0.03125, 0.0625, 0.09375, 0.125, 0.15625, 0.1875, 0.21875, 0.25”. `Angles in degrees` should contain a list of angles separated by commas, such as “0, 90” (values should come from the [0, 180) interval; angle 0 is “to the right”).</p><p>For each selected property, the result will consist of three matrices: one for each of the Hue, Saturation, and Value colour channels. In each matrix, the values express the relationship between pixels that are a certain distance apart in a certain direction. For instance, you can examine the average contrast of pixels that are 0.125 mm apart in horizontal direction (0°). An example that should help you understand this more intuitively, including a useful application, will be provided in a chapter below.</p><p>The available properties are:</p><ul><li>ASM: Angular second moment, a measure of homogeneity.</li><li>Contrast: Amount of local variation.</li><li>Correlation: Measure of grey-level linear dependencies.</li><li>Dissimilarity: Weighted sum of absolute grey-level differences.</li><li>Energy: Square root of ASM.</li><li>Homogeneity: Inverse difference moment.</li></ul> |
    
    ** Colour ** (These measurements ignore pixels in areas marked as reflections. Also note that “averaging” colours works differently in different colour models, so measurements using the HSV and RGB models shouldn't be mixed together.)
    
    |   |   |
    | --------------------------------- | ----------- |
    | Mean HSV                          | Mean Hue, Saturation, Value colour values. |
    | Mean RGB                          | Mean Red, Green, Blue colour values. |
    
    ---
    
7. ### Advanced measurements: Profile fusion and comparison

    Here we will show how the computed profiles (most commonly body profiles) of multiple specimens can be combined and compared. Comparing the body shapes of _Graphosoma_ and _Pyrrhocoris_ specimens this way is a bit artificial task, but the same process can be used to compare, e.g., the body shapes of certain ants and ant-mimicking spiders.
    
    To do this, we will need the body profile measurements that we computed earlier. For the sake of the example, we will also update the tags of the photos. To simulate that we want to compare specimens originating from two different locations, two of the _Graphosoma_ photos will get a “FromLocationA” tag, and the other two will get “FromLocationB”. We will then do the same with the _Pyrrhocoris_ photos.<br />
    ![Photos with updated tags](../images/user_guide/PhotosWithTags1.png "Photos with updated tags")<br />
    
    If we want to compare groups of profiles, we first need to compute a “median profile” for each group, and compare those — such as “median _Graphosoma_” vs. “median _Pyrrhocoris_”, or “median _Pyrrhocoris_ from location A” vs. “median _Pyrrhocoris_ from anywhere”.
    
    The issue with comparing or combining the computed profiles directly (e.g., in a spreadsheet program) is that there are inter-specimen differences that do not correspond to the general body shape of a species, but to individual variations of size. To mitigate this, the profiles in each group first need to be aligned:<br />
    ![Aligning profiles](../images/user_guide/AligningProfiles1.png "Aligning profiles")<br />
    Figure (a) shows a set of raw, misaligned profiles (in this case, an ant _Opisthopsis haddoni_). Figures (b) and (c) show how matching extrema (body constrictions) are identified in the profiles, and how the profiles are aligned to match more closely. Figure (d) then shows the set of profiles after they have been aligned. If we compare the median profile (dashed line) of the misaligned set (a) with that of the aligned set (d), we can see that the alignment helps to preserve the body constrictions, which could otherwise be “smoothed out”.
    
    The process described above can be used within MAPHIS. To start, select `Plugins/Profile fusion` from the menu. A new window will open:<br />
    ![Profile fusion window](../images/user_guide/ProfileFusion1.png "Profile fusion window")<br />
    
    We will want to compare the _Pyrrhocoris_ specimens from location A with those from location B. To compare them correctly, we should map/register both of these groups to a common space. We will do this in two steps:

    - Compute the median profile of _Pyrrhocoris_ from location A and map/register it to the median profile of all _Pyrrhocoris_ specimens.
    - Compute the median profile of _Pyrrhocoris_ from location B and map/register it to the median profile of all _Pyrrhocoris_ specimens.
    
    Move the mouse over the left field that says “hover to select tags”, and check `Pyrrhocoris` and `FromLocationA`:<br />
    ![Selecting profiles to register](../images/user_guide/ProfileFusion2.png "Selecting profiles to register")<br />
    In the right field, check only `Pyrrhocoris`. The window should now look like this, with the first registration task being _“Median profile of FromLocationA & Pyrrhocoris will be registered to the median of the following: median profile of Pyrrhocoris”_:<br />
    ![One registration task ready](../images/user_guide/ProfileFusion3.png "One registration task ready")<br />
    
    To add the second task, click the long `+` button beneath the first task panel. In the second task panel, select `Pyrrhocoris` and `FromLocationB` in the left field, and `Pyrrhocoris` in the right field. The window should now look like this, with the second registration task being _“Median profile of FromLocationB & Pyrrhocoris will be registered to the median of the following: median profile of Pyrrhocoris”_:<br />
    ![Both registration tasks ready](../images/user_guide/ProfileFusion4.png "Both registration tasks ready")<br />
    
    If you want to re-use the configuration you have set up in this window, you can use `Save configuration...` and `Load configuration...`.
    
    When you click `Apply`, the results will be saved in a `registered_profiles/profiles.xlsx` file in the project folder.
    
    The first sheet of the document will contain the raw median profiles from all tasks (“median Pyrrhocoris from location A”, “median Pyrrhocoris from location B”, and two instances of “median Pyrrhocoris”). 
    
    The second sheet, `Aligned profiles`, will contain the important results: the profiles mapped to the desired space. In this case, there will be “median Pyrrhocoris from location A mapped to median Pyrrhocoris”, and “median Pyrrhocoris from location B mapped to median Pyrrhocoris”. These aligned profile values can then be plotted or compared with one another easily:<br />
    ![Aligned profiles in the “profiles.xlsx” spreadsheet](../images/user_guide/AlignedProfiles1.png "Aligned profiles in the “profiles.xlsx” spreadsheet")<br />
    (Admittedly, these do not have very exciting profiles.)
    
    ---
    
    We may also want to compare profiles from completely different groups of photos, which do not share tags. For instance, we can compare the _Pyrrhocoris_ profiles to the _Graphosoma_ ones by mapping both groups to their common median profile — i.e., to the median of (median _Pyrrhocoris_) and (median _Graphosoma_). To specify this “median of several different medians” on the right side, use the short `+` button below the right field in a task panel:<br />
    ![Specifying a combined registration target](../images/user_guide/ProfileFusion5.png "Specifying a combined registration target")<br />
    
    When everything is set correctly for comparing the _Graphosoma_ and _Pyrrhocoris_ profiles, the window should look like this:<br />
    ![Both tasks with a combined registration target](../images/user_guide/ProfileFusion6.png "Both tasks with a combined registration target")<br />
    The tasks specified in this window are:

    - “Median profile of Graphosoma will be registered to the median of the following: median profile of Graphosoma and median profile of Pyrrhocoris”
    - “Median profile of Pyrrhocoris will be registered to the median of the following: median profile of Graphosoma and median profile of Pyrrhocoris”
    
    After the registration is done, we can again visualize the aligned profiles in the spreadsheet:<br />
    ![Aligned profiles in the “profiles.xlsx” spreadsheet](../images/user_guide/AlignedProfiles2.png "Aligned profiles in the “profiles.xlsx” spreadsheet")<br />
    
    ---
    
8. ### Advanced measurements: Quantifying patterns using GLCM properties

    In this example, we will show how the `GLCM properties` measurements can be used to quantify the patterns. We will be using the measurements we computed previously: `GLCM contrast` of the `abdomen` region, computed with `Distances in mm` set to “0.03125, 0.0625, 0.09375, 0.125, 0.15625, 0.1875, 0.21875, 0.25”, and `Angles in degrees` set to “0, 90”. We will export the measurements into a “.xlsx” file and open it in a spreadsheet application. The GLCM properties are on the third sheet:<br />
    ![GLCM measurements in the spreadsheet](../images/user_guide/GLCMSpreadsheet1.png "GLCM measurements in the spreadsheet")<br />

    The C22 cell, for example, says the following (hover the mouse over individual parts of the sentence to see which cell they come from): _“In the <abbr title="B21">V channel</abbr> of <abbr title="A1">Graphosoma1.tif</abbr> <abbr title="B21">abdomen</abbr>, pairs of pixels that are <abbr title="B22">0.03125 mm</abbr> apart in the <abbr title="C21">horizontal (0°)</abbr> direction have the average <abbr title="B21">contrast</abbr> of <abbr title="C22">4017.278</abbr>”_.
    
    We will now compare the contrast of the horizontal and the vertical components of the pattern (that is why we picked the angles of 0° and 90°, respectively). For our purposes, the most useful values will be those in the `V` (Value) colour channel, which correspond to the brightness of the pixels.
    
    We will now compile four tables:

    - `V` values for the 0° angle for all _Graphosoma_ specimens.
    - `V` values for the 90° angle for all _Graphosoma_ specimens.
    - `V` values for the 0° angle for all _Pyrrhocoris_ specimens.
    - `V` values for the 90° angle for all _Pyrrhocoris_ specimens.
    
    For each table, we will also calculate the mean values:<br />
    ![Aggregated GLCM measurements](../images/user_guide/GLCMSpreadsheet2.png "Aggregated GLCM measurements")<br />
    
    Now we can plot the calculated mean values and interpret the results. We can clearly see that in the horizontal direction (angle 0°), the contrast of the _Graphosoma_ specimens depends on how far two pixels are apart. Specifically, the contrast is highest between pixels that are 0.0625 mm apart horizontally, and then again between pixels that are 0.1875 mm apart. The lowest contrast tends to be between pixels that are 0.125 mm apart horizontally:<br />
    ![Plots of aggregated GLCM measurements](../images/user_guide/GLCMSpreadsheet3.png "Plots of aggregated GLCM measurements")<br />
    
    Since we don't see any similar feature in the vertical (90°) _Graphosoma_ series, this suggests that the abdomen of the _Graphosoma_ specimens is vertically striped. We can even infer that the most common distance from the center of one stripe to the center of the next stripe of the same colour is approximately 0.125 mm. We can check this by using the `Ruler tool` and measuring it manually in MAPHIS:<br />
    ![Measuring the stripes manually](../images/user_guide/MeasuringStripes1.png "Measuring the stripes manually")<br />
    
    If we calculate the correlation between the 0° and 90° series for each species, we can even sum up these features into a single number.
    
    In the _Graphosoma_ specimens, the correlation value of -0.08 shows that the horizontal and vertical components of the pattern are quite different — i.e., that the pattern is directional, such as stripes.
    
    In the _Pyrrhocoris_ specimens, the correlation between the horizontal and vertical series is 0.8, indicating that any two pixels that are a certain distance apart tend to have the same relative contrast regardless of whether they are spaced horizontally, or vertically — i.e., that the pattern is not as directional.
    
    ---