# pull the official base image
FROM python:3.12.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# для работы weasyprint
RUN apk add py3-pip so:libgobject-2.0.so.0 so:libpango-1.0.so.0 so:libharfbuzz.so.0 so:libharfbuzz-subset.so.0 so:libfontconfig.so.1 so:libpangoft2-1.0.so.0
RUN apk add gcc musl-dev python3-dev zlib-dev jpeg-dev openjpeg-dev libwebp-dev g++ libffi-dev
RUN apk --update --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font \
   && fc-cache -f \
   && fc-list | sort

# copy project
COPY . /usr/src/app


