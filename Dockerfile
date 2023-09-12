### BASE STAGE ###
FROM python:3.8.18-slim-bullseye AS base-stage
# Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN mkdir /app && adduser -u 1000 --disabled-password --gecos "" appuser && chown -R appuser /app
RUN --mount=type=cache,target=/var/cache/apt apt-get update -y 

USER appuser
# Install pip requirements
WORKDIR /home/appuser
RUN --mount=type=cache,target=/home/appuser/.cache/pip,uid=1000,gid=1000 python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN --mount=type=cache,target=/home/appuser/.cache/pip,uid=1000,gid=1000 python3 -m pip install -r requirements.txt

# Copy code
COPY . /app
WORKDIR /app
EXPOSE 5000
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENV PATH=$PATH:/home/appuser/.local/bin
CMD ["python3", "app.py"]
