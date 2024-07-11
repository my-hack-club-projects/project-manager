#!/bin/bash

# Find the root of the project
gitroot=$(git rev-parse --show-toplevel)

cd "$gitroot/frontend"
# Build frontend
npm run test
npm run build

cd "$gitroot/backend"

# Collect static files
python3 manage.py collectstatic --noinput

# Migrate
python3 manage.py makemigrations
python3 manage.py migrate

# Run tests and server
python3 manage.py test
python3 manage.py runserver

cd $gitroot