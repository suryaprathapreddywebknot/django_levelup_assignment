FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y librdkafka-dev
RUN apt-get update && apt-get -y install cron

WORKDIR /app


ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app
