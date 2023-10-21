# Introduction

MAPHIS is a GPL open-source application that allows you to automatically or manually perform hierarchical segmentation of arthropod photos, and to extract various measurements describing the size, shape, colour, or texture properties of their individual body parts.

The application is not limited only to arthropod photos. With a different segmentation plugin or using manual editing, even photos from completely unrelated domains can be processed.

![The main window of MAPHIS](images/user_guide/Application1.png "The main window of MAPHIS")
 

## Installing and running on Windows
For Windows users we provide a convenient distribution package at: [https://cbia.fi.muni.cz/files/software/maphis/maphis.zip](https://cbia.fi.muni.cz/files/software/maphis/maphis.zip). 
Extract the contents of the downloaded zip-file at a destination of your choosing and run `MAPHIS` by executing the file `maphis.exe` inside the extracted folder.

**NOTE**: This way of obtaining and running `MAPHIS` is the most convenient. However, because of the way the distribution is generated, you may encounter that `MAPHIS` freezes when clicking on labels in the *Labels* tree view (it does not happen on all machines, though). As far as we know this problem is not `MAPHIS`-specific and is currently out of our hands, and therefore if you do encounter such a problem, we recommend looking at the alternative ways of installing `MAPHIS` detailed in the sections below.

---

## Alternative ways of installing `MAPHIS`
The next two sections detail how to install `MAPHIS` either through the `Python Package Index` or `git`. The required prerequisite for both of these ways is to have the `Python` interpreter installed. You can obtain `Python` from [https://www.python.org/](https://www.python.org/). `MAPHIS` is compatible with `Python` versions `3.8` or later, however it was developed and extensively tested mainly with `Python 3.8`.

### Virtual environment
As `MAPHIS` contains a few dependencies, their versions might clash with versions of the same dependencies that you already may have installed in your `Python environment`. To prevent this, we recommend installing `MAPHIS` (and it is generally a good practice for other big projects) in its own `virtual environment` (see [https://realpython.com/python-virtual-environments-a-primer/#why-do-you-need-virtual-environments](https://realpython.com/python-virtual-environments-a-primer/#why-do-you-need-virtual-environments) for further explanation).

The steps below describe how to create a virtual environment using the `miniconda` manager. Virtual environment management can be also achieved with the modules `venv` ([https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)) or `virtualenv` ([https://virtualenv.pypa.io/en/latest/](https://virtualenv.pypa.io/en/latest/)).

1. Download and install `miniconda` for your operating system from [https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

2. Open up `Anaconda Powershell Prompt` or `Anaconda Prompt` (Windows) or your terminal emulator (Linux).

3. In the prompt, create a new virtual environment called `maphis` with Python 3.8 (you can change the version in `python=3.8` as you like, it should be 3.8 or higher, though): `conda create -n maphis python=3.8`



### Alternative 1: Installing from PyPI and running from command line (Linux, Windows)
In this section we describe how to obtain `MAPHIS` from the `Python Package Index `(PyPI).

<!-- 1. ### Prerequisites
    In this guide, we will detail how to obtain Python 3.8 and create a Python virtual environment using the `miniconda` manager ([https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)).
    
    > &#128221; **Note:** <br/>Alternatively, you can also obtain Python 3.8 by downloading it directly (from [https://www.python.org/downloads/](https://www.python.org/downloads/)) or by using `pyenv` ([https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)). Virtual environment management can be also achieved with the modules `venv` ([https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)) or `virtualenv` ([https://virtualenv.pypa.io/en/latest/](https://virtualenv.pypa.io/en/latest/)).

    ** Set up Python 3.8 and virtual environment **
    
    1. Download and install `miniconda` for your operating system from [https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).
    
    2. Open up `Anaconda Powershell Prompt` or `Anaconda Prompt` (Windows) or your terminal emulator (Linux).
    
    3. In the prompt, create a new virtual environment called `maphis` with Python 3.8 as its interpreter: `conda create -n maphis python=3.8` -->
    

#### Installation
1. Activate the virtual environment: `conda activate maphis`
2. Install the app: `python -m pip install maphis`

#### Running

1. Activate the virtual environment: `conda activate maphis`
2. Start `MAPHIS` like so: `python -m maphis`
    
---

### Alternative 2: For developers - cloning the `git` repository

#### Installation

1. Clone the repository from [https://gitlab.fi.muni.cz/cbia/maphis](https://gitlab.fi.muni.cz/cbia/maphis)
2. Go to the root directory of the cloned repository
3. Activate the virtual environment: `conda activate maphis`
4. Install the requirements: `python -m pip install -r requirements.txt`
5. Install the app in editable mode: `python -m pip install -e .`
    
#### Running

1. Activate the virtual environment: `conda activate maphis`
2. Go to the root directory of the cloned repository
3. Run: `python maphis/__main__.py`

Or you can alternatively run `MAPHIS` with `python -m maphis` after *Step 1*.

