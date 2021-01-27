# Creating Custom Environments with Conda

The authors of the PLOS One paper tell us that their software depends on the following packages:

1. numpy
1. pandas
1. Keras
1. scikit_learn

Package dependency is a major challenge with software and Python has a long history of doing a pretty poor job at it! Anaconda (and conda) largely arose because of the inadequacies in native Python package management.

What do we mean by package dependency? In a nutshell it is this: instead of writing all of our code from scratch using our language of choice (e.g. Python) we are going to use code that someone else has already written (e.g. Pandas) to solve some of what we need our program to do and then write the rest ourselves.

If all the packages we were going to use were written entirely in Python, this would not be particularly challenging. However, often these packages are not written just in Python but are written in C/C++ or Fortran. And the problem here is that Code written in C or Fortran for one type of computer will not necessarily run on another type of computer. So without going into more detail, let's just leave it at: package management is a problem and conda tries to solve that problem.

## What are our package dependencies in detail?

The authors list four dependencies

1. `numpy`: a package for working with large arrays of data
1. `pandas`: a large, complex package for working with tabular data
1. `Keras`: a package for creating deep neural networks (deep learning)
1. `scikit-learn`: a package for doing machine learning

In reality each of these packages depends on other packages not listed and the authors of these packages should have described these dependencies in such a way that when `conda` (or `pip` described later) is installed it installs all the dependencies correctly.

`pandas`, `keras`, and `scikit-learn` all depend on `numpy` so we are probably smarter not to specify `numpy` as a dependency and let `conda` figure out that it needs to install `numpy`? The fact that all of these packages depend on `numpy` is getting to the heart of one of the package management challenges: particular versions of `keras`, `scikit-learn`, and `pandas` may all require different versions of `numpy`. So one task `conda` has, a task that sometimes is quite slow, is figuring out which versions of all the packages need to be installed so that everything we want can in fact be installed.

We are going to specify our Python environment by creating an `environment.yml` file. This is a [YAML](https://yaml.org/) file and we will use it to specify what version of Python, pandas, etc. we will be using.

Here is an example `environment.yml` file for a [simple project](https://github.com/Melbourne-BMDS/signal_detection_theory) I created for one of my classes.

```Yaml
name: mbmds-sdt
channels:
  - defaults
dependencies:
  - python=3.7
  - numpy
  - pandas
  - pip
  - matplotlib
  - seaborn
  - jinja2
  - ipywidgets
  - ipython
  - pip:
    - RISE
```

Here is the basic structure analyzed:

1. __name__: This is going to be the name of the Python environment.
1. __channels__: `conda` has different channels that can be searched for packages
1. __dependencies__: These are the packages we are going to tell `conda` to install. Note that one of the packages we are installing is `pip` which is the default (standard) way of installing packages in Python.
1. __pip__: Not every package we want to install is going to be available with `conda`, so we will use `pip` to install these other packages, which in this case is `RISE`

## Create an `environment.yml` file

Go back to your JupyterLab instance in your browser and from the Launcher create a new text file in the top level directory for the `MIMIC-III-ICU_Readmission_Analysis` repository.

![Create a text file](media/launcher_text.png)

Rename the file `environment.yml`

![Rename a file](media/rename_file.png)

I went to anaconda.org and searched for each of the following packages to see what channels they were in and what the latest versions of the packages were. `keras` is only available in the `conda-forge` (community contributed packages). `Pandas` and `scikit-learn` are available in the default channel (the channel currated by the Anaconda team). The `conda` developers recommend not mixing channels, so we will stick with the `conda-forge` channel. In addition to the software listed as dependencies, I also want to add `seaborn` for making graphs, `jupyterlab` so we can use the environment we are used to and `plaidml`. `plaidml` is not available on `conda` so we will need to install `pip` and use `pip` to install `plaidml`. `plaidml` allows packages like `keras` to use non-NVidia gpus, such as those on Mac computers.

Based on the latest available versions, I created the following `environment.yml` file:

```Yaml
name: mimic3
channels:
  - conda-forge
dependencies:
  - python=3.7
  - pandas=1.1.*
  - keras=2.4.*
  - scikit-learn=0.23.*
  - pip=20.2.*
  - seaborn=0.11.*
  - jupyterlab=2.2.*
  - pip:
    - plaidml==0.7.*
```

__Note__: `conda` uses a single `=` when specifying a version while `pip` uses a double `==`.

To create the environment, in the bash shell I execute the following command from the directory containing `environment.yml`:

```bash
conda env create -f environment.yml
```



__It failed!__

One obvious problem is `pip`. I don't really care what version of `pip` I'm using, so I'm not going to specify the version for `pip` and retry.

__It failed again!__

So I'm going to get rid of all the version numbers and see if conda can manage to create an environment with all the desired software.

__Note__: The repository we cloned is two years old, so they certainly didn't use the latest version anyway. We might need to edit their code or specify older package versions to get everything working anyway.

```Yaml
name: mimic3
channels:
  - conda-forge
dependencies:
  - python=3.7
  - pandas
  - keras
  - scikit-learn
  - pip
  - seaborn
  - jupyterlab
  - pip:
    - plaidml
```

__Now it worked!!__ We can specify versions later when we have verified that all of our code works.
