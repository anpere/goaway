#!/usr/bin/env bash
echo "Running init script"
## Ehm. this is bad
## source ~/goaway/goaway/init.sh
echo "killing servers listening on port 9060"
sudo kill -9 `sudo lsof -t -i:9060`
