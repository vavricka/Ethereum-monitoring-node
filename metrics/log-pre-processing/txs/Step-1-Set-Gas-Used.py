#!/usr/bin/python3
import pandas as pd
import numpy as np



# TODODOD>.......


TXS_GAS_LOG = "txgasused.log.FINAL" #txgasused.log* logs concatenated
TXS_LOG = "unique-unique-txs.log.FINAL"




TXS_OUT="unique-unique-txs-with-gasused.log"

# load txgasused only txhash and its gasuded
txsgas = pd.read_csv(TXS_GAS_LOG,
    names=['LocalTimeStamp','BlockHash','TxHash','GasUsed'], usecols=['LocalTimeStamp','TxHash','GasUsed'])

#sort by txhash
txsgas = txsgas.sort_values(by=['TxHash'])

#load uniquetxs
txs = pd.read_csv(TXS_LOG,
    names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
   'Cost','Size','To','From','ValidityErr'], index_col=False)

#add gasused column
txs["GasUsed"] = ""

#tmp   2019-02-28T14:29:38.134+0000   time of first tx in uniq.txs.ArithmeticError
timeFirstTx  = pd.to_datetime("2019-02-28T14:29:38.134+0000")

gasOlder = 0
invalidAndHasGas=0
notInGastxs=0



#loop all uniquetxs
for i, row in txs.iterrows():
    # if not inval  (row['ValidityErr'] == nil).
    #  chceck if txhash   is in   txgasused.log   SET   else   NA
    
    line = txsgas['TxHash'].searchsorted(row['Hash']) 
    try:
        if row['Hash'] == txsgas.iloc[line].TxHash:
            txs.at[i, 'GasUsed'] = txsgas.iloc[line].GasUsed

            #tmp GasOlderThanFirstTxInTXS
            if pd.to_datetime(txsgas.iloc[line].LocalTimeStamp) < timeFirstTx:
                print("GOLDER", txsgas.iloc[line].LocalTimeStamp, txsgas.iloc[line].TxHash)
                gasOlder = gasOlder + 1
            #also new ;;  invalid but IT IS in txgas... this would be missing in old setup..
            if row['ValidityErr'] == 'nil':
                print("Invalid", txsgas.iloc[line].LocalTimeStamp, txsgas.iloc[line].TxHash)
                invalidAndHasGas = invalidAndHasGas + 1

        else:  
            notInGastxs = notInGastxs + 1 
            # set txs  gasused   as  NA
            #because  this we don't have gasused in our db for this tx..
    except IndexError as e:
        print(row['LocalTimeStamp'], row['Hash'], e)

    
        



print("gasOlder:", gasOlder,"invalidAndHasGas:", invalidAndHasGas,"notInGastxs:",notInGastxs)


# export to new csv..
txs.to_csv(TXS_OUT, index=False, header=False)
