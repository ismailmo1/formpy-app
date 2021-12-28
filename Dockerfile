# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:slim

# install opencv dependencies
RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development
ENV FLASK_SECRET=secret
ENV IMG_STORAGE_PATH=/static/image_storage/template_images
ENV DOCS_FOLDER_PATH=static/docs
# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
WORKDIR /app
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
