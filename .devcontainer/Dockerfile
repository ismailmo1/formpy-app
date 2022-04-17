# references: https://aka.ms/vscode-docker-python
# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
FROM python:slim

EXPOSE 5000


#install poppler
RUN apt update -y && apt install -y poppler-utils

# Install pip requirements
COPY app/requirements.txt .
RUN python -m pip install -r requirements.txt

# copy flask app files
COPY app/ .

# Keeps Python from generating .pyc  files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG="True"
ENV FLASK_PORT=5000
ENV FLASK_ENV="production"
ENV IMG_STORAGE_PATH=/static/image_storage/template_images
ENV DOCS_FOLDER_PATH=static/docs
ENV MONGODB_HOSTNAME=mongodb
ENV MONGODB_DATABASE=formpydb
