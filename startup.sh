#!/bin/bash

echo "Pip installing requirements.txt"
/usr/bin/pip3 install -r /app/requirements.txt --break-system-packages

cd /app
echo "Starting nginx server..."
/etc/init.d/nginx start

chown -R www-data:www-data /app

echo "Starting uwsgi server..."
uwsgi --ini homepage_api.ini
