# pull the official base image
FROM python:latest

# set work directory
WORKDIR /home/app/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y cron

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /home/app/web
RUN pip install -r requirements.txt

# copy project
COPY . /home/app/web

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]






