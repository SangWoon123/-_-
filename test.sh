#!/usr/bin/env bash

home=~
echo `docker build -t ksw1_base ~/ksw/ksw1`
echo `docker build -t ksw2_base ~/ksw/ksw2`
echo `docker build -t ksw3_base ~/ksw/ksw3`
echo `docker build -t ksw4_base ~/ksw/ksw4`

echo `docker run -dit --name ksw1_con -p 5000:5000 ksw1_base`
echo `docker run -dit --name ksw2_con -p 5001:5001 ksw2_base`
echo `docker run -dit --name ksw3_con -p 5002:5002 ksw3_base`
echo `docker run -dit --name ksw4_con -p 5003:5003 ksw4_base`

echo `docker network create ksw-network`

echo `docker network connect ksw-network ksw1_con`
echo `docker network connect ksw-network ksw2_con`
echo `docker network connect ksw-network ksw3_con`
echo `docker network connect ksw-network ksw4_con`

echo `curl http://localhost:5000/ksw1/1`
