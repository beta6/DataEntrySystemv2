#!/bin/bash
img=`docker ps -a |grep des:latest|cut -f1 -d' '|head -1`
docker container stop $img

