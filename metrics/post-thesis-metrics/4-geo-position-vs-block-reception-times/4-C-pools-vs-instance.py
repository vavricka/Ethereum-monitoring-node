import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

from numpy import ma
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedFormatter, FixedLocator

#Set  True of False
SAVE_TO_FILE = True

if SAVE_TO_FILE:
    print("SAVE TO FILE IS SET")
    import matplotlib as mpl
    mpl.use('Agg')
else:
    print("SAVING TO FILE IS NOT SET, plots will be shown directly")

import matplotlib.pyplot as plt

#print all columns (not to cut the tail)
pd.set_option('display.expand_frame_repr', False)

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter - blocks-propagation-times-v3.log.")

BLOCKS_LOG = sys.argv[1] 
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

dtypes_blocks_propag_times_v3 = {
        'BlockHash'         : 'object',
        'Number'            : 'Int64',
        'BlockType'         : 'object',
        'AngainorTimeStamp' : 'object',
        'FalconTimeStamp'   : 'object',
        'S1USTimeStamp'     : 'object',
        'S2CNTimeStamp'     : 'object',
        'FirstObservation'  : 'object',
        'AngainorDiff'      : 'float',
        'FalconDiff'        : 'float',
        'S1USDiff'          : 'float',
        'S2CNDiff'          : 'float',
        'MiningPool'        : 'object',
        'NumTransactions'   : 'Int64',
        'SameMinerSeqLen'   : 'Int64',
        'PositionInsideSeq' : 'Int64',
        'Difficulty'        : 'Int64',   
        'BlockSize'         : 'Int64',
        'InterblockTime'    : 'float',   
        'InterblockTimePerPool' : 'float',
        }

#load blocks
blocks = pd.read_csv(BLOCKS_LOG, 
    names=['BlockHash','Number','BlockType','AngainorTimeStamp','FalconTimeStamp',
        'S1USTimeStamp','S2CNTimeStamp','FirstObservation',
        'AngainorDiff','FalconDiff','S1USDiff','S2CNDiff',
        'MiningPool','NumTransactions','SameMinerSeqLen','PositionInsideSeq',
        'Difficulty','BlockSize','InterblockTime','InterblockTimePerPool'],
    dtype=dtypes_blocks_propag_times_v3)



#
#
##now only ethermine
#ethermine_blocks = blocks[ blocks['MiningPool'] == "Ethermine" ]
##print(ethermine_blocks["AngainorDiff"].value_counts())
#print(len(ethermine_blocks))
#print(len(ethermine_blocks[ethermine_blocks["AngainorDiff"] <= 0]))
##print(len(ethermine_blocks[ethermine_blocks["AngainorDiff"] <= 0.01]))
#print(len(ethermine_blocks[ethermine_blocks["FalconDiff"] <= 0]))
#print(len(ethermine_blocks[ethermine_blocks["S1USDiff"] <= 0]))
#print(len(ethermine_blocks[ethermine_blocks["S2CNDiff"] <= 0]))
#





#  crate a data framame   with  one min. pool  for each row
min_pools_list = blocks['MiningPool'].unique() 
min_pools = pd.DataFrame(min_pools_list, columns =['MiningPool'])
min_pools.set_index('MiningPool', inplace=True)

#print(min_pools)
min_pools = min_pools.assign(
    pt = 0, cz = 0, us = 0, cn = 0,
    pt10ms = 0, cz10ms = 0, us10ms = 0, cn10ms = 0)


for i in blocks.index:
    currentMiner = blocks.at[i,'MiningPool']

    if blocks.at[i,'AngainorDiff'] <= 0:
        min_pools.at[currentMiner, 'pt'] = min_pools.at[currentMiner, 'pt'] + 1
    if blocks.at[i,'FalconDiff'] <= 0:
        min_pools.at[currentMiner, 'cz'] = min_pools.at[currentMiner, 'cz'] + 1
    if blocks.at[i,'S1USDiff'] <= 0:
        min_pools.at[currentMiner, 'us'] = min_pools.at[currentMiner, 'us'] + 1
    if blocks.at[i,'S2CNDiff'] <= 0:
        min_pools.at[currentMiner, 'cn'] = min_pools.at[currentMiner, 'cn'] + 1

    if blocks.at[i,'AngainorDiff'] <= 0.01:
        min_pools.at[currentMiner, 'pt10ms'] = min_pools.at[currentMiner, 'pt10ms'] + 1
    if blocks.at[i,'FalconDiff'] <= 0.01:
        min_pools.at[currentMiner, 'cz10ms'] = min_pools.at[currentMiner, 'cz10ms'] + 1
    if blocks.at[i,'S1USDiff'] <= 0.01:
        min_pools.at[currentMiner, 'us10ms'] = min_pools.at[currentMiner, 'us10ms'] + 1
    if blocks.at[i,'S2CNDiff'] <= 0.01:
        min_pools.at[currentMiner, 'cn10ms'] = min_pools.at[currentMiner, 'cn10ms'] + 1


print(min_pools)


def print_bar_graph(min_pools, precision10ms):
    if precision10ms == False:
        PT = 'pt'
        CZ = 'cz'
        US = 'us'
        CN = 'cn'
    else:
        PT = 'pt10ms'
        CZ = 'cz10ms'
        US = 'us10ms'
        CN = 'cn10ms'

    #only 11 biggest pools
    min_pools = min_pools[:11]

    #  graph  for  ? 3 biggest  ppooolls
    r = list(range(0,11))

    # From raw value to percentage
    totals = [i+j+k+l for i,j,k,l in zip(min_pools[PT].reset_index(drop=True),
        min_pools[CZ].reset_index(drop=True), min_pools[US].reset_index(drop=True),
        min_pools[CN].reset_index(drop=True))]

    #TMP PRINT
    #print("totals:", totals)

    pt = [i / j * 100 for i,j in zip(min_pools[PT].reset_index(drop=True), totals)]
    cz = [i / j * 100 for i,j in zip(min_pools[CZ].reset_index(drop=True), totals)]
    us = [i / j * 100 for i,j in zip(min_pools[US].reset_index(drop=True), totals)]
    cn = [i / j * 100 for i,j in zip(min_pools[CN].reset_index(drop=True), totals)]

    #TMP PRINT
    #print("pt:", pt)
    #print("cz:", cz)

    # plot
    barWidth = 0.85
    names = ('Spa\nrkp\nool','Eth\nerm\nine','F2p\nool2','2mi\nners\nsolo','Nano\npool',
        'Min\ning\nExpr\ness','min\ning\npool\nhub1','small\nminers\ncomb\nined',
        '2mi\nners','xnp\nool','pand\napool') #TODO check


    # Create green Bars
    plt.bar(r, pt, color='#b5ffb9', edgecolor='white', width=barWidth, label="Portugal")
    # Create orange Bars
    plt.bar(r, cz, bottom=pt, color='#f9bc86', edgecolor='white', width=barWidth, label="Czechia")
    # Create blue Bars
    plt.bar(r, us, bottom=[i+j for i,j in zip(pt, cz)], color='#a3acff', edgecolor='white',
        width=barWidth, label="USA - EAST")
    # Create blue Bars
    plt.bar(r, cn, bottom=[i+j+k for i,j,k in zip(pt, cz, us)], color='#c3acff',
        edgecolor='white', width=barWidth, label="Taiwan")

    # Custom x axis
    plt.xticks(r, names)
    #plt.xlabel("title ..")

    # Add a legend
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)

    plt.ylim(bottom=0)
    plt.yticks([0,25,50,75,100], ['0','25 %','50 %','75 %','100 %'])

    if SAVE_TO_FILE:
        plt.savefig('4-c-miners-vs-our-instances-10msPrecis.pdf', bbox_inches="tight")
    else:
        plt.show()


# False  / True    ()
#if precision10ms == False:    --> only raw data
#    precision10ms == True :  -->  using delay <0,10ms)

print_bar_graph(min_pools, True)
