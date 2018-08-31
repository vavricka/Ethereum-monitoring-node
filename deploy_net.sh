#!/bin/bash
set -x

# Check number of parameters.
if [ $# -ne 1 ]; then
    printf "ERROR: This scripts expects one parameter:\n\
    deploy_net.sh <Num of clients to deploy>\n"
    exit 1
fi

export PROJ_ROOT="$PWD"

NUM_CLIENTS="$1"

if [ "$NUM_CLIENTS" -lt 1 ] || [ "$NUM_CLIENTS" -gt 10 ] ; then
	printf "ERROR: You can deploy only 1 - 10 clients.\n"
	exit 1
fi

export DATA_PATH="$PROJ_ROOT/clients-data"
export GETH="$PROJ_ROOT/go-ethereum"

if [[ -d "$DATA_PATH" ]]; then
	rm -rf "$DATA_PATH"
	sleep 1
fi

while [ $NUM_CLIENTS -ge 1 ]; do
	mkdir -p "$DATA_PATH/$NUM_CLIENTS"
	"$GETH/build/bin/geth" --datadir "$DATA_PATH/$NUM_CLIENTS" init "$PROJ_ROOT/genesis.json"
    NUM_CLIENTS=$((NUM_CLIENTS-1))
done
