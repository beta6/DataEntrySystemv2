#!/bin/bash
img=`docker ps -a |grep des:latest|head -1|cut -f1 -d' '`
docker container start $img
docker container exec -it $img  bash

