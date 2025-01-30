# Use an official PHP image with Apache
FROM php:8.2-apache

# Set non-interactive mode to prevent prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    mariadb-server \
    mariadb-client \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libzip-dev \
    unzip \
    git \
    curl \
    libonig-dev \
    && docker-php-ext-configure gd \
    && docker-php-ext-install pdo pdo_mysql mysqli gd zip

# Install Composer (latest version)
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Install Drush using Composer
RUN composer global require drush/drush
ENV PATH="/root/.composer/vendor/bin:${PATH}"

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Start MariaDB service when the container starts
CMD ["bash", "-c", "service mariadb start && apache2-foreground"]

# Set working directory
WORKDIR /var/www/html
