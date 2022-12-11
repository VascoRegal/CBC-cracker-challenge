#!/bin/bash

docker stop cbc && docker rm cbc
docker build -t cbcexploit .
docker run -d -p 80:80 -e KEY_LEN=128 -e FLAG=ganza  --name cbc cbcexploit