#!/bin/bash

set -e

echo "Pip installing requirements.txt"
pip3 install -r /workspace/src/requirements.txt --break-system-packages

cd /workspace/src
echo "Starting nginx server..."
/etc/init.d/nginx start

chown -R www-data:www-data /workspace/src

echo "Starting uwsgi server..."
uwsgi --ini homepage_api.ini
