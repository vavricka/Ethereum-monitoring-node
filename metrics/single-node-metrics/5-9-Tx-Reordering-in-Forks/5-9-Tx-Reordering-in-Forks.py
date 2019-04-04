#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import textdistance
from itertools import chain

if len(sys.argv) != 2:
    sys.exit(sys.argv[0], ": expecting one parameter")

BLOCKS_LOG = sys.argv[1]   # blocks-stage-4.log

#check - that log-file exists
if not os.path.isfile(BLOCKS_LOG):
    sys.exit(BLOCKS_LOG, ": does not exists!")

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
        'ForkLength'        : 'int',
        }

blocks = pd.read_csv(BLOCKS_LOG, 
    names=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength'],
    dtype=dtypes_blocks)

#sort by Number
blocks.sort_values(by=['Number'], inplace=True)
blocks.reset_index(inplace=True, drop=True)

#add columns
blocks = blocks.assign(NumTxs = 0, NumTxsInCorrespondingMain = 0, NumCommonTxs = 0,
    JaroCommonTxsOnly = 0.0, JaroAllTxs = 0.0,
    uncleTxsString = "", mainTxsString = "")

uncles = blocks[(blocks.BlockType == "Uncle") | (blocks.BlockType == "Recognized")]
uncles.reset_index(inplace=True, drop=True)

main_blocks = blocks[blocks.BlockType == "Main"]
main_blocks.reset_index(inplace=True, drop=True)


for id_block, row in uncles.iterrows():
    cur_block_num = row['Number']

    # search  main block with the same block number
    try:
        line = main_blocks['Number'].searchsorted(cur_block_num)
        if main_blocks.at[line,'Number'] == cur_block_num:
            #all good
            pass
        else:
            print("!!! there is no main block for", row['BlockHash'], "with number", cur_block_num)
            continue
    except (IndexError, KeyError) as e:
        print("!!!! there is no main block for", row['BlockHash'], "with number", cur_block_num)
        continue

    #txs in UNCLE
    try:
        uncle_txs = row['ListOfTxs'].split(";")
        #remove empty lines (there is always one empty line at the end of the list)
        uncle_txs = list(filter(None, uncle_txs))
        num_txs_in_uncle_block = len(uncle_txs)
    except AttributeError:
        num_txs_in_uncle_block = 0

    #print("number of txs in uncle block:", num_txs_in_uncle_block)
    uncles.at[id_block, 'NumTxs'] = num_txs_in_uncle_block

    #txs in MAIN
    try:
        main_txs = main_blocks.at[line,'ListOfTxs'].split(";")
        #remove empty lines (there is always one empty line at the end of the list)
        main_txs = list(filter(None, main_txs))
        num_txs_in_main_block = len(main_txs)
    except AttributeError:
        num_txs_in_main_block = 0

    #print("number of txs in main block:", num_txs_in_main_block)
    uncles.at[id_block, 'NumTxsInCorrespondingMain'] = num_txs_in_main_block

    if (num_txs_in_main_block == 0) | (num_txs_in_uncle_block == 0):
        uncles.at[id_block, 'NumCommonTxs'] = 0
        if (num_txs_in_main_block == 0) & (num_txs_in_uncle_block == 0):
            #print("JARO   1 ..  cuz both 0")
            uncles.at[id_block, 'JaroCommonTxsOnly'] = 1
            uncles.at[id_block, 'JaroAllTxs'] = 1
        else:
            #print("JARO   0 ..  cuz one has 0 txs and the other has some")
            uncles.at[id_block, 'JaroCommonTxsOnly'] = 0
            uncles.at[id_block, 'JaroAllTxs'] = 0
            uncles.at[id_block, 'JaroAllTxs'] = 0

        continue
    
    #else both contain some txs... we can calculate jaro

    #common txs in both lists
    set_common_txs = set(uncle_txs).intersection(main_txs)
    num_common_txs_in_both_blocks = len(set_common_txs)
    #print("number of txs that are both in main and uncle blocks:",num_common_txs_in_both_blocks)
    uncles.at[id_block, 'NumCommonTxs'] = num_common_txs_in_both_blocks

    #generate a range of valid visible unicode characters used for converting hashes to unique chars
    # A-Z,  a-z, then some another visible chars;    (there never are more than 400 txs in a block..)
    # it could simply be just e.g. range(0,1000); we use 65-91 (AZ), 97-123 (az) etc. becasue if we
    # print them out, to look good
    ranges = chain(range(65,91), range(97, 123), range(942, 1367), range(384, 451))
    #ranges_main = chain(range(2306,2436), range(3840,3948), range(4608, 4681), range(4256,4293), range(4352,4441))
    ranges_main = range(3000,4000)
    #ranges_uncle = chain( range(5024,5108), range(5150,5555) )
    ranges_uncle =  range(5000,6000)

    # in both,  sets all hashes from common_txs
    for tx, i  in zip(set_common_txs, ranges):
        main_txs[main_txs.index(tx)] = chr(i)
        uncle_txs[uncle_txs.index(tx)] = chr(i)

    #create string
    main_txs_common_string = ""
    main_txs_complete_string = ""
    for tx, i in zip(main_txs, ranges_main):
        if len(tx) == 1:
            main_txs_common_string = main_txs_common_string + tx
            main_txs_complete_string = main_txs_complete_string + tx
        else:
            main_txs[main_txs.index(tx)] = chr(i)
            main_txs_complete_string = main_txs_complete_string + chr(i)

    #print(main_txs_common_string)
    #print(main_txs_complete_string)

    #create string
    uncle_txs_common_string = ""
    uncle_txs_complete_string = ""
    for tx, i in zip(uncle_txs, ranges_uncle):
        if len(tx) == 1:
            uncle_txs_common_string = uncle_txs_common_string + tx
            uncle_txs_complete_string = uncle_txs_complete_string + tx
        else:
            uncle_txs[uncle_txs.index(tx)] = chr(i)
            uncle_txs_complete_string = uncle_txs_complete_string + chr(i)

    #print(uncle_txs_common_string)
    #print(uncle_txs_complete_string)

    jaro_common_txs = textdistance.jaro(main_txs_common_string, uncle_txs_common_string)
    #print("JARO - common hashes only:", jaro_common_txs)
    jaro_all_txs = textdistance.jaro(main_txs_complete_string, uncle_txs_complete_string)

    uncles.at[id_block, 'uncleTxsString'] = uncle_txs_common_string
    uncles.at[id_block, 'mainTxsString'] = main_txs_common_string

    uncles.at[id_block, 'JaroCommonTxsOnly'] = jaro_common_txs
    uncles.at[id_block, 'JaroAllTxs'] = jaro_all_txs


# log file used in 5-9-Plot.py
uncles.to_csv("5-9-uncles-jaro.log", index=False, header=False,
    columns=['LocalTimeStamp','BlockHash','Number','GasLimit','GasUsed','Difficulty','Time',
    'Coinbase','ParentHash','UncleHash','BlockSize','ListOfTxs','ListOfUncles',
    'CapturedLocally','BlockType','ForkLength',
    'NumTxs', 'NumTxsInCorrespondingMain', 'NumCommonTxs', 'JaroCommonTxsOnly', 'JaroAllTxs'])

# csv for teachers with numbers..
#uncles.to_csv("uncles-jaro.csv", index=False, header=True,
#columns=['Number', 'NumTxs', 'NumTxsInCorrespondingMain', 'NumCommonTxs', 'JaroCommonTxsOnly', 'JaroAllTxs','uncleTxsString','mainTxsString'])
