FROM python:3.8-slim-buster

WORKDIR /app

RUN mkdir /app/backups && mkdir /app/logs && mkdir /app/data

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV MINECRAFT_BACKUP_FILE_ENDING=.tgz
ARG BACKUP_SERVER_PORT=6783
ENV BACKUP_SERVER_PORT=${BACKUP_SERVER_PORT}
ENV LOG_MAX_BYTES=50000
ENV MINECRAFT_BACKUP_FILE_ENDING=.tgz

COPY . .
EXPOSE ${BACKUP_SERVER_PORT}

CMD [ "python3", "server.py"]