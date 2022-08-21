# postgres image
FROM postgres:14.1

#copy maintenace folder
COPY ./docker/local/postgres/maintenance /usr/local/bin/maintenance

# grant permission to all scripts in maintenace folder
RUN chmod +x /usr/local/bin/maintenance/*
# move contents of maintenace folder to the bin folder in the postgres container; then remove the maintenance directory
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
   && rmdir /usr/local/bin/maintenance