# references: https://aka.ms/vscode-docker-python
# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

EXPOSE 5000

# standard place to keep web server files
WORKDIR /workspace

#install poppler
RUN apt update -y && apt install -y poppler-utils

# Install pip requirements
COPY app/requirements.txt .
RUN python -m pip install -r requirements.txt

# copy rest of files
COPY . .

# Keeps Python from generating .pyc  files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

