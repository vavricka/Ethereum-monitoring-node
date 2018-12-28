#!/bin/bash

export PROJ_ROOT="$PWD"
export DATA_PATH="$PROJ_ROOT/clients-data"

#UNCOMMENT and DO JUST ONE TIME
#mkdir "$DATA_PATH"

export GETH="$PROJ_ROOT/go-ethereum"

#NOHUP
nohup "$GETH/build/bin/geth" --syncmode "fast" --identity \
"INESC-ID-EU-Lisbon" --datadir "$DATA_PATH" \
--cache=6144 --maxpeers "500" &>>"/dev/null" &

#CONSOLE
#"$GETH/build/bin/geth" --syncmode "fast" --identity \
#"INESC-ID-EU-Lisbon" --datadir "$DATA_PATH" \
#--cache=6144 --verbosity 5 console 2>>"/home/dvavricka/data/geth-out.log"
