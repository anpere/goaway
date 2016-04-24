#!/usr/bin/env bash 
# GOAWAYPATH=~/goaway
# export $GOAWAYPATH
cd ~/goaway
sudo pip install -r goaway/requirements.txt
python goaway/cmdserver.py $1
