#!/bin/bash

export PROJ_ROOT="$PWD"
export DATA_PATH="$PROJ_ROOT/clients-data"

#UNCOMMENT and DO JUST ONE TIME
#mkdir "$DATA_PATH"

export GETH="$PROJ_ROOT/go-ethereum"

nohup "$GETH/build/bin/geth" --syncmode "fast" --identity \
"INESC" --datadir "$DATA_PATH" \
--cache=75000 --maxpeers 1500 --maxpendpeers 150 \
--lightpeers 0 --txpool.pricelimit 0 &>>"/dev/null" &
