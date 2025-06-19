FROM mysql:8.0

# Copy custom MySQL configuration if needed
COPY services/mysql/my.cnf /etc/mysql/conf.d/

# Copy initialization scripts
COPY services/mysql/init.sql /docker-entrypoint-initdb.d/

# Set default authentication plugin
CMD ["mysqld", "--default-authentication-plugin=mysql_native_password"] 