FROM python:3.10.6@sha256:745efdfb7e4aac9a8422bd8c62d8bc35a693e8979a240d29677cb03e6aa91052
WORKDIR /app

RUN apk update
RUN apk add --no-cache --virtual .build-deps \
    gcc
#    python3-dev \
#    musl-dev \
#    postgresql-dev 
    
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py install