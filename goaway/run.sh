#!/usr/bin/env bash
echo "Running init script"
## Ehm. this is bad
## source ~/goaway/goaway/init.sh
touch temp1.txt
echo "killing servers listening on port 9060"
sudo kill `sudo lsof -t -i:9060`
echo "Running cmd server with config file path:"
echo "started goaway on remote machine"
