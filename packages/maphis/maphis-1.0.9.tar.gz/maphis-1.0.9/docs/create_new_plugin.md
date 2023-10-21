# Creating a new plugin

## Overview
In this tutorial we will guide you through the process of creating a new plugin for MAPHIS. At the end, our plugin will allow the users to
segment images through simple thresholding based on user defined color.

## MAPHIS plugin system
A plugin in MAPHIS is simply a grouping of various *actions* and *tools*. 
Actions represent code that generates segmentations or computes properties of segmentation, while tools provide ways for the user to work with segmentations in an interactive manner.
All plugins are stored in the `plugins` folder of the `maphis` package, whose location depends on the way you've installed MAPHIS. You can simply access the folder by clicking **Plugins>Open plugins folder** in MAPHIS.

### Plugin folder structure
Below is illustrated the full structure of MAPHIS plugin. For a plugin to be recognized by the application there must be `plugin.py` and `__init__.py` located in the folder, all other folders and directories are optional, depending on what functionality you want to provide.
It is also good to include a `README.md` file containting any useful information about your plugin, especially if you plan to [publish it](publishing_your_plugin.md).


```
maphis/plugins/
    ├───custom_plugin/
    |    ├───__init__.py
    |    ├───plugin.py
    |    ├───README.md
    |    ├───general/
    |    |   ├─── *any number of python files*
    |    |   └───__init__.py
    |    ├───project_types/
    |    |   ├─── *any number of python files*
    |    |   └───__init__.py
    |    ├───properties/
    |    |   ├─── *any number of python files*
    |    |   └───__init__.py
    |    ├───regions/
    |    |   ├─── *any number of python files*
    |    |   └───__init__.py
    |    └───tools/
    |    |   └───__init__.py
```


## Plugin implementation
Now we will get to the actual implementation of the plugin.
Our plugin will provide a segmentation computation based on simple thresholding, and a property computation of area of segmented regions.

### Create plugin folder
First we have to create a folder for our plugin. Do so in the *plugins* folder of MAPHIS as mentioned in the previous section and inside create the files `plugin.py` and `__init__.py`. We will name the folder as `tutorial_plugin`.

### Filling out `plugin.py`
Next thing MAPHIS expects is to find some code inside the file `plugin.py`, see below.

```py linenums="1" title="maphis/plugins/tutorial_plugin/plugin.py"
from typing import Optional

from maphis.plugin_creation import Plugin, Info, State, action_info, region_computation, param_int, Photo, LabelImg, RegionComputation



@action_info(name='Tutorial', description='A demonstration of plugin creation.', group='General')
class Tutorial(Plugin):

    def __init__(self, state: State, info: Optional[Info] = None):
        super().__init__(state, info)

    @staticmethod
    @region_computation(name='Blue threshold',
                        description='Segments the photo based on thresholding the blue channel.',
                        group='Segmentation')
    def blue_threshold(comp: RegionComputation, photo: Photo, *args) -> List[LabelImg]:
        # get the pixel data from `photo`
        image: np.ndarray = photo.image

        # Threshold the blue channel and obtain binary mask.
        # We are interested in pixels that have blue values lower than the threshold.
        # Our plugin will work on photos with specimens photographed against a blue background.

        mask = image[:, :, 2] < 120

        # access the `Labels` LabelImg for storing regions. This is where we will store the segmentation.
        label_image: LabelImg = photo['Labels']

        # Get the label hierarchy for the `LabelImg`
        label_hierarchy = label_image.label_hierarchy

        # We will assign the segmented regions the code "1:0:0:0". However, this representation is mainly for
        # humans to be easy to interpret, internally we have to convert this code to the according integer label:
        region_label = label_hierarchy.label("1:0:0:0")

        # Now we can actually assign the regions pixel the corresponding label:
        # Where the mask is True, assign `region_label`, anywhere else assign the label 0
        label_image.label_image = np.where(mask, region_label, 0).astype(np.uint32)

        # return the label image in a list
        return [label_image]

```

As you can see, your `Tutorial` plugin class contains (besides the `__init__` method) one method called `blue_threshold`. The important piece of code is this:

```py linenums="14"
    @region_computation(name='Blue threshold',
                        description='Segments the photo based on thresholding the blue channel.',
                        group='Segmentation')
```

The usage of the [`@region_computation`](reference.md#maphis.common.action.region_computation) decorator tells MAPHIS that the method `blue_threshold` is the [`__call__`](reference.md#maphis.common.action.RegionComputation.__call__) method of [`RegionComputation`](reference.md#maphis.common.action.RegionComputation).

Notice that the documentation for the [`__call__`](reference.md#maphis.common.action.RegionComputation.__call__) method of [`RegionComputation`](reference.md#maphis.common.action.RegionComputation) does not specify instance of `RegionComputation` as the first parameter. However, as the `__call__` method is an instance method of `RegionComputation` it does take an instance of [`RegionComputation`](reference.md#maphis.common.action.RegionComputation) as its first parameter. Hence why our `blue_threshold` method also takes an instance of `RegionComputation` as its first parameter. This similarly applies in cases when you are implementing functions that should act as [`GeneralAction`](reference.md#maphis.common.action.GeneralAction) and [`PropertyComputation`](reference.md#maphis.common.action.PropertyComputation).


If you start MAPHIS now, you should find our *Blue threshold* computation in the *Segmentation and other* panel on the right, see image below.

![Our blue threshold plugin showing in the panel on top right.](../images/blue_threshold1.png "Our segmentation computation in the 'Segmentation and other' panel")

Let's hit **Apply** to run the computation and see the result below.

![Segmentation result from our segmentation computation](../images/blue_threshold2.PNG "Segmentation result from our segmentation computation")


As we can see, most of the specimen got segmented correctly, however there are some pixels that it missed and it also segmented the place where the two blue pieces of background overlap. Both of these errors are easily correctible by the use of interactive tools like the **Brush**.

### User parameter: threshold value
Our segmentation computation will not be much of a use if the intensity of the blue background changes from photo to photo, since the threshold value is hard-coded in the source code.
To provide a bit of flexibility, we can offer the user to choose the appropriate thresholding value in the form of a **user parameter**.
The user parameter we want to include in our computation will be an integer number and we can easily implement this with the usage of the [`@param_int`](reference.md#maphis.common.action.param_int) decorator like this:

``` py linenums="14" hl_lines="5 6 7 8 17"
    @staticmethod
    @region_computation(name='Blue threshold',
                        description='Segments the photo based on thresholding the blue channel.',
                        group='Segmentation')
    @param_int(name="Threshold value", 
               description="The value to treshold the blue channel against.",
               key="threshold_value", 
               default_value=120, min_value=0, max_value=255)
    def blue_threshold(comp: RegionComputation, photo: Photo, *args) -> List[LabelImg]:
        # get the pixel data from `photo`
        image: np.ndarray = photo.image

        # Threshold the blue channel and obtain binary mask.
        # We are interested in pixels that have blue values lower than the threshold.
        # Our plugin will work on photos with specimens photographed against a blue background.

        mask = image[:, :, 2] < comp.user_params_dict['threshold_value'].value
        ...

```

User parameter for threshold:

![Threshold user parameter](../images/blue_threshold_param.PNG)


### Other types of user parameters
Besides *integer* (decorator [`@param_int`](reference.md#maphis.common.action.param_int)) user parameters, you have the option to provide *boolean* ([`@param_bool`](reference.md#maphis.common.action.param_bool)) in the form of checkboxes or *text string* parameters ([`@param_string`](reference.md#maphis.common.action.param_string)) in the form of text fields.

## 'Perimeter' property

In addition to the simple blue channel thresholding operation, our plugin will also offer computation of perimeter for regions. This is a good oportunity for us to see how to handle `pixel` and `real` units.

Just how we marked the `blue_threshold` method with the `@region_computation` decorator, we will decorate the method for computing region perimeter with the [`@scalar_property_computation`](reference.md#maphis.common.action.scalar_property_computation) decorator.

We need to import a few more things first, so the import statement should look as follows:

```py linenums="1" hl_lines="4 5 6 7" title="maphis/plugins/tutorial_plugin/plugin.py"
from typing import List, Optional

import numpy as np
from skimage.measure import perimeter

from maphis.plugin_creation import Plugin, Info, State, action_info, region_computation, param_int, Photo, LabelImg, \
    RegionComputation, PropertyComputation, scalar_property_computation, ScalarValue, ureg, RegionsCache, RegionProperty
```

Here's a brief explanation of what we're importing:

- [`skimage.measure.perimeter`](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.perimeter) - a function for computing the perimeter of binary regions from the [`scikit-image`](https://scikit-image.org) library
- [`scalar_property_computation`](reference.md#maphis.common.action.scalar_property_computation) - the decorator that will turn our method into a proper implementation of [`PropertyComputation`](reference.md#maphis.common.action.PropertyComputation)
- [`ScalarValue`](reference.md#maphis.measurement.values.ScalarValue) - a representation of a scalar value with or without units
- [`ureg`](reference.md#maphis.measurement.values.ureg) - an instance of [`pint.UnitRegistry`](https://pint.readthedocs.io/en/stable/api/base.html#pint.UnitRegistry); it stores units and their definitions
- [`RegionsCache`](reference.md#maphis.common.regions_cache.RegionsCache) - stores [`Region`](reference.md#maphis.common.regions_cache.Region) objects of a segmentation; the regions are subregions of the segmentation
- [`RegionProperty`](reference.md#maphis.measurement.region_property.RegionProperty) - an object representing a computed property of a specific segmentation region. All `PropertyComputation`s return a list of `RegionProperty` from their `__call__` methods, and so will our `perimeter` method.

Now we get to the implementation of the the computation itself:

```py linenums="48" title="maphis/plugins/tutorial_plugin/plugin.py"
    @staticmethod
    @scalar_property_computation(name='Perimeter',
                                 description='Computes the perimeter of regions in pixels or real units.',
                                 group='Length & area measurements',
                                 export_target='Common',
                                 default_value=ScalarValue(ureg('0 px')))
    def perimeter(comp: PropertyComputation, photo: Photo, region_labels: List[int], regions_cache: RegionsCache, props: List[str]) -> List[RegionProperty]:
        computed_perimeters: List[RegionProperty] = []

        for region_label in region_labels:
            # if a region whose label is `region_label` is not present in this `photo`s segmentation, let's move on to
            # another `region_label` in `region_labels`
            if region_label not in regions_cache.regions:
                continue
            region: Region = regions_cache.regions[region_label]

            region_perimeter_px = ScalarValue(perimeter(region.mask) * ureg('px'))

            perimeter_property: RegionProperty = comp.example('perimeter')
            perimeter_property.label = region_label

            # if `photo` has a scale available, we convert the value in pixel units to real units
            if photo.image_scale is not None:
                perimeter_property.value = ScalarValue(region_perimeter_px / photo.image_scale)
            else:
                perimeter_property.value = region_perimeter_px

            computed_perimeters.append(perimeter_property)

        return computed_perimeters
```

The implementation is short and simple. 

- the `for` cycle at line 57 is what all `PropertyComputations` have in common - we iterate over all integer labels of regions that the user scheduled the computation for.
- if there is no region with `region_label` in the segmentation, we skip (lines 60-61) to another `region_label`
- we obtain a [`Region`](reference.md#maphis.common.regions_cache.Region) with `region_label` that is present in the segmentation by accessing it through the `RegionsCache` (line 62)
- Compute the perimeter of the region by calling the [`skimage.measure.perimeter`](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.perimeter) on the `mask` attribute of `region`. Immediately we construct a [`ScalarValue`](reference.md#maphis.measurement.values.ScalarValue) from the raw perimeter value (which is in pixels) and endow it with `pixel` units like so: 
```py 
perimeter(region.mask) * ureg('px')
```
- Next we need to prepare a `RegionProperty` instance that will store the perimeter `ScalarValue`. To obtain a properly set up instance of `RegionProperty` (with correct metadata needed by MAPHIS), we use the method `example` of the `comp` object. We just need to set the `label` attribute of the returned `RegionProperty` to `region_label` (lines 66-67).
- If `photo` has a scale value, we convert the pixel value of perimeter to real units and set the `value` attribute of `RegionProperty` (lines 70-71), otherwise we will store the `region_perimeter_px` value in the `value` attribute (line 73).
- Insert the `RegionProperty` to the list of computed perimeter properties that will get returned after all `region_label`s have been processed (line 75).
- Lastly, return the computed `RegionProperty` objects.

That's it to our 'Perimeter' property.

When implementing your own properties, you can provide user parameters to customize the behaviour. You can do it the same way as you do for `RegionComputation`s, see [here](#user-parameter-threshold-value) and [here](#other-types-of-user-parameters).