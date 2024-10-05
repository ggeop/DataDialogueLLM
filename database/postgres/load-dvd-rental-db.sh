#!/bin/bash
set -e
set -x  # Enable verbose logging

echo "Starting init-db.sh script"

# Unzip the dummy data
unzip /docker-entrypoint-initdb.d/dvdrental.zip -d /tmp/dvdrental

# Extract the tar file
tar -xvf /tmp/dvdrental/*.tar -C /tmp/dvdrental

# Wait for the PostgreSQL server to start
until PGPASSWORD=$POSTGRES_PASSWORD psql -h localhost -U "$POSTGRES_USER" -d postgres -c '\q'; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Function to run SQL commands
run_sql() {
  PGPASSWORD=$POSTGRES_PASSWORD psql -h localhost -U "$POSTGRES_USER" -d postgres -c "$1"
}

# Disconnect all active connections to the dvdrental database
echo "Disconnecting active connections to dvdrental database"
run_sql "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'dvdrental' AND pid <> pg_backend_pid();"

# Drop the dvdrental database if it exists
echo "Dropping dvdrental database if it exists"
run_sql "DROP DATABASE IF EXISTS dvdrental;"

# Create the dvdrental database
echo "Creating dvdrental database"
run_sql "CREATE DATABASE dvdrental;"

if [ $? -ne 0 ]; then
  echo "Failed to create dvdrental database"
  exit 1
fi

# Load the data into the database using pg_restore
echo "Loading data from tar file into dvdrental database"
if PGPASSWORD=$POSTGRES_PASSWORD pg_restore -h localhost -U "$POSTGRES_USER" -d dvdrental -v --no-owner --role="$POSTGRES_USER" /tmp/dvdrental/*.tar; then
  echo "Database restore completed successfully"
else
  echo "Error: Database restore failed"
  exit 1
fi

# Verify the restoration
echo "Verifying database restoration"
PGPASSWORD=$POSTGRES_PASSWORD psql -h localhost -U "$POSTGRES_USER" -d dvdrental -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

if [ $? -ne 0 ]; then
  echo "Failed to verify database restoration"
  exit 1
fi

# Clean up
rm -rf /tmp/dvdrental

echo "Database load data completed"