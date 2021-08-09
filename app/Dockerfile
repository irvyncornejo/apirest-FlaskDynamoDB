FROM python:3.8.8-buster

RUN pip3 install --upgrade pip

USER root

WORKDIR /app

COPY . /app

# add credentials
RUN mkdir -p /app/${USER}/.aws
COPY aws/credentials /app/${USER}/.aws

RUN pip3 --no-cache-dir install -r requirements.txt
CMD ["python3", "main.py"]
