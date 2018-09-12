#!/usr/bin/python3

import pandas as pd

PROJ_ROOT = "/Users/deus/Projects/Ethereum-monitoring-node/"
LOGS_PATH = PROJ_ROOT + "raw-logs/csv/"

TX_CSV = LOGS_PATH + "TxMsg.csv"
#TX_CSV = LOGS_PATH + "TxMsgTEST.csv"

#read file into DataFrame
txs = pd.read_csv(TX_CSV, usecols=['MsgType', 'GasLimit'])


def print_info(msgType):
    #uncomment to print all gasLimits for each msg separately
    #print( txs[txs.MsgType == msgType].GasLimit)
    #print( txs[txs.MsgType == msgType])

    print("The mean \"GasLimit\" for the ", msgType, "msg-type is: ")
    print(txs[txs.MsgType == msgType].GasLimit.values.mean())


print_info("CC")
print_info("MC")
print_info("TX")
