# Use the official MySQL image from the Docker Hub
FROM mysql:latest

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=mydatabase
ENV MYSQL_USER=myuser
ENV MYSQL_PASSWORD=mypassword

# Expose the MySQL port
EXPOSE 3306

# Add custom configuration file if needed (optional)
# COPY my-custom.cnf /etc/mysql/conf.d/

# Initialize MySQL database (optional)
# COPY init-db.sql /docker-entrypoint-initdb.d/

# Command to start MySQL
CMD ["mysqld"]
