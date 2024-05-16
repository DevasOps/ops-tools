#!/bin/bash
docker stop alert-night
docker rm alert-night
sleep 2s
docker run --detach \
  --net=host \
  --volume $(pwd):/alert \
  --volume /etc/localtime:/etc/localtime \
  --restart always \
  --name alert-night \
alert/wxzhang18:v1
