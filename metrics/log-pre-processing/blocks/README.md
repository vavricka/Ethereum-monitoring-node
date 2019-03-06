(1) go to the folder with all the blocks.log.xx files

(2) copy there ../concatLogs.sh, and all scripts from this folder

(3)$ sudo bash dropDuplicates.sh blocks
(Result) it will create one final unique-unique-blocks.log.FINAL

(4) $ sudo bash dropDuplicates.sh blocksAnnouncements
(Result) it will create one final unique-unique-blockAnnouncements.log.FINAL

(5) check unique-unique-blocks.log.FINAL for non-sense blocks (e.g. eth classic.)
 using aux/showMissingNewBlocks.py
 (also verify missing blocks.. (look for holes - when peer was down for instance))
 Input : unique-unique-blocks.log.FINAL
 after this is done, rename the file to>  blocks-stage-0.log
 Output :  blocks-stage-0.log

(6) $sudo python3 Step-0-Timestamps.py  
 this sets the lowest timestamp of block reception (from both 
 files blocks-stage-0.log and blocksAnnouncements.log)
 Output: blocks-stage-1.log

(7) $sudo python3 Step-1-Import-Missing-Blocks.py   
 Merges bloks from blocks-stage-1.log.MACHINE-2 into blocks-stage-1.log
 (only the blocks that were missing in local machine)
 also adds two new params: BlockType and CapturedLocally
  BlockType will be empty atm-will be set in next step
  CapturedLocally - True - if the block was there; False -> if it was added in this
  script and in this case, the LocalTimestamp does not count...
  Input: blocks-stage-1.log from various machines
  Output blocks-stage-2.log    with two more params:  BlockType,CapturedLocally
(!) (After this, verify that there are NO HOLES... i.e. blocks and their block-numbers are 
consecutive)
(!) Eventually, modify this script to work with more peers (if we decide to have more peers)

# TODO verify this on last blocks  #


(8) sudo python3 Step-2-Set-Main-Blocks.py    
# TODO   Done but properly check if it works properly
# todo also change .csv .... one more param !!
  goes through blocks-stage-2.log and sets the last block's blocktype as 'Main'
  then it goes to that block's parentHash and sets that block as 'Main',
  recursively it does the same till the first block.
  Input blocks-stage-2.log
  Output blocks-stage-3.log (with set BlockType='Main')

#TODO
(9 TODO) Step-3 ...py script that sets Uncles

Input blocks-stage-3.log
Output blocks-stage-4.log (with set BlockType='Uncle')
#End TODO.




(10) $ sudo python3 BlockTypes.py blocksMergedCheckManuallyNow.log   -> to show if there is need to check the block manually 
(opt)() manually set the blocks with  BlockType==nan or "CheckManually" to Main/Uncle


(11) $sudo python3 Step-4-Set-Recognized-Uncles.py
that sets Uncles into  Recognized or Unrecognized..
#todo one more param..

(11) $sudo python3 BlockTypes.py blocksFinal.log  -> to see how many uncles/recognized..
to verify
#todo  one more param..)

