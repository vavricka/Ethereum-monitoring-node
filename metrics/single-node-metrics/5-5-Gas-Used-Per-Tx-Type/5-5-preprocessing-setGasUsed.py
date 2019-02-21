#!/usr/bin/python3
import pandas as pd
import numpy as np

TXS_GAS_LOG = "txgasused.log.FINAL" #txgasused.log* logs concatenated
TXS_LOG = "unique-unique-txs.log.FINAL"
TXS_OUT="unique-unique-txs-with-gasused.log"

# load txgasused only txhash and its gasuded
txsgas = pd.read_csv(TXS_GAS_LOG,
    names=['BlockHash','TxHash','GasUsed'], usecols=['TxHash','GasUsed'])

#sort by txhash
txsgas = txsgas.sort_values(by=['TxHash'])

#load uniquetxs
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
   'Cost','Size','To','From','ValidityErr'], index_col=False)

#add gasused column
txs["GasUsed"] = ""

#loop all uniquetxs
for i, row in txs.iterrows():
    # if not inval  (row['ValidityErr'] == nil).
    #  chceck if txhash   is in   txgasused.log   SET   else   NA
    if row['ValidityErr'] == 'nil':
        line = txsgas['TxHash'].searchsorted(row['Hash']) 

        if row['Hash'] == txsgas.iloc[line][0]:
            tmpGasUsed = txsgas.iloc[line][1]

            if tmpGasUsed != -1:
                txs.at[i, 'GasUsed'] = tmpGasUsed

        else:  
            pass
            # set txs  gasused   as  NA
            #because  this we don't have gasused in our db for this tx..
    else:
        #  set  gasused  for this tx   as nil  (was invalid tx already)
        pass

# export to new csv..
txs.to_csv(TXS_OUT, index=False, header=False)
