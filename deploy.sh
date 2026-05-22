#!/bin/bash

cd /var/www/niemiecki-z-ania

source venv/bin/activate

git pull

python manage.py migrate

python manage.py collectstatic --noinput

systemctl restart niemieckizania

echo "Deploy zakonczony 🚀"
