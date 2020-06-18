FROM jupyter/scipy-notebook:2c0af4ab516b

MAINTAINER chapmanbe <brian.chapman@unimelb.edu.au>
USER root

# RUN apt-get update && apt-get upgrade -y && apt-get install -y \
#      graphviz\
#      locales-all \
#      vim \
#  && rm -rf /var/lib/apt/lists/*

WORKDIR /home/jovyan

USER jovyan

run conda install -y -c conda-forge \
    pyarrow=0.17.* \
    spacy=2.2.3 \
    psycopg2 && \
    conda clean -afy

RUN  conda install -c pyviz hvplot && conda clean -afy


RUN jupyter labextension install @pyviz/jupyterlab_pyviz

RUN pip install pycontextnlp \
    radnlp \
    nbgitpuller \
    clinical-sectionizer \
    nlpre \
    cycontext \
    markdown \
    clipspy \
    durable_rules \
    wfdb \
    entrezpy \
    pymongo \
    kanren \
    ibis-framework[postgres,bigquery]

RUN pip install git+https://github.com/chapmanbe/dminteract#egg=dminteract

WORKDIR /home/jovyan

CMD ["start-notebook.sh"]
