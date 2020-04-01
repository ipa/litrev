FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/app
RUN mkdir -p /opt/db/data
RUN mkdir -p /opt/db/backup
WORKDIR /opt/app

# install depenencies
RUN apt-get update
RUN apt-get install -y vim supervisor

COPY . /opt/app
COPY ./conf/celery.conf /etc/supervisor/conf.d/celery.conf

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# create empty database
RUN python manage.py migrate
RUN python manage.py initadmin
