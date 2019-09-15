FROM python:3.7-slim-buster

RUN apt-get update && \
    apt-get install python-pip -y && \
    apt-get clean


ADD requirements.txt /jaap/
# Set the working directory to /app
WORKDIR /jaap
# Copy the current directory contents into the container at /app
COPY . /jaap


RUN pip install -r requirements.txt

ADD . /jaap


RUN ls -all

CMD python __main__.py