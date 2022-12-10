# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.8-slim-buster
WORKDIR /app

RUN apt update && apt install -y python3 iputils-ping

COPY . .

ENV host ya.ru
CMD ["sh", "-c", "python3 main.py ${host}"]