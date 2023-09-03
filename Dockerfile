FROM python:3.11-alpine3.17

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./Backend /Backend
RUN pip install --upgrade pip && pip install -r Backend/requirements.txt

COPY ./TelegramBot /TelegramBot
RUN pip install -r TelegramBot/requirements.txt
