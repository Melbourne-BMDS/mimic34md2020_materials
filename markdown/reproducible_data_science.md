# (Trying to) Do Reproducible Computational Science

## What I'm Reading Now!

!["The Practic eof Reproducible Science"](https://images.ucpress.edu/covers/300/9780520294752.jpg)

## People I follow

- [Shirley Zhao: @zhao_shirley](https://twitter.com/zhao_shirley)
    - [Reproducible Science Course by Shirley](https://github.com/UUDeCART/reproducible_science)
- [Heather Piwowar: @researchremix](https://twitter.com/researchremix)

## Tools I Use

- [Docker](https://www.docker.com/)
    - Docker can be tricky on Windows Machines
        - Does your OS support virtualization
        - Windows vs Linux containers?
- [LaTex](https://www.ctan.org/)
- [Jupyter](https://jupyter.org/)
    - What is good, whatis bad about Jupyter notebooks?
    - [nbstripout](https://pypi.org/project/nbstripout/)
    - [jupytext](https://jupytext.readthedocs.io/en/latest/formats.html)
    - [nbdime](https://nbdime.readthedocs.io/en/latest/)
    
## Electronic Notebooks

## Data Version Control

I don't know what the best solution is yet, but...

- [Pachyderm](https://www.pachyderm.com/)
- [DVC](https://dvc.org/)
- [Girder](https://girder.readthedocs.io/en/stable/)

## Key excerpts from _The Practice of Reproducible Science_

> A research projet is computationally reproducible if a second investigator (including you in the future) can re-create the final reported results of the project, including key quantitative findings, tables, and figures, given only a set of files, and written instructions (_The Practice of Reproducible Research_, p. xxii)

>A crucial component of the chain of evidence is the software used to process and analyze the data. Modern data analysis typically involves dozens, if not hundreds of steps, each of whcih can be performed by numerous algorithms that are nominally identical but differ in detail, and each of which involves at least some ad hoc choices. (_The Practice of Reproducible Research_, p. xix)

>Using point-and-click tools, rather than scripted analysses, makes it easier to commit errors and harder to find them. One recent calamity attributable in part to poor computational practice is the work of Reinhart and Rogoff (2010), which was used to justify econoic austerity measures in sothern Europe. Errors in their Excel spreadsheet led to the wrong conclusion (herndon et al., 2014). If they had scripted their analysis and tested the code instead of using spreadsheet software, their errors might have been avoided, discovered, aor corrected before harm was done. (_The Practice of Reproducible Research_, p. xix)

## "Three Key Practices" (_The Practice of Reproducible Research_, p. 20)

1. Clearly separate, label, and document all data, files, and operations taht occur on data and files.
1. Document all operations fully, automating them as much as possible, and avoiding manual intervention in the workflow when feasible.
1. Design a workflow as a sequence of small steps that are glued together, with intermediate outputs from one step feeding into the next step as inputs. 

## What version of software did you use?

- `pip freeze`
- `conda env create -f environment.yml`
