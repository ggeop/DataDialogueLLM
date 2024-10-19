FROM postgres:13

# Install unzip
RUN apt-get update && apt-get install -y unzip dos2unix

# Copy the sample database zip file and load script
COPY dvdrental.zip /docker-entrypoint-initdb.d/dvdrental.zip
COPY load-dvd-rental-db.sh /docker-entrypoint-initdb.d/load-dvd-rental-db.sh


# Convert potential CRLF to LF and make the script executable
RUN dos2unix /docker-entrypoint-initdb.d/load-dvd-rental-db.sh && \
    chmod +x /docker-entrypoint-initdb.d/load-dvd-rental-db.sh

# Make sure the script is executable
RUN chmod +x /docker-entrypoint-initdb.d/load-dvd-rental-db.sh