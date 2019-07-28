#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

TXS_LOG = sys.argv[1] #"txs-stage-5.log"

if not os.path.isfile(TXS_LOG):
    sys.exit(TXS_LOG, ": does not exists!")

dtypes = {
        'LocalTimeStamp'    : 'object',
        'Hash'              : 'object',
        'GasLimit'          : 'object',
        'GasPrice'          : 'float',
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
        'CommitTime0'       : 'float',
        'CommitTime3'       : 'float',
        'CommitTime12'      : 'float',
        'CommitTime36'      : 'float',
        }

#load txs  ALL fields  #sort NOT
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
            'Cost','Size','To','From','ValidityErr','CapturedLocally','GasUsed',
            'InMainBlock','InUncleBlocks','InOrder','NeverCommitting',
            'CommitTime0','CommitTime3','CommitTime12','CommitTime36'],
            usecols=['Value','Nonce','To','From','NeverCommitting','ValidityErr'],
            dtype=dtypes)

#sort 
txs = txs.sort_values(by=['From', 'Nonce', 'NeverCommitting'],ascending=[True,True,True])
txs.reset_index(inplace=True, drop=True)

committed_txs = txs.loc[txs['NeverCommitting'] == "Committed"].copy()
neverCommitting_txs = txs.loc[txs['NeverCommitting'] == "NeverCommitting"].copy()

comm_from =  ""
comm_nonce =""
comm_to =   ""
comm_value = "" 

never_comm_from = ""
never_comm_nonce = ""
never_comm_to = ""
never_comm_value = ""


num_never_com_same_TO = 0
num_never_com_diff_TO = 0
Num_BUG = 0

#for i in neverCommitting_txs.index:
for i in txs.index:

    if txs.at[i,'NeverCommitting'] != "NeverCommitting":
        comm_from = txs.at[i,'From']
        comm_nonce = txs.at[i,'Nonce']
        comm_to = txs.at[i,'To']
        comm_value, txs.at[i,'Value']

    elif txs.at[i,'NeverCommitting'] == "NeverCommitting":

        never_comm_from = txs.at[i,'From']
        never_comm_nonce = txs.at[i,'Nonce']
        never_comm_to = txs.at[i,'To']
        never_comm_value, txs.at[i,'Value']

        #### Now tmp   just verify that    
        if comm_from !=  never_comm_from or comm_nonce != never_comm_nonce:

            #continue
            #print("PROBLEM")
            Num_BUG = Num_BUG + 1

            ### THese bugs shall be prevalent only in incomplete logs
            #  caused by missing commited tx.

            #if comm_from !=  never_comm_from:
            #    print("BUG-from:", comm_from, never_comm_from)
            #else:
            #    print("BUG-nonce:", comm_nonce, never_comm_nonce)


        else:
            if comm_to != never_comm_to:
                num_never_com_diff_TO = num_never_com_diff_TO + 1

                #print(txs.at[i,'NeverCommitting'])
                #print(comm_to, never_comm_to)
            else:
                num_never_com_same_TO = num_never_com_same_TO + 1

            #if comm_value != never_comm_value:
            #    print(comm_value, never_comm_value)





            

print('txs', len(txs))
print('committed_txs', len(committed_txs))
print('neverCommitting_txs', len(neverCommitting_txs))

print("BUG:", Num_BUG)
print("never comm  diff  TO:", num_never_com_diff_TO)
print("never comm  same  TO:", num_never_com_same_TO)











