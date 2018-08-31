#!/bin/bash
#set -x

export PROJ_ROOT="$PWD"
export DATA_PATH="$PROJ_ROOT/clients-data"

#UNCOMMENT and DO JUST ONE TIME
#mkdir "$DATA_PATH"

export GETH="$PROJ_ROOT/go-ethereum"

# RUN the client in console mode.
"$GETH/build/bin/geth" --syncmode "fast" --identity \
"INESC-ID-1-EU-Lisbon" --datadir "$DATA_PATH" \
--cache=4096 --verbosity 6 console 2>> "$DATA_PATH/geth-out.log"

#later:  nohup command-name &
#        = no console, run on background ...
