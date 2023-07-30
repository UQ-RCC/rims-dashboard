FROM python:3.10.6@sha256:745efdfb7e4aac9a8422bd8c62d8bc35a693e8979a240d29677cb03e6aa91052
WORKDIR /app

RUN apt-get update && apt-get -y install \
    git \
    vim \    
    gcc

RUN pip install --upgrade pip

COPY . /app

RUN pip install -e /app

COPY data /app/data
COPY conf/ app/conf
#COPY . app/

CMD gunicorn --bind 0.0.0.0:8050 frontend.wsgi:server