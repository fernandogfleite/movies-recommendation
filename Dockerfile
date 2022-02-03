FROM python:3.10.1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ./movie_recomendation /movie_recomendation
COPY  ./.env /.env
COPY ./movies-csv /movies-csv
COPY ./templates /templates
COPY ./static /static
COPY ./manage.py /manage.py