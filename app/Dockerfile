# references: https://aka.ms/vscode-docker-python
# https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
FROM python:slim

EXPOSE 5000

# standard place to keep web server files
WORKDIR /var/www/

#install poppler
RUN apt update -y && apt install -y poppler-utils

# Install pip requirements
COPY requirements.txt /var/www/
RUN python -m pip install -r requirements.txt

# copy rest of files
COPY . /var/www/

# Keeps Python from generating .pyc  files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


# Creates a non-root user with an explicit UID and adds permission to access the var/www folder
# so attacker doesnt have root access if they break out of container
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /var/www
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi"]
