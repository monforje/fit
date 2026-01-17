FROM jupyter/scipy-notebook:python-3.11.6

USER root

WORKDIR /home/jovyan

USER ${NB_UID}

RUN pip install --no-cache-dir \
    sqlalchemy==2.0.23 \
    psycopg2-binary==2.9.9 \
    python-dotenv==1.0.0

WORKDIR /home/jovyan/work
