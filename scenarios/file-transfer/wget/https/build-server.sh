#!/bin/bash

# Generate the ssh keys
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/self-signed.key -out /etc/nginx/self-signed.crt -subj "/C=US/ST=Maryland/L=Silver Spring/O=Organization/CN=example.com"


# Update the nginx config
echo "
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;

    keepalive_timeout  65;

    server {
        listen 443 ssl;
        server_name your_domain.com;

        ssl_certificate /etc/nginx/self-signed.crt;
        ssl_certificate_key /etc/nginx/self-signed.key;

        location / {
            root /var/www/html;
            index index.html;
        }
    }
}" | sudo tee /etc/nginx/nginx.conf


# Generate a large random data file for nginx to serve
dd if=/dev/urandom of=rand-file bs=1M count=10000
sudo mv -f rand-file /var/www/html/index.html


# Restart nginx
sudo systemctl restart nginx


# Fix firewall permissions
sudo ufw allow 'Nginx Full'

