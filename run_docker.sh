#!/bin/bash

IMAGENAME='rimsdash:0.1'

docker run -p 8050:8050 "$IMAGENAME"


#gunicorn --bind 0.0.0.0:8050 app:server

#not working on 127.0.0.1:8050
#cf.    https://docs.docker.com/network/links/
#       https://docs.docker.com/engine/reference/commandline/run/#publish
#       https://dash.plotly.com/deployment
#       https://towardsdatascience.com/dockerize-your-dash-app-1e155dd1cea3