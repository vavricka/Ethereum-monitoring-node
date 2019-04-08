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

if len(sys.argv) != 4:
    sys.exit(sys.argv[0], ": expecting 3 parameters.")

#INPUT FILES
LOCAL_TXS = sys.argv[1] #"unique-unique-txs.log.FINAL"
REMOTE_TXS = sys.argv[2]
OUT = sys.argv[3]

if not os.path.isfile(LOCAL_TXS):
    sys.exit(LOCAL_TXS, ": does not exists!")

if not os.path.isfile(REMOTE_TXS):
    sys.exit(REMOTE_TXS, ": does not exists!")

if os.path.isfile(OUT):
    sys.exit(OUT, ": already exists!")

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
        'CapturedLocally'   : 'object',
        'GasUsed'           : 'object',
        'InMainBlock'       : 'object',
        'InUncleBlocks'     : 'object',
        'InOrder'           : 'object',
        'NeverCommitting'    : 'object',
        'CommitTime0'       : 'object',
        'CommitTime3'       : 'object',
        'CommitTime12'      : 'object',
        'CommitTime36'      : 'object',
        }

local_txs = pd.read_csv(
    LOCAL_TXS, 
    names=[
    'LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
    'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
    'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
    'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
    dtype=dtypes)

remote_txs = pd.read_csv(
    REMOTE_TXS, 
    names=[
    'LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
    'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
    'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
    'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
    dtype=dtypes)



local_txs['CapturedLocally'] = 'True'
remote_txs['CapturedLocally'] = 'False'

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
local_txs.to_csv(OUT, index=False, header=False)
