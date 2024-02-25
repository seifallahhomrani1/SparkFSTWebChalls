# Use an official PHP runtime as a parent image
FROM php:7.4-apache

# Set the working directory to /var/www/html
WORKDIR /var/www/html

# Copy the current directory contents into the container at /var/www/html
COPY . /var/www/html

# Install any necessary dependencies
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Secure the container
RUN a2enmod rewrite && \
    sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf && \
    chmod -R 755 /var/www/html && \
    chown -R www-data:www-data /var/www/html

# Set the flag
RUN FLAG_NAME=/tmp/flag && \
    echo "flag{EXAMPLE_FLAG}" > "$FLAG_NAME" && chown www-data:www-data "$FLAG_NAME"

# Expose port 80 for Apache
EXPOSE 80

# Start Apache in the foreground
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
