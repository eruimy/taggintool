# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /taggintool

COPY requirements.txt /taggintool
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000
ENV FLASK_APP=flaskapp.py

CMD  ["flask", "run", "--host", "0.0.0.0"]