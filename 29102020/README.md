# Notes for 29 October 2020

In todays meet up, we are going to focus on getting the [MIMIC-III_ICU_Readmission_Analysis](https://github.com/Jeffreylin0925/MIMIC-III_ICU_Readmission_Analysis) working. This involves reorganizing the code, making a few edits, and, optionally, reworking the provided scripts into Jupyter notebooks.

## Reorganizing  the Repository

The directory `mimic3benchmark` is a Python __package__. A package is a collection of Python __modules__. A module is a file that contains Python code, Python code that can be imported into your code.

### How does Python import modules?

When you execute a Python statement like

```Python
import math
```

Python searches your computer for a module named `math`. Where you computer searches is determined by a system variable named `PYTHONPATH`. The computer is searched in the order that directories are listed in `PYTHONPATH`. You can see the value of `PYTHONPATH` using the `sys` module:

```Python
import sys                                                       
sys.path                                                                
['/Users/brian/opt/anaconda3/bin',
 '/Users/brian/opt/anaconda3/lib/python38.zip',
 '/Users/brian/opt/anaconda3/lib/python3.8',
 '/Users/brian/opt/anaconda3/lib/python3.8/lib-dynload',
 '',
 '/Users/brian/opt/anaconda3/lib/python3.8/site-packages',
 '/Users/brian/opt/anaconda3/lib/python3.8/site-packages/aeosa',
 '/Users/brian/opt/anaconda3/lib/python3.8/site-packages/IPython/extensions',
 '/Users/brian/.ipython']
 ```
In the original repository, the developer instructs you to modify `PYTHONPATH` to add the location of the repository. In general, you don't need/want to mess with you `PYTHONPATH`. We will take advantage of the fact that the __current directory__ (represented by the empty string in `sys.path`) is always in the search path.

If we move the `mimic3benchmark` directory (package) into the `scripts` directory, then when we run the Python scripts located in `scripts` will find the `mimic3benchmark` code without having to modify the system variable.


### [Editing the code](./code_edits.md)
