#!/bin/bash

docker-compose up -d --build
echo "Waiting for DB to be up"
sleep 20
curl -v http://localhost:5000/init