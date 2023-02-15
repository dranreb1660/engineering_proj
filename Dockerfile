# a Dockerfile specifies how to build a docker image
FROM python:3.9

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./fpl_engineering ./fpl_engineering
COPY ./artifacts ./artifacts
COPY ./models ./models
COPY ./server.py .
COPY ./api_logic.py .
# COPY ./.env .

ENTRYPOINT [ "python3" ]

CMD [ "server.py"]
