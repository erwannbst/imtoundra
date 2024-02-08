# Use the official PostgreSQL image as the base image
FROM postgres:16

# Set environment variables
ENV POSTGRES_USER toundra
ENV POSTGRES_PASSWORD toundra123
ENV POSTGRES_DB observations

# Copy the SQL script to the container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432
