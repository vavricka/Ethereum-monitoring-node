#!/bin/bash

export PROJ_ROOT="$PWD"
export DATA_PATH="$PROJ_ROOT/clients-data"

#UNCOMMENT and DO JUST ONE TIME
#mkdir "$DATA_PATH"

export GETH="$PROJ_ROOT/go-ethereum"

nohup "$GETH/build/bin/geth" --syncmode "fast" --identity \
"INESC" --datadir "$DATA_PATH" \
--cache=16384 --maxpeers 1500 --maxpendpeers 150 \
--lightpeers 0 --txpool.pricelimit 0 &>>"/dev/null" &
#--verbosity 5 &>>"/mnt/ssd_1tb/dvavricka/logs/geth-out.log" &
