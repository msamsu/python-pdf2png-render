FROM python:3.10.0-buster

RUN pip install Django==3.2.9
RUN pip install django-extensions==3.1.5
RUN pip install djangorestframework==3.12.4
RUN pip install psycopg2-binary==2.9.2
RUN pip install celery==5.2.1
RUN pip install coverage==6.1.2

RUN apt update && apt install -y poppler-utils
RUN pip install pdf2image==1.16.0
RUN pip install pymupdf==1.19.2

RUN pip freeze

WORKDIR /code
COPY src /code
COPY environment/entrypoint.sh /

ENV PYTHONPATH $PYTHONPATH:/code/
ENV C_FORCE_ROOT 1

ENTRYPOINT /entrypoint.sh
