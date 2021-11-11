FROM python:3.8.1
USER root
ENV PYTHONUNBUFFERRED=1
WORKDIR /hasty

COPY . /hasty/

RUN pip install -r requirements.txt
RUN pre-commit install
RUN tox
WORKDIR /hasty/hasty
RUN python manage.py makemigrations
RUN python manage.py migrate --run-syncdb

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
