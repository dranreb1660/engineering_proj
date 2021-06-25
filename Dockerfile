# a Dockerfile specifies how to build a docker image
FROM continuumio/anaconda3:latest

ADD . /code
WORKDIR /code


ENTRYPOINT [ "python", "fantasy.py" ]

