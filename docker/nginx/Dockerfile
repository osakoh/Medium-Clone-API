# nginx image
FROM nginx:1.21.5-alpine
# remove default directory that came with image
RUN rm /etc/nginx/conf.d/default.conf

# replace remove directory: default.conf from host machine to nginx container
COPY ./default.conf /etc/nginx/conf.d/default.conf