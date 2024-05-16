#!/bin/bash
docker stop alert-host
docker rm alert-host
sleep 2s
docker run --detach \
  --net=host \
  --volume $(pwd):/alert \
  --volume /etc/localtime:/etc/localtime \
  --restart always \
  --name alert-host \
alert/wxzhang18:v1
