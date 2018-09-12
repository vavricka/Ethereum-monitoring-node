#!/bin/bash
#set -x

export PROJ_ROOT="$PWD"
export DATA_PATH="$PROJ_ROOT/clients-data"

export GETH="$PROJ_ROOT/go-ethereum"

#ONE TIME
#mkdir "$DATA_PATH"
#"$GETH/build/bin/geth" --datadir "$DATA_PATH" init rinkeby.json

#CONNECT
"$GETH/build/bin/geth" --networkid=4 --datadir "$DATA_PATH" \
--cache=3072 --ethstats='Epictetus:Respect my authoritah!@stats.rinkeby.io' \
--bootnodes=enode://a24ac7c5484ef4ed0c5eb2d36620ba4e4aa13b8c84684e1b4aab0cebea2ae45cb4d375b77eab56516d34bfbd3c1a833fc51296ff084b770b94fb9028c4d25ccf@52.169.42.101:30303 \
--verbosity 3 console 2>> "$DATA_PATH/geth-out.log" 
#--verbosity 6 console 2>> "$DATA_PATH/geth-out.log"