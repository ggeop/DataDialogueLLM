FROM mysql:8.0

# Copy the SQL files
COPY sakila-db/sakila-schema.sql /docker-entrypoint-initdb.d/1-sakila-schema.sql
COPY sakila-db/sakila-data.sql /docker-entrypoint-initdb.d/2-sakila-data.sql

# Install dos2unix using microdnf (Oracle Linux package manager)
RUN microdnf install -y dos2unix && \
    dos2unix /docker-entrypoint-initdb.d/1-sakila-schema.sql && \
    dos2unix /docker-entrypoint-initdb.d/2-sakila-data.sql && \
    microdnf clean all