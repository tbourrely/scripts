sudo apt-get update
sudo apt-get install nginx mysql-server php5-fpm php5-mysql phpmyadmin
sudo ufw allow 'Nginx HTTP'
sudo mysql_secure_installation