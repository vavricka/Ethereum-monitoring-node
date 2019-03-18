#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
import gc
from pathlib import Path

# Merges txs from 
# another node to fill the missing txs in the curent machine.
# also adds two new params: GasUsed,CapturedLocally
#  CapturedLocally - True - if the block was there; False -> if it was added in this
# GasUsed will be filled in the following Step 1
#  script and in this case, the LocalTimestamp does not count...
#  Input: unique-unique-txs.log.FINAL unique-unique-txs.log.FINAL.OTHERMACHINE
#  Output txs-stage-1.log

if len(sys.argv) != 3:
    sys.exit(sys.argv[0], ": expecting 2 parameters.")

#INPUT FILES
LOCAL_TXS = sys.argv[1] #"unique-unique-txs.log.FINAL"
REMOTE_TXS = sys.argv[2]

if not os.path.isfile(LOCAL_TXS):
    sys.exit(LOCAL_TXS, ": does not exists!")

if not os.path.isfile(REMOTE_TXS):
    sys.exit(REMOTE_TXS, ": does not exists!")

#output of this script
TXS_FINAL_LOG = "txs-stage-1.log"

dtypes = {
        'LocalTimeStamp'    : 'object',
        'Hash'              : 'object',
        'GasLimit'          : 'object',
        'GasPrice'          : 'object',
        'Value'             : 'object',
        'Nonce'             : 'object',
        'MsgType'           : 'object',
        'Cost'              : 'object',
        'Size'              : 'object',
        'To'                : 'object',
        'From'              : 'object',
        'ValidityErr'       : 'object',
        }

local_txs = pd.read_csv(LOCAL_TXS, 
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
   'Cost','Size','To','From','ValidityErr'], dtype=dtypes)

remote_txs = pd.read_csv(REMOTE_TXS, 
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
   'Cost','Size','To','From','ValidityErr'], dtype=dtypes)

# add  4 columns to loc & all captLoc = True
local_txs = local_txs.assign(CapturedLocally = True, GasUsed = np.nan, InMainBlock = np.nan,
    InBlocks = np.nan, InOrder = np.nan, CommitTime = np.nan, NeverCommiting = np.nan,
    RemoteTimeStamp = np.nan)

# add  4 columns to loc & all captLoc = False
remote_txs = remote_txs.assign(CapturedLocally = False, GasUsed = np.nan, InMainBlock = np.nan,
    InBlocks = np.nan, InOrder = np.nan, CommitTime = np.nan, NeverCommiting = np.nan,
    RemoteTimeStamp = np.nan)

#merge both together
local_txs = local_txs.append(remote_txs, ignore_index=True)
#drop remote
del remote_txs
gc.collect()

#sort by HASH  and then by CapturedLocally(True up.)
local_txs.sort_values(['Hash', 'CapturedLocally'], ascending=[True, False], inplace=True)

#dropduplicates   preserve  first (with CapturedLocally==True)
local_txs.drop_duplicates(subset='Hash', keep='first', inplace=True)

#out
local_txs = local_txs.sort_values(by=['LocalTimeStamp'])
local_txs.to_csv(TXS_FINAL_LOG, index=False, header=False)
