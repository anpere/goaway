#!/usr/bin/env bash
echo "Running init script"
source ~/goaway/goaway/init.sh
echo "Running cmd server with config file path:"
echo $1
python ~/goaway/goaway/cmdserver.py $1
