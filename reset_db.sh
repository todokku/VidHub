#!/bin/bash

mysql -u vidhub -p -e 'drop database vidhub; create database vidhub;' || exit 1
rm -v streamer/migrations/0001_initial.py || exit 1
mv -v streamer/migrations/*_vidhub_*.py ./ || exit 1

./manage.py makemigrations || exit 1

mv -v *_vidhub_*.py streamer/migrations/ || exit 1

./manage.py migrate || exit 1