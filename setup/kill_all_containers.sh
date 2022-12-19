#!/bin/bash

num_running_containers=$(docker ps -q | wc -l)
echo $num_running_containers
if [ "$num_running_containers" -gt "0" ];
then
    docker kill $(docker ps -q)
    docker rm $(docker ps -a -q)
fi
