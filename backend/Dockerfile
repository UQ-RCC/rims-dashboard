FROM python:3.10.6@sha256:745efdfb7e4aac9a8422bd8c62d8bc35a693e8979a240d29677cb03e6aa91052
WORKDIR /app

#set up the container
RUN apt-get update && apt-get -y install \
    vim \    
    gcc

RUN pip install --upgrade pip

#copy and install requirements separately, to cache them for subsequent builds
COPY ./setup.cfg /app
COPY ./pyproject.toml /app
RUN pip install /app

#now copy and install the actual app
COPY . /app
RUN pip install /app

#copy any extra data, configs etc
COPY conf/ app/conf

#entrypoint
CMD uvicorn rimsdash.main:app --host 0.0.0.0 --port 5000