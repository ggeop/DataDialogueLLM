#!/bin/bash
set -e

# Unzip the dummy data
unzip /docker-entrypoint-initdb.d/dvdrental.zip -d /tmp/dvdrental

# Extract the tar file
tar -xvf /tmp/dvdrental/*.tar -C /tmp/dvdrental

# Wait for the PostgreSQL server to start
until pg_isready; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Load the data into the database using pg_restore
echo "Loading data from tar file"
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v /tmp/dvdrental/*.tar

# Clean up
rm -rf /tmp/dvdrental