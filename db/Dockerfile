# db/Dockerfile

# pull base image from DockerHub
FROM mongo:latest
# Define mountable directories.
VOLUME ["/db/data"]
# create container working directory
WORKDIR /data/db
# Expose ports
EXPOSE 27017
EXPOSE 28017