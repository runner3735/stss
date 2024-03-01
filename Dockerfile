FROM python:3.9.13-slim-bullseye

# create non-root user
RUN groupadd --gid 1000 app \
&& useradd --uid 1000 --gid 1000 -m app

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# install dependencies debian
RUN apt-get update
RUN apt-get install -y --no-install-recommends ffmpeg
RUN apt-get install -y --no-install-recommends mediainfo
RUN apt-get install -y --no-install-recommends ghostscript

# install dependencies python
RUN pip install --upgrade pip \
&& pip install Django==3.2.15 \
&& pip install django-widget-tweaks==1.4.12 \
&& pip install django-imagekit==4.1.0 \
&& pip install gunicorn==20.1.0 \
&& pip install ghostscript==0.7 \
&& pip install Pillow==9.2.0
RUN pip install psycopg2-binary
RUN pip install yt-dlp
RUN pip install pillow-heif

# set default user
USER app

