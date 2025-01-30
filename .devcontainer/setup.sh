#!/bin/bash

# Exit on error
set -e

# Define database credentials
DB_NAME=drupal
DB_USER=root
DB_PASS=root

# Install MariaDB Server
echo "Installing MariaDB Server..."
export DEBIAN_FRONTEND=noninteractive
apt-get update && apt-get install -y mariadb-server

# Start MariaDB and create database
service mysql start
mysql -uroot -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
mysql -uroot -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
mysql -uroot -e "FLUSH PRIVILEGES;"

# Install latest Drupal
echo "Installing Drupal..."
rm -rf /var/www/html/*
composer create-project drupal/recommended-project /var/www/html
chown -R www-data:www-data /var/www/html

# Enable Apache Rewrite Module
a2enmod rewrite
service apache2 restart

# Create settings.php
cp /var/www/html/web/sites/default/default.settings.php /var/www/html/web/sites/default/settings.php
chmod 666 /var/www/html/web/sites/default/settings.php

echo "Drupal installation completed!"
