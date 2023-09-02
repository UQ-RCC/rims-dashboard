#!/bin/bash
#manual test script for frontend->backend mimicking browser options

#get only

#curl -i http://127.0.0.1:5000/api/v1/userlist 

#curl -i -X GET -H "Origin:  http://localhost:8080" \
#    -H 'Access-Control-Request-Method: GET' \
#    -H 'Access-Control-Request-Headers: Content-Type, Authorization' \
#    http://127.0.0.1:5000/api/v1/userlist


#get with params

#curl -i http://127.0.0.1:5000/api/v1/state?login=myusername

curl -i -X GET -H "Origin:  http://localhost:8080" \
    -H 'Access-Control-Request-Method: GET' \
    -H 'Access-Control-Request-Headers: Content-Type, Authorization' \
    http://127.0.0.1:5000/api/v1/state?login=myusername