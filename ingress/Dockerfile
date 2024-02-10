
#-----------------------------------------------
#server
FROM nginx:1.25

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD nginx -g "daemon off;"