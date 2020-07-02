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
    vega=2.5.0 \
    altair=4.1.0=py_1 \
    psycopg2 && \
    conda clean -afy

RUN  conda install -c pyviz hvplot && conda clean -afy


RUN jupyter labextension install @pyviz/jupyterlab_pyviz @jupyterlab/vega5-extension@2.1.0

RUN pip install pycontextnlp \
    radnlp \
    nbgitpuller \
    spacy==2.2.2 \
    cycontext \
    clinical-sectionizer==0.1.2 \
    medspacy==0.0.1 \
    https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz \
    https://github.com/abchapman93/spacy_models/raw/master/releases/en_info_3700_i2b2_2012-0.1.0/dist/en_info_3700_i2b2_2012-0.1.0.tar.gz \
    nlpre \
    markdown \
    clipspy \
    durable_rules \
    wfdb \
    entrezpy \
    pymongo \
    kanren \
    pymysql \
    tinydb \
    ibis-framework[postgres,bigquery,sqlite,mysql] \
    gensim==3.8.3


WORKDIR /home/jovyan

CMD ["start-notebook.sh"]
