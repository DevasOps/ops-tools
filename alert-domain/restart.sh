#!/bin/bash
docker stop alert-domain
docker rm alert-domain
sleep 2s
docker run --detach \
  --net=host \
  --volume $(pwd):/alert \
  --volume /etc/localtime:/etc/localtime \
  --restart always \
  --name alert-domain \
alert/wxzhang18:v1
