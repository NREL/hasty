# syntax=docker/dockerfile:1
FROM python:3.8.1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /hasty
COPY requirements.txt /hasty/
RUN pip install -r requirements.txt
COPY . /hasty/
RUN pre-commit install
WORKDIR /hasty/hasty
ENTRYPOINT [ "./docker-entrypoint.sh" ]
