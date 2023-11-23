#!/bin/bash

cd "$1" || exit 1
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 989870301024.dkr.ecr.us-east-1.amazonaws.com
docker build -t p4 .
docker tag p4:latest 989870301024.dkr.ecr.us-east-1.amazonaws.com/p4:latest
