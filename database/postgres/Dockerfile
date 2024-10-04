FROM postgres:13

# Install unzip
RUN apt-get update && apt-get install -y unzip

# Copy the zip file into the container
COPY dvdrental.zip /docker-entrypoint-initdb.d/

# Copy the initialization script
COPY init-db.sh /docker-entrypoint-initdb.d/

# Make sure the script is executable
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh