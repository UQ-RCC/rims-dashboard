#multi-stage
#1) build with node 16
#2) serve with nginx
#builder
FROM node:16 AS builder
WORKDIR /app

# Bundle app sources
COPY package.json vue.config.js babel.config.js yarn.lock .
COPY nginx nginx
COPY public public
COPY src src

RUN yarn install && yarn run build

#-----------------------------------------------
#server
FROM nginx:1.25
#FROM nginx:1.21.1-alpine
COPY --from=builder /app/dist/ /usr/share/nginx/html/
COPY --from=builder /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
#COPY --from=builder /app/nginx/dashboard.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD nginx -g "daemon off;"
#ENTRYPOINT ["nginx", "-g", "daemon off;"]
