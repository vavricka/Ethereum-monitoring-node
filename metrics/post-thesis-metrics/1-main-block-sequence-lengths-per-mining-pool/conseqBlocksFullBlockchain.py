import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

#from numpy import ma



if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting 1 parameter.")

BLOCKS = sys.argv[1] #"blocks-stage-4.log"
if not os.path.isfile(BLOCKS):
    sys.exit(BLOCKS, ": does not exists!")

dtypes_blocks = {
        'number'        : 'int',
        'hash'          : 'object',
        'parent_hash'   : 'object',
        'nonce'         : 'object',
        'sha3_uncles'   : 'object',
        'logs_bloom'    : 'object',
        'transactions_root' : 'object',
        'state_root'        : 'object',
        'receipts_root'     : 'object',
        'miner'             : 'object',
        'difficulty'        : 'object',
        'total_difficulty'  : 'object',
        'size'          : 'object',
        'extra_data'    : 'object',
        'gas_limit'     : 'object',
        'gas_used'      : 'object',
        'timestamp'     : 'object',
        'transaction_count' : 'int',
        }

# load  blck-st-4   ;  load only needed   things (surely not txs)
blocks = pd.read_csv(BLOCKS, 
    usecols=['number','miner'],
    dtype=dtypes_blocks)

#number,hash,parent_hash,nonce,sha3_uncles,logs_bloom,transactions_root,state_root,
# receipts_root,miner,difficulty,total_difficulty,
# size,extra_data,gas_limit,gas_used,timestamp,transaction_count


len_blocks = len(blocks)
print("blocks total:  ", len_blocks)

#######   num per each coinbase
#print(blocks["miner"].value_counts())


####### ASSIGN
blocks = blocks.assign(MiningPool = "ALL-OTHER-MINERS", probNext = np.nan, SameMinSeq = np.nan)
blocks.loc[blocks['miner'] == "0xEA674fdDe714fd979de3EdF0F56AA9716B898ec8".lower(), 'MiningPool'] = "Ethermine"
blocks.loc[blocks['miner'] == "0x5A0b54D5dc17e0AadC383d2db43B0a0D3E029c4c".lower(), 'MiningPool'] = "Sparkpool"
blocks.loc[blocks['miner'] == "0x829BD824B016326A401d083B33D092293333A830".lower(), 'MiningPool'] = "f2pool2"
blocks.loc[blocks['miner'] == "0x52bc44d5378309EE2abF1539BF71dE1b7d7bE3b5".lower(), 'MiningPool'] = "Nanopool"
blocks.loc[blocks['miner'] == "0xb2930B35844a230f00E51431aCAe96Fe543a0347".lower(), 'MiningPool'] = "miningpoolhub1"
blocks.loc[blocks['miner'] == "0x1B5B5906306c96b842dc03105E3b38636A4EDa0b".lower(), 'MiningPool'] = "HuoBi.pro"
blocks.loc[blocks['miner'] == "0x2a5994b501E6A560e727b6C2DE5D856396aaDd38".lower(), 'MiningPool'] = "pandapool"
blocks.loc[blocks['miner'] == "0x2a65Aca4D5fC5B5C859090a6c34d164135398226".lower(), 'MiningPool'] = "DwarfPool1"
blocks.loc[blocks['miner'] == "0x005e288D713a5fB3d7c9cf1B43810A98688C7223".lower(), 'MiningPool'] = "xnpool"
blocks.loc[blocks['miner'] == "0xD224cA0c819e8E97ba0136B3b95ceFf503B79f53".lower(), 'MiningPool'] = "uupool"
blocks.loc[blocks['miner'] == "0x09ab1303d3CcAF5f018CD511146b07A240c70294".lower(), 'MiningPool'] = "Minerall"
blocks.loc[blocks['miner'] == "0x35F61DFB08ada13eBA64Bf156B80Df3D5B3a738d".lower(), 'MiningPool'] = "firepool"
blocks.loc[blocks['miner'] == "0x04668Ec2f57cC15c381b461B9fEDaB5D451c8F7F".lower(), 'MiningPool'] = "zhizhu"
blocks.loc[blocks['miner'] == "0x06B8C5883Ec71bC3f4B332081519f23834c8706E".lower(), 'MiningPool'] = "MiningExpress"
blocks.loc[blocks['miner'] == "0x4C549990A7eF3FEA8784406c1EECc98bF4211fA5".lower(), 'MiningPool'] = "Hiveon"
blocks.loc[blocks['miner'] == "0x84A0d77c693aDAbE0ebc48F88b3fFFF010577051".lower(), 'MiningPool'] = "(0x84A0d7..)"
blocks.loc[blocks['miner'] == "0xAA5c4244F05c92781C4F259913319d8ba1aCF05E".lower(), 'MiningPool'] = "(0xAA5c42..)"
blocks.loc[blocks['miner'] == "0x00192Fb10dF37c9FB26829eb2CC623cd1BF599E8".lower(), 'MiningPool'] = "2miners"
blocks.loc[blocks['miner'] == "0x52E44f279f4203Dcf680395379E5F9990A69f13c".lower(), 'MiningPool'] = "bw"
blocks.loc[blocks['miner'] == "0x6a7a43BE33ba930fE58F34E07D0ad6bA7ADB9B1F".lower(), 'MiningPool'] = "Coinotron"
blocks.loc[blocks['miner'] == "0x858fDEC2da9fA3CD3d97B8Bd1af98E9249D33613".lower(), 'MiningPool'] = "(0x858fDE..)"
blocks.loc[blocks['miner'] == "0x002e08000acbbaE2155Fab7AC01929564949070d".lower(), 'MiningPool'] = "2minerssolo"


num_all_blocks = len(blocks)

counts_of_blcks_per_pool = blocks["MiningPool"].value_counts()

#  crate a data framame   with  one min. pool  for each row
min_pools_list = blocks['MiningPool'].unique() 

min_pools = pd.DataFrame(min_pools_list, columns =['MiningPool'])
min_pools.set_index('MiningPool', inplace=True)

min_pools = min_pools.assign(count = counts_of_blcks_per_pool, countVStotal = np.nan, SameMinSeq = 0,
    seqVScount = np.nan, col_2_4_corel = np.nan,
    seq_1 = 0, seq_2 = 0, seq_3 = 0, seq_4 = 0, seq_5 = 0,
    seq_6 = 0, seq_7 = 0, seq_8 = 0, seq_9 = 0, seq_10 = 0,
    seq_11 = 0, seq_12 = 0, seq_13 = 0, seq_14 = 0, seq_15 = 0)   #seq_15 means anything over 14

for i in min_pools.index:
    min_pools.at[i, 'countVStotal'] = min_pools.at[i, 'count'] / num_all_blocks

min_pools = min_pools.sort_values('count', ascending=False)

#  reset index, because we dropped some forks and uncles
#blocks.reset_index(inplace=True, drop=True)

#loop all  main blocks   (SORTED BY   Num  (ascending))
cur_seq = 1
seq_str = ""

for i in blocks.index:

    if i == 0:
        prevMiner = blocks.at[i, 'MiningPool']
        continue

    if blocks.at[i, 'MiningPool'] == prevMiner:
        min_pools.at[prevMiner, 'SameMinSeq'] = min_pools.at[prevMiner, 'SameMinSeq'] + 1
        cur_seq = cur_seq + 1
    else:

        if cur_seq < 15:
            seq_str = "seq_" + str(cur_seq)
        else:
            seq_str = "seq_15"


        #TMP PRINT  SEQ-12   and SEQ-14    (and not index 'ALL-OTHER-MINERS')
        if blocks.at[i-1, 'MiningPool'] != 'ALL-OTHER-MINERS':
            if cur_seq == 14 or cur_seq == 12:
                print("seq-len:", cur_seq, "pool:", blocks.at[i-1, 'MiningPool'],
                    "block nums:", blocks.at[i - cur_seq, 'number'], blocks.at[i-1, 'number'])
        #END PRINT TMP


        min_pools.at[prevMiner, seq_str] = min_pools.at[prevMiner, seq_str] + 1
        cur_seq = 1

    prevMiner = blocks.at[i, 'MiningPool']

    # need to set len of seq for the last block
    if i == blocks.index[-1]:
        cur_miner = blocks.at[i, 'MiningPool']
        if cur_seq < 15:
            seq_str = "seq_" + str(cur_seq)
        else:
            seq_str = "seq_15"
        min_pools.at[cur_miner, seq_str] = min_pools.at[cur_miner, seq_str] + 1

for i in min_pools.index:
    min_pools.at[i, 'seqVScount'] = min_pools.at[i, 'SameMinSeq'] / min_pools.at[i, 'count']
    min_pools.at[i, 'col_2_4_corel'] = min_pools.at[i, 'seqVScount'] - min_pools.at[i, 'countVStotal']


# drop ALL-OTHER-MINERS
min_pools = min_pools[min_pools.index != 'ALL-OTHER-MINERS']

print(min_pools[['count','countVStotal','seq_1','seq_2','seq_3','seq_4','seq_5','seq_6','seq_7','seq_8',
    'seq_9','seq_10','seq_11','seq_12','seq_13','seq_14','seq_15']])
