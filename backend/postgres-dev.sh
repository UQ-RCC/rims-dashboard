#!/bin/bash

CONF_FILE='./conf/rimsdash.conf'
DB_VOLUME="rdb_postgres_data3"

db_name=$(awk -F "=" '/db_name/ {print $2}' $CONF_FILE | tr -d ' ' )
db_username=$(awk -F "=" '/db_username/ {print $2}' $CONF_FILE | tr -d ' ' )
db_pw=$(awk -F "=" '/db_password/ {print $2}' $CONF_FILE | tr -d ' ' )

docker run --rm -e POSTGRES_DB=$db_name -e POSTGRES_USER=$db_username -e POSTGRES_PASSWORD=$db_pw -v $DB_VOLUME:/var/lib/postgresql/data/ -p mydbport:mydbport postgres:12
