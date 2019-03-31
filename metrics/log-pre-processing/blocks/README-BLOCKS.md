(1) go to the folder with all the blocks.log.xx files

(2) copy there ../concatLogs.sh, and all scripts from this folder
    also make sure that you did not forget to do repairLogs.sh first!

(3)$ bash dropDuplicates.sh blocks
(Result) it will create one final unique-unique-blocks.log.FINAL

(4) $ bash dropDuplicates.sh blocksAnnouncements
(Result) it will create one final unique-unique-blockAnnouncements.log.FINAL

(5) python3 showHoles-Blocks.py unique-unique-blocks.log.FINAL
   prints holes in logs... as well as non-sense and eth classic blocs
   manually locate MIN and MAX valid blocknumbers you want to preserve
(5b) python3 extractWeirdBlocks.py unique-unique-blocks.log.FINAL <MIN> <MAX>
   where MIN and MAX are respective blocks (inlcusive) you want to preserve
   it will generate $1.withoutWeirdBlocks and $1.weirdBlocks  files
   in case move possible broken blocks from the first to the second file
(5c) python3 showHoles-Blocks.py unique-unique-blocks.log.FINAL.withoutWeirdBlocks
   final check
(5d) manually:
     $mv unique-unique-blocks.log.FINAL.withoutWeirdBlocks blocks-stage-0.log

(6) $python3 Step-0-Timestamps.py
 this sets the lowest timestamp of block reception and 
 files blocks-stage-0.log and unique-unique-blockAnnouncements.log.FINAL)
 Output: blocks-stage-1.log     (with two more params:  BlockType,CapturedLocally   -both not set)


(7) $python3 Step-1-Import-Missing-Blocks.py blocks-stage-1.log.LOC blocks-stage-1.log.REMOTE  <out-file>

(7a)first on angainor
$python3 Step-1-Import-Missing-Blocks.py blocks-stage-1.log.ANG blocks-stage-1.log.FALC tmp-blcks-A-F
$python3 Step-1-Import-Missing-Blocks.py tmp-blcks-A-F blocks-stage-1.log.S1-US tmp-blcks-A-F-S1
$python3 Step-1-Import-Missing-Blocks.py tmp-blcks-A-F-S1 blocks-stage-1.log.S2-CN tmp-blcks-A-F-S1-S2
$mv tmp-blcks-A-F-S1-S2 blocks-stage-2.log.ANGAINOR


(7b) every machine (except angainor):
$python3 Step-1-Import-Missing-Blocks.py blocks-stage-1.log.LOC blocks-stage-2.log.ANGAINOR blocks-stage-2.log


----
  Output blocks-stage-2.log  
 Merges bloks from REM into LOCAL
 (only the blocks that were missing in local machine)
 also adds two new params: BlockType and CapturedLocally
  BlockType will be empty atm-will be set in next step
  CapturedLocally - True - if the block was there; False -> if it was added in this
  script and in this case, the LocalTimestamp does not count...
---


(7c) python3 Step-1-B-Verify-Holes.py blocks-stage-2.log    # ther must be no HOLES !
     # otherwise, import from etherscan or whatever..


--
from here, it's enough to do it on angainor only
---

(8) python3 Step-2-Set-Main-Blocks.py blocks-stage-2.log
  goes through blocks-stage-2.log and sets the last block's blocktype as 'Main'
  then it goes to that block's parentHash and sets that block as 'Main',
  recursively it does the same till the first block.
  All remaining blocks will be set to 'Uncle'.
  Input blocks-stage-2.log
  Output blocks-stage-3.log (with set BlockType='Main','Uncle')

(9) python3 Step-3-Set-Recognized-Uncles.py blocks-stage-3.log
   sets Uncles that are included in the ListOfUncles property of some block from Main chain as Recognized.
   Output: blocks-stage-4.log with all blocktypes set : Main/Uncle/Recognized (=recognized uncle)

(10) $python3 BlockTypes.py blocks-stage-4.log
   shows some statistics like this:
      Total Blocks:  24574 (Local: 24433 Imported: 141)
      ---
      Main Blocks: 22957 (Local: 22828 Imported: 129)
      Not-recognized Uncles: 25 (Local: 25 Imported: 0)
      Recognized Uncles: 1592 (Local: 1580 Imported: 12)

(11) blocks-stage-4.log is the final log-file to calculate single-node metrics

---

(12) $python3 Step-4-Propagation-Delays.py blocks-stage-2.log.ANGAINOR blocks-stage-2.log.FALCON blocks-stage-2.log.S1-US blocks-stage-2.log.S2-CHINA   (any blocks-2 + )
   Output: blocks-propagation-times.log with delays set, csv-template i nmetrics/multiple-nodes-metrics/5-1..../blocks-propagation-times.csv

   (TODO? if we dicide to use more than two Geth nodes, modify this for more servers...)
