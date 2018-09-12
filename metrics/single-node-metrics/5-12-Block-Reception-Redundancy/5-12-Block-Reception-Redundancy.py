#!/usr/bin/python3

import pandas as pd

PROJ_ROOT = "/Users/deus/Projects/Ethereum-monitoring-node/"
LOGS_PATH = PROJ_ROOT + "raw-logs/csv/"

NEWBLOCK_CSV = LOGS_PATH + "NewBlockMsg.csv"
NEWBLOCKHASHES_CSV = LOGS_PATH + "NewBlockHashesMsg.csv"
#NEWBLOCK_CSV = LOGS_PATH + "NewBlockMsgTEST.csv"
#NEWBLOCKHASHES_CSV = LOGS_PATH + "NewBlockHashesMsgTEST.csv"

#read file into a DataFrame
blck1 = pd.read_csv(NEWBLOCK_CSV, usecols=['BlockHash'])
blck2 = pd.read_csv(NEWBLOCKHASHES_CSV, usecols=['BlockHash'])
blck1_hashes = blck1["BlockHash"]
blck2_hashes = blck2["BlockHash"]
blck_total = blck1_hashes.append(blck2_hashes, ignore_index=True)

#computes how many times the same blockHash was received per msgType
#msgType -- block received via NewBlockMsg or NewBlockHashesMsg or combined
def print_info(msgType):
    #occurencies = occurencies.sort_index()
    occurencies = pd.value_counts(msgType.value_counts().values)
    for i, row in occurencies.iteritems():
        print("In total", row, "txs were received", i, "times")
    print("Avg number of block reception", msgType.value_counts().values.mean())

print("BLOCKS are propagated using 2 different message types",
"NewBlockMsg and NewBlockHashesMsg.")

print("####### NewBlockMsg:")
print_info(blck1_hashes)

print("####### NewBlockHashesMsg:")
print_info(blck2_hashes)

print("####### NewBlockMsg and NewBlockHashesMsg together:")
print_info(blck_total)
