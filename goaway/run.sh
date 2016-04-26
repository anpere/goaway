#!/usr/bin/env bash
echo "Running init script"
source ~/goaway/goaway/init.sh
echo "killing servers listening on port 9060"
sudo kill `sudo lsof -t -i:9060`
echo "Running cmd server with config file path:"
echo $1
python ~/goaway/goaway/cmdserver.py $1 
