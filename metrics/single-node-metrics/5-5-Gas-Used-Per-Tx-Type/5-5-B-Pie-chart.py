import numpy as np

#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd

TXS_LOG="unique-unique-txs-with-gasused.log"
#TXS_LOG="/Users/deus/tmp/unique-txs-w-gas.log"

txs = pd.read_csv(TXS_LOG, 
names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
'Cost','Size','To','From','ValidityErr','GasUsed'], usecols=['MsgType', 'ValidityErr', 'GasUsed'])

# print  txs before drop
print("Txs TOTAL: ", len(txs.index))
print("TX: ", len(txs[txs.MsgType == "TX"]))
print("MC: ", len(txs[txs.MsgType == "MC"]))
print("CC: ", len(txs[txs.MsgType == "CC"]))

txsnum = len(txs[txs.MsgType == "TX"])
mcs = len(txs[txs.MsgType == "MC"])
ccs = len(txs[txs.MsgType == "CS"])

df = pd.DataFrame({'num': [txsnum, mcs , ccs]},index=['TX', 'MC', 'CC'])
plot = df.plot.pie(y='num', figsize=(5, 5))
#save to file
plt.savefig('5-5-txs-Pie-before-drop.pdf')


# drop txs w/ GasUsed   nil or -1,  validityErr != nil
condition = txs[ (txs['GasUsed'] == -1) | (txs['GasUsed'].isnull()) | (txs['ValidityErr'] != "nil") ].index
txs.drop(condition , inplace=True)

# print  txs after drop
print("Txs TOTAL (after drop): ", len(txs.index))


print("TX: ", len(txs[txs.MsgType == "TX"]))
print("MC: ", len(txs[txs.MsgType == "MC"]))
print("CC: ", len(txs[txs.MsgType == "CC"]))

txsnum = len(txs[txs.MsgType == "TX"])
mcs = len(txs[txs.MsgType == "MC"])
ccs = len(txs[txs.MsgType == "CS"])

df = pd.DataFrame({'num': [txsnum, mcs , ccs]},index=['TX', 'MC', 'CC'])
plot = df.plot.pie(y='num', figsize=(5, 5))
#save to file
plt.savefig('5-5-txs-Pie-after-drop.pdf')





#LOCAL show
#plt.show()
#save to file
#plt.savefig('5-5-txs-Pie.pdf')
