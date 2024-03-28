# Overview

This dashboard is a frontpage for UQ's Research Infrastructure Management System (RIMS), used to manage user and client projects within the University's research infrastructure labs, facilitating access to high-end instrumentation such as electron microscopes and mass-spectrometers. 

RIMS-dashboard is an internal tool providing up-to-date status information on users, projects, instruments and training requests to facility staff. It integrates data from university systems such as the 3rd-party SaaS management system, PPMS. 

The application is designed and developed by the Centre for Microscopy and Microanalysis (CMM) and the Research Computing Centre (RCC).

# Features

# Installation

The application is fully containerised, and can be easily stood up via docker-compose. 

```py
#clone
git clone git@github.com:UQ-RCC/rims-dashboard.git

cd rims-dashboard

#build
docker-compose -f docker-compose.prod.yml build

#start
docker-compose -f docker-compose.prod.yml up -d

#end
docker-compose -f docker-compose.prod.yml down -d

```

To correctly interface with the RIMS/PPMS system, the RIMS and keycloak config must be specified in backend/conf/rimsdash.conf. 

This must include a valid RIMS API key in "api2_key", and a valid keycloak server config and public key under the [keycloak] section. If needed, UQ facilities can contact UQ RCC to obtain these for their core.