import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#save to file
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

#print all columns (not to cut the tail)
pd.set_option('display.expand_frame_repr', False)

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

BLOCKS = sys.argv[1] #"blocks-stage-4.log"
if not os.path.isfile(BLOCKS):
    sys.exit(BLOCKS, ": does not exists!")


dtypes_blocks = {
        'LocalTimeStamp'    : 'object',
        'BlockHash'     : 'object',
        'Number'        : 'object',
        'GasLimit'      : 'object',
        'GasUsed'       : 'object',
        'Difficulty'    : 'object',
        'Time'          : 'object',
        'Coinbase'      : 'object',
        'ParentHash'    : 'object',
        'UncleHash'     : 'object',
        'BlockSize'     : 'object',
        'ListOfTxs'     : 'object',
        'ListOfUncles'  : 'object',
        'CapturedLocally'   : 'bool',
        'BlockType'         : 'object',
        'ForkLength'    : 'int',
        }

# load  blck-st-4   ;  load only needed   things (surely not txs)
blocks = pd.read_csv(BLOCKS, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    usecols=['LocalTimeStamp','BlockHash','Number', 'Coinbase','BlockType'],
    dtype=dtypes_blocks)


len_blocks = len(blocks)




main_blocks = blocks[ blocks['BlockType'] == "Main" ]
main_blocks.set_index('Number', inplace=True)




#  select  forks only (both rec and unrec)
forked_blocks = blocks[ blocks['BlockType'] != "Main" ]



#add deltas
forked_blocks = forked_blocks.assign(deltaVsMainBlock = np.nan)


# for each for compare tiemstamp  with coresp. main
for i in forked_blocks.index:

    # those which were received before  main,  print   number,  timedelta,  timeA timeB
    block_num = forked_blocks.at[i, 'Number']
    fork_time = forked_blocks.at[i, 'LocalTimeStamp']

    main_time = main_blocks.at[block_num, 'LocalTimeStamp']

    delta_times = (pd.to_datetime(main_time) - pd.to_datetime(fork_time)).total_seconds()
    forked_blocks.at[i, 'deltaVsMainBlock'] = delta_times

    # printing...
    if delta_times > 10:
        print(block_num, "FORK", fork_time, "MAIN", main_time, delta_times)
        

#end for


#ffm = ffm
ffm = forked_blocks[ forked_blocks['deltaVsMainBlock'] > 0 ]



delayed_main_blocks = len(ffm)
delayed_main_blocks_up_to_1 = len(ffm[  (ffm['deltaVsMainBlock'] < 1 ) ] )
delayed_main_blocks_1_to_5 = len(ffm[  (ffm['deltaVsMainBlock'] >= 1 ) & (ffm['deltaVsMainBlock'] < 5 ) ] )
delayed_main_blocks_5_to_12 = len(ffm[  (ffm['deltaVsMainBlock'] >= 5 ) & (ffm['deltaVsMainBlock'] < 12 ) ] )
delayed_main_blocks_over_12 = len(ffm[  (ffm['deltaVsMainBlock'] > 12 ) ] )

print("blocks total:  ", len_blocks)
# print number of forks
print("forked blocks (uncles+unrecognized) total:  ", len(forked_blocks))
# print number of forks that were captured before main blocks.
print("delayed main blcks:", delayed_main_blocks)
print("out of them delayed less than 1 sec:", delayed_main_blocks_up_to_1, delayed_main_blocks_up_to_1/delayed_main_blocks * 100, "%")
print("out of them delayed <1 - 5) sec:", delayed_main_blocks_1_to_5, delayed_main_blocks_1_to_5/delayed_main_blocks * 100, "%")
print("out of them delayed <5 - 12) sec:", delayed_main_blocks_5_to_12, delayed_main_blocks_5_to_12/delayed_main_blocks * 100, "%")
print("out of them delayed 12+ sec:", delayed_main_blocks_over_12, delayed_main_blocks_over_12/delayed_main_blocks * 100, "%")








##########PLOT

#PLOT graph
s_forks     =  ffm.deltaVsMainBlock

bin_seq = list(np.arange(0,50,0.02))    #np.arange(0, 1.1, step=0.1)
fig, ax = plt.subplots()

counts, bin_edges = np.histogram (s_forks, bins=bin_seq)
cdf = np.cumsum (counts)
linetxs0, = ax.plot (bin_edges[1:], cdf/cdf[-1], label='Forks observed before corresponding main blocks')


plt.yticks(np.arange(0, 1.1, step=0.1),['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])
#
plt.xlabel('delay [seconds]')
plt.xscale('linear')
ax.set_xlim(left=0)
ax.set_xlim(right=1)
nums = [0,1,2,3,5,10,20,30,40,50]
labels = ['0','1','2','3','5','10','20','30','40','50']

plt.xticks(nums, labels)
ax.legend()

#LOCAL show
#plt.show()
##save to file
plt.savefig('PTM-2-Forks-observed-before-main-blocks.pdf')


