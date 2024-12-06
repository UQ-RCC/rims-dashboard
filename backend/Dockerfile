FROM python:3.10
WORKDIR /app

#set up the container
RUN apt-get update && apt-get -y install gcc

RUN pip install --upgrade pip

#copy and install requirements separately, to cache them for subsequent builds
COPY setup.cfg .
COPY pyproject.toml .
COPY rimsdash rimsdash
COPY conf/rimsdash.conf.example conf/rimsdash.conf
RUN pip install .

#entrypoint
CMD uvicorn rimsdash.main:app --host 0.0.0.0 --port 5000
