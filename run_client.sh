#!/bin/bash
#set -x

# The NETWORK_ID must be the same as in genesis.json
NETWORK_ID=19990022

# Check the number of parameters.
if [ $# -ne 1 ]; then
    printf "ERROR: This scripts expects one parameter:\n\
    run_client.sh <client number>\n"
    exit 1
fi

export PROJ_ROOT="$PWD"

CLIENT_NUMBER="$1"

if [ "$CLIENT_NUMBER" -lt 1 ] || [ "$CLIENT_NUMBER" -gt 10 ]; then
	printf "ERROR: Client number must be in range 1 - 10\n"
	exit 1
fi

export DATA_PATH="$PROJ_ROOT/clients-data"

if [[ ! -d "$DATA_PATH/$CLIENT_NUMBER" ]]; then
	printf "ERROR: $DATA_PATH/$CLIENT_NUMBER does not exist! \
	Maybe you forgot to deploy the private network. Run deploy_net.sh \
	<Ethereum-monitoring-node path> <number of clients> first.\n"
    exit 1
fi

export GETH="$PROJ_ROOT/go-ethereum"

# RUN the client in console mode.
"$GETH/build/bin/geth" --identity "INESC-ID-Node-$CLIENT_NUMBER" --datadir \
"$DATA_PATH/$CLIENT_NUMBER" --ipcdisable --port "3030$CLIENT_NUMBER" --nodiscover \
--networkid $NETWORK_ID --cache=64 console
