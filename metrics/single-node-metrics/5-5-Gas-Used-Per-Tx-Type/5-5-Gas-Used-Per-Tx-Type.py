import numpy as np

#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd

#TXS_LOG= "unique-unique-txs.log.FINAL"
TXS_LOG="unique-unique-txs-with-gasused.log"

#txs = pd.read_csv(TX_CSV, usecols=['MsgType', 'GasLimit'])
txs = pd.read_csv(TXS_LOG, 
names=['LocalTimeStamp','Hash','GasLimit','GasPrice','Value','Nonce','MsgType',
'Cost','Size','To','From','ValidityErr','GasUsed'], usecols=['MsgType', 'ValidityErr', 'GasUsed'])

# print  txs before drop
print("Txs TOTAL: ", len(txs.index))
# drop txs w/ GasUsed   nil or -1,  validityErr != nil
condition = txs[ (txs['GasUsed'] == -1) | (txs['GasUsed'].isnull()) | (txs['ValidityErr'] != "nil") ].index
txs.drop(condition , inplace=True)

# print  txs after drop
print("Txs TOTAL (after drop): ", len(txs.index))


s_tx = txs[txs.MsgType == "TX"].GasUsed
s_mc = txs[txs.MsgType == "MC"].GasUsed
s_cc = txs[txs.MsgType == "CC"].GasUsed

bin_seq = list(range(0,8000000,20)) 

fig, ax = plt.subplots()

counts_tx, bin_edges_tx = np.histogram (s_tx, bins=bin_seq)
cdf_tx = np.cumsum (counts_tx)
lineTx, = ax.plot (bin_edges_tx[1:], cdf_tx/cdf_tx[-1], label='regular transfers')

counts_mc, bin_edges_mc = np.histogram (s_mc, bins=bin_seq)
cdf_mc = np.cumsum (counts_mc)
lineMc, = ax.plot (bin_edges_mc[1:], cdf_mc/cdf_mc[-1], label='function calls')

counts_cc, bin_edges_cc = np.histogram (s_cc, bins=bin_seq)
cdf_cc = np.cumsum (counts_cc)
lineCc, = ax.plot (bin_edges_cc[1:], cdf_cc/cdf_cc[-1], label='contract creations')

plt.xlabel('Gas used (x1000)')
plt.yticks(np.arange(0, 1.1, step=0.1),['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])

plt.xscale('symlog')
ax.set_xlim(left=20000)
ax.set_xlim(right=8000000)

nums = [21000,80000,160000,500000,1000000,2000000,4000000,8000000]
labels = ['21', '80', '160', '500', '1000', '2000', '4000', '8000']

plt.xticks(nums, labels)

##  tmp
for q in [50, 90, 95, 100]:
    print ("reg tx  :{}%% percentile: {}".format (q, np.percentile(s_tx, q)))
    print ("Msg call:{}%% percentile: {}".format (q, np.percentile(s_mc, q)))
    print ("con crea:{}%% percentile: {}".format (q, np.percentile(s_cc, q)))
##end tmp

ax.legend()

#LOCAL show
#plt.show()
#save to file
plt.savefig('5-5-txs-gasUsed.pdf')
