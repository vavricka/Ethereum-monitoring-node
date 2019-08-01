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
    usecols=['BlockHash','Number', 'Coinbase','BlockType'],
    dtype=dtypes_blocks)

len_blocks = len(blocks)
print("blocks total:  ", len_blocks)

#######   num per each coinbase
#print(blocks["Coinbase"].value_counts())

####### ASSIGN
blocks = blocks.assign(MiningPool = "ALL-OTHER-MINERS", probNext = np.nan, SameMinSeq = np.nan)
blocks.loc[blocks['Coinbase'] == "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8", 'MiningPool'] = "Ethermine"
blocks.loc[blocks['Coinbase'] == "0x5A0b54D5dc17e0AadC383d2db43B0a0D3E029c4c", 'MiningPool'] = "Sparkpool"
blocks.loc[blocks['Coinbase'] == "0x829BD824B016326A401d083B33D092293333A830", 'MiningPool'] = "f2pool2"
blocks.loc[blocks['Coinbase'] == "0x52bc44d5378309EE2abF1539BF71dE1b7d7bE3b5", 'MiningPool'] = "Nanopool"
blocks.loc[blocks['Coinbase'] == "0xb2930B35844a230f00E51431aCAe96Fe543a0347", 'MiningPool'] = "miningpoolhub1"
blocks.loc[blocks['Coinbase'] == "0x1B5B5906306c96b842dc03105E3b38636A4EDa0b", 'MiningPool'] = "HuoBi.pro"
blocks.loc[blocks['Coinbase'] == "0x2a5994b501E6A560e727b6C2DE5D856396aaDd38", 'MiningPool'] = "pandapool"
blocks.loc[blocks['Coinbase'] == "0x2a65Aca4D5fC5B5C859090a6c34d164135398226", 'MiningPool'] = "DwarfPool1"
blocks.loc[blocks['Coinbase'] == "0x005e288D713a5fB3d7c9cf1B43810A98688C7223", 'MiningPool'] = "xnpool"
blocks.loc[blocks['Coinbase'] == "0xD224cA0c819e8E97ba0136B3b95ceFf503B79f53", 'MiningPool'] = "uupool"
blocks.loc[blocks['Coinbase'] == "0x09ab1303d3CcAF5f018CD511146b07A240c70294", 'MiningPool'] = "Minerall"
blocks.loc[blocks['Coinbase'] == "0x35F61DFB08ada13eBA64Bf156B80Df3D5B3a738d", 'MiningPool'] = "firepool"
blocks.loc[blocks['Coinbase'] == "0x04668Ec2f57cC15c381b461B9fEDaB5D451c8F7F", 'MiningPool'] = "zhizhu"
blocks.loc[blocks['Coinbase'] == "0x06B8C5883Ec71bC3f4B332081519f23834c8706E", 'MiningPool'] = "MiningExpress"
blocks.loc[blocks['Coinbase'] == "0x4C549990A7eF3FEA8784406c1EECc98bF4211fA5", 'MiningPool'] = "Hiveon"
blocks.loc[blocks['Coinbase'] == "0x84A0d77c693aDAbE0ebc48F88b3fFFF010577051", 'MiningPool'] = "(0x84A0d7..)"
blocks.loc[blocks['Coinbase'] == "0xAA5c4244F05c92781C4F259913319d8ba1aCF05E", 'MiningPool'] = "(0xAA5c42..)"
blocks.loc[blocks['Coinbase'] == "0x00192Fb10dF37c9FB26829eb2CC623cd1BF599E8", 'MiningPool'] = "2miners"
blocks.loc[blocks['Coinbase'] == "0x52E44f279f4203Dcf680395379E5F9990A69f13c", 'MiningPool'] = "bw"
blocks.loc[blocks['Coinbase'] == "0x6a7a43BE33ba930fE58F34E07D0ad6bA7ADB9B1F", 'MiningPool'] = "Coinotron"
blocks.loc[blocks['Coinbase'] == "0x858fDEC2da9fA3CD3d97B8Bd1af98E9249D33613", 'MiningPool'] = "(0x858fDE..)"
blocks.loc[blocks['Coinbase'] == "0x002e08000acbbaE2155Fab7AC01929564949070d", 'MiningPool'] = "2minerssolo"




class CloseToOne(mscale.ScaleBase):
    name = 'close_to_one'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)
        self.nines = kwargs.get('nines', 5)

    def get_transform(self):
        return self.Transform(self.nines)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(FixedLocator(
                np.array([1-10**(-k) for k in range(1+self.nines)])))
        axis.set_major_formatter(FixedFormatter(
                [str(1-10**(-k)) for k in range(1+self.nines)]))


    def limit_range_for_scale(self, vmin, vmax, minpos):
        return vmin, min(1 - 10**(-self.nines), vmax)

    class Transform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, nines):
            mtransforms.Transform.__init__(self)
            self.nines = nines

        def transform_non_affine(self, a):
            masked = ma.masked_where(a > 1-10**(-1-self.nines), a)
            if masked.mask.any():
                return -ma.log10(1-a)
            else:
                return -np.log10(1-a)

        def inverted(self):
            return CloseToOne.InvertedTransform(self.nines)

    class InvertedTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, nines):
            mtransforms.Transform.__init__(self)
            self.nines = nines

        def transform_non_affine(self, a):
            return 1. - 10**(-a)

        def inverted(self):
            return CloseToOne.Transform(self.nines)

mscale.register_scale(CloseToOne)


#  take only  MAIN blocks from now
main_blocks = blocks[ blocks['BlockType'] == "Main" ]
rec_uncle_blocks = blocks[ blocks['BlockType'] == "Recognized" ]
unrec_forked_blocks = blocks[ blocks['BlockType'] == "Uncle" ]

len_man_blocks = len(main_blocks)
print("main blocks total:  ", len_man_blocks)
counts_of_blcks_per_pool = main_blocks["MiningPool"].value_counts()

#  crate a data framame   with  one min. pool  for each row
min_pools_list = main_blocks['MiningPool'].unique() 

min_pools = pd.DataFrame(min_pools_list, columns =['Pool'])
min_pools.set_index('Pool', inplace=True)

min_pools = min_pools.assign(count = counts_of_blcks_per_pool, countVStotal = np.nan, SameMinSeq = 0,
    seqVScount = np.nan, col_2_4_corel = np.nan,
    seq_1 = 0, seq_2 = 0, seq_3 = 0, seq_4 = 0, seq_5 = 0,
    seq_6 = 0, seq_7 = 0, seq_8 = 0, seq_9 = 0, seq_10 = 0)   #seq_10 means anything over 9,. e.g. 10,11,12..

for i in min_pools.index:
    min_pools.at[i, 'countVStotal'] = min_pools.at[i, 'count'] / len_man_blocks

min_pools = min_pools.sort_values('count', ascending=False)

#  reset index, because we dropped some forks and uncles
main_blocks.reset_index(inplace=True, drop=True)

#loop all  main blocks   (SORTED BY   Num  (ascending))
cur_seq = 1

for i in main_blocks.index:

    if i == 0:
        prevMiner = main_blocks.at[i, 'MiningPool']
        continue

    if main_blocks.at[i, 'MiningPool'] == prevMiner:
        min_pools.at[prevMiner, 'SameMinSeq'] = min_pools.at[prevMiner, 'SameMinSeq'] + 1
        cur_seq = cur_seq + 1
    else:
        if cur_seq == 1:
            min_pools.at[prevMiner, 'seq_1'] = min_pools.at[prevMiner, 'seq_1'] + 1
        elif cur_seq == 2:
            min_pools.at[prevMiner, 'seq_2'] = min_pools.at[prevMiner, 'seq_2'] + 1
        elif cur_seq == 3:
            min_pools.at[prevMiner, 'seq_3'] = min_pools.at[prevMiner, 'seq_3'] + 1
        elif cur_seq == 4:
            min_pools.at[prevMiner, 'seq_4'] = min_pools.at[prevMiner, 'seq_4'] + 1
        elif cur_seq == 5:
            min_pools.at[prevMiner, 'seq_5'] = min_pools.at[prevMiner, 'seq_5'] + 1
        elif cur_seq == 6:
            min_pools.at[prevMiner, 'seq_6'] = min_pools.at[prevMiner, 'seq_6'] + 1
        elif cur_seq == 7:
            min_pools.at[prevMiner, 'seq_7'] = min_pools.at[prevMiner, 'seq_7'] + 1
        elif cur_seq == 8:
            min_pools.at[prevMiner, 'seq_8'] = min_pools.at[prevMiner, 'seq_8'] + 1

            # print    miner and block num
            print("LEN-8", main_blocks.at[i-1, 'MiningPool'], main_blocks.at[i-8, 'Number'],
            main_blocks.at[i-1, 'Number'])

        elif cur_seq == 9:
            min_pools.at[prevMiner, 'seq_9'] = min_pools.at[prevMiner, 'seq_9'] + 1

            # print    miner and block num
            print("LEN-9", main_blocks.at[i-1, 'MiningPool'], main_blocks.at[i-9, 'Number'], 
            main_blocks.at[i-1, 'Number'])

        elif cur_seq > 9:
            min_pools.at[prevMiner, 'seq_10'] = min_pools.at[prevMiner, 'seq_10'] + 1  #seq_10 means anything over 9,. e.g. 10,11,12..

        cur_seq = 1

    prevMiner = main_blocks.at[i, 'MiningPool']

    # need to set len of seq for the last block
    if i == main_blocks.index[-1]:
        cur_miner = main_blocks.at[i, 'MiningPool']
        seq_str = "seq_" + str(cur_seq)
        min_pools.at[cur_miner, seq_str] = min_pools.at[cur_miner, seq_str] + 1

    
for i in min_pools.index:
    min_pools.at[i, 'seqVScount'] = min_pools.at[i, 'SameMinSeq'] / min_pools.at[i, 'count']
    min_pools.at[i, 'col_2_4_corel'] = min_pools.at[i, 'seqVScount'] - min_pools.at[i, 'countVStotal']



def print_bar_graph(min_pools):
    #only 5 biggest pools
    min_pools = min_pools[:5]

    #  graph  for  ? 3 biggest  ppooolls
    r = list(range(0,5))

    # From raw value to percentage
    totals = [i+j+k+l+m+n+o+p+q for i,j,k,l,m,n,o,p,q in zip(min_pools['seq_1'].reset_index(drop=True),
        min_pools['seq_2'].reset_index(drop=True), min_pools['seq_3'].reset_index(drop=True),
        min_pools['seq_4'].reset_index(drop=True), min_pools['seq_5'].reset_index(drop=True),
        min_pools['seq_6'].reset_index(drop=True), min_pools['seq_7'].reset_index(drop=True),
        min_pools['seq_8'].reset_index(drop=True), min_pools['seq_9'].reset_index(drop=True))]

    seq_1 = [i / j * 100 for i,j in zip(min_pools['seq_1'].reset_index(drop=True), totals)]

    seq_2 = [i / j * 100 for i,j in zip(min_pools['seq_2'].reset_index(drop=True), totals)]
    seq_3 = [i / j * 100 for i,j in zip(min_pools['seq_3'].reset_index(drop=True), totals)]
    seq_4 = [i / j * 100 for i,j in zip(min_pools['seq_4'].reset_index(drop=True), totals)]
    seq_5 = [i / j * 100 for i,j in zip(min_pools['seq_5'].reset_index(drop=True), totals)]
    seq_6 = [i / j * 100 for i,j in zip(min_pools['seq_6'].reset_index(drop=True), totals)]
    seq_7 = [i / j * 100 for i,j in zip(min_pools['seq_7'].reset_index(drop=True), totals)]
    seq_8 = [i / j * 100 for i,j in zip(min_pools['seq_8'].reset_index(drop=True), totals)]
    seq_9 = [i / j * 100 for i,j in zip(min_pools['seq_9'].reset_index(drop=True), totals)]
    
    # plot
    barWidth = 0.85
    names = ('Ethermine','Sparkpool','F2pool2','Nanopool','Miningpoolhub1')

    #f, ax = plt.subplots(1)
    #ax.set_ylim(bottom=0)

    # Create green Bars
    plt.bar(r, seq_1, color='#b5ffb9', edgecolor='white', width=barWidth, label="unique block")
    # Create orange Bars
    plt.bar(r, seq_2, bottom=seq_1, color='#f9bc86', edgecolor='white', width=barWidth, label="sequence of 2")
    # Create blue Bars
    plt.bar(r, seq_3, bottom=[i+j for i,j in zip(seq_1, seq_2)], color='#a3acff', edgecolor='white', width=barWidth, label="sequence of 3")
    # Create blue Bars
    plt.bar(r, seq_4, bottom=[i+j+k for i,j,k in zip(seq_1, seq_2, seq_3)], color='#c3acff', edgecolor='white', width=barWidth, label="sequence of 4")
    # Create blue Bars
    plt.bar(r, seq_5, bottom=[i+j+k+l for i,j,k,l in zip(seq_1, seq_2, seq_3, seq_4)], color='#f1acff', edgecolor='white', width=barWidth, label="sequence of 5+")
    # Create blue Bars
    plt.bar(r, seq_6, bottom=[i+j+k+l+m for i,j,k,l,m in zip(seq_1, seq_2, seq_3, seq_4, seq_5)], color='#b3acff', edgecolor='white', width=barWidth)
    # Create blue Bars
    plt.bar(r, seq_7, bottom=[i+j+k+l+m+n for i,j,k,l,m,n in zip(seq_1, seq_2, seq_3, seq_4, seq_5, seq_6)], color='#e3acff', edgecolor='white', width=barWidth)
    # Create blue Bars
    plt.bar(r, seq_8, bottom=[i+j+k+l+m+n+o for i,j,k,l,m,n,o in zip(seq_1, seq_2, seq_3, seq_4, seq_5, seq_6, seq_7)], color='#c3acff', edgecolor='white', width=barWidth)
    # Create blue Bars
    plt.bar(r, seq_9, bottom=[i+j+k+l+m+n+o+p for i,j,k,l,m,n,o,p in zip(seq_1, seq_2, seq_3, seq_4, seq_5, seq_6, seq_7, seq_8)], color='#a3acff', edgecolor='white', width=barWidth)

    # Custom x axis
    plt.xticks(r, names)
    #plt.xlabel("title ..")

    # Add a legend
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)

    plt.ylim(bottom=70)
    plt.yticks([70,75,80,85,90,95,100], ['70 %','75 %','80 %','85 %','90 %','95 %','100 %'])

    if SAVE_TO_FILE:
        plt.savefig('1-main-block-seqeunces.pdf', bbox_inches="tight")
    else:
        plt.show()


def print_cdf(min_pools):

    #TODO   all pools ...   or at least 8 biggest
    s_ethermine = []
    s_sparkpool = []
    s_f2pool2 = []
    s_Nanopool = []
    s_miningpoolhub1 = []
    s_pandapool = []


    for i in range(1,11): # seq_1 to seq_10
        num = min_pools.at['Ethermine', 'seq_' + str(i)]
        s_ethermine.extend([i for j in range(num)])

        num = min_pools.at['Sparkpool', 'seq_' + str(i)]
        s_sparkpool.extend([i for j in range(num)])

        num = min_pools.at['f2pool2', 'seq_' + str(i)]
        s_f2pool2.extend([i for j in range(num)])

        num = min_pools.at['Nanopool', 'seq_' + str(i)]
        s_Nanopool.extend([i for j in range(num)])

        num = min_pools.at['miningpoolhub1', 'seq_' + str(i)]
        s_miningpoolhub1.extend([i for j in range(num)])

        num = min_pools.at['pandapool', 'seq_' + str(i)]
        s_pandapool.extend([i for j in range(num)])


    bin_seq = list(range(0,11,1))
    fig, ax = plt.subplots()

    counts_ethermine, bin_edges_ethermine = np.histogram (s_ethermine, bins=bin_seq)
    cdf_ethermine = np.cumsum (counts_ethermine)
    #convert all Y==1 to Y=0.9999 because of plot
    yaxis = [0.99999 if x == 1 else x for x in cdf_ethermine/cdf_ethermine[-1]]
    lineethermine, = ax.plot (bin_edges_ethermine[1:], yaxis,drawstyle='steps-pre', label='Ethermine', linestyle=':')

    counts_sparkpool, bin_edges_sparkpool = np.histogram (s_sparkpool, bins=bin_seq)
    cdf_sparkpool = np.cumsum (counts_sparkpool)
    #convert all Y==1 to Y=0.9999 because of plot
    yaxis = [0.99999 if x == 1 else x for x in cdf_sparkpool/cdf_sparkpool[-1]]
    linesparkpool, = ax.plot (bin_edges_sparkpool[1:], yaxis,drawstyle='steps-pre', label='Sparkpool', linestyle='--')

    counts_f2pool2, bin_edges_f2pool2 = np.histogram (s_f2pool2, bins=bin_seq)
    cdf_f2pool2 = np.cumsum (counts_f2pool2)
    yaxis = [0.99999 if x == 1 else x for x in cdf_f2pool2/cdf_f2pool2[-1]]
    linef2pool2, = ax.plot (bin_edges_f2pool2[1:], yaxis,drawstyle='steps-pre', label='F2pool2', linestyle='-.')

    counts_Nanopool, bin_edges_Nanopool = np.histogram (s_Nanopool, bins=bin_seq)
    cdf_Nanopool = np.cumsum (counts_Nanopool)
    yaxis = [0.99999 if x == 1 else x for x in cdf_Nanopool/cdf_Nanopool[-1]]
    lineNanopool, = ax.plot (bin_edges_Nanopool[1:], yaxis,drawstyle='steps-pre', label='Nanopool', linestyle='-')

    counts_miningpoolhub1, bin_edges_miningpoolhub1 = np.histogram (s_miningpoolhub1, bins=bin_seq)
    cdf_miningpoolhub1 = np.cumsum (counts_miningpoolhub1)
    yaxis = [0.99999 if x == 1 else x for x in cdf_miningpoolhub1/cdf_miningpoolhub1[-1]]
    lineminingpoolhub1, = ax.plot (bin_edges_miningpoolhub1[1:], yaxis,drawstyle='steps-pre', label='Miningpoolhub1', linestyle=':')

    counts_pandapool, bin_edges_pandapool = np.histogram (s_pandapool, bins=bin_seq)
    cdf_pandapool = np.cumsum (counts_pandapool)
    yaxis = [0.99999 if x == 1 else x for x in cdf_pandapool/cdf_pandapool[-1]]
    linepandapool, = ax.plot (bin_edges_pandapool[1:], yaxis,drawstyle='steps-pre', label='Pandapool', linestyle='--')


    plt.xlabel('Mainchain block sequence length')

    plt.ylabel('CDF (logarithmic scale)')

    #plt.title("Distribution of main block sequences generated by an unique miner")

    #does not work thanks to  inverted log yaxis.
    #plt.yticks(np.arange(0.5, 1.1, step=0.1),['50%','60%','70%','80%','90%','100%'])
    
    #enable if neede,   i think it looks ugly
    # Don't allow the axis to be on top of your data
    ax.set_axisbelow(True)

    # Customize the grid
    ax.grid(linestyle=':', linewidth='0.3')#, color='red')


    ax.set_xlim(left=0.8)
    ax.set_xlim(right=10)
    nums = [1,2,3,4,5,6,7,8,9,10]
    labels = ['1','2','3','4','5','6','7','8','9','9+']

    plt.xticks(nums, labels)
    
    ax.legend()


    plt.yscale('close_to_one', nines=5)
    

    
    if SAVE_TO_FILE:
        plt.savefig('ptm-1-cdf.pdf', bbox_inches="tight")
    else:
        plt.show()






if input("print table? [y] or [n]: ") == "y":
    print(min_pools)

if input("print bar_plot? [y] or [n]: ") == "y":
    print_bar_graph(min_pools)

if input("print cdf_plot? [y] or [n]: ") == "y":
    print_cdf(min_pools)