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

# Initialize MariaDB data directory
echo "Initializing MariaDB..."
mkdir -p /var/lib/mysql
chown -R mysql:mysql /var/lib/mysql
mysql_install_db --user=mysql --datadir=/var/lib/mysql

# Start MariaDB
echo "Starting MariaDB..."
service mariadb start

# Secure the installation
echo "Configuring MariaDB..."
mysqladmin -u root password "$DB_PASS"

# Create Drupal database
echo "Creating Drupal database..."
mysql -uroot -p$DB_PASS -e "CREATE DATABASE IF NOT EXISTS $DB_NAME DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -uroot -p$DB_PASS -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"
mysql -uroot -p$DB_PASS -e "FLUSH PRIVILEGES;"

# Install latest Drupal
echo "Installing Drupal..."
rm -rf /var/www/html/*
composer create-project drupal/recommended-project /var/www/html
chown -R www-data:www-data /var/www/html

# Configure Apache
echo "Configuring Apache..."
cat > /etc/apache2/sites-available/000-default.conf << 'EOF'
<VirtualHost *:80>
    DocumentRoot /var/www/html/web
    <Directory /var/www/html/web>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF

# Enable Apache Rewrite Module
a2enmod rewrite
service apache2 restart

# Create settings.php and files directory
mkdir -p /var/www/html/web/sites/default/files
cp /var/www/html/web/sites/default/default.settings.php /var/www/html/web/sites/default/settings.php
chmod 666 /var/www/html/web/sites/default/settings.php
chmod 777 /var/www/html/web/sites/default/files

echo "Drupal installation completed!"