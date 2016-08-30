#!/bin/bash

echo "Starting docker-compose"
docker-compose up --build -d

echo "Running tests for worker"
docker-compose exec worker python -m unittest discover tests -p "*_test.py"

echo -e "\n\n"

echo "Running tests for api"
docker-compose exec api python -m unittest history_api_test

echo "Stopping docker-compose"
docker-compose stop
