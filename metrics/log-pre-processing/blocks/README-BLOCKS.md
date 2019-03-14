(1) go to the folder with all the blocks.log.xx files

(2) copy there ../concatLogs.sh, and all scripts from this folder
    also make sure that you did not forget to do repairLogs.sh first!

(3)$ bash dropDuplicates.sh blocks
(Result) it will create one final unique-unique-blocks.log.FINAL

(4) $ bash dropDuplicates.sh blocksAnnouncements
(Result) it will create one final unique-unique-blockAnnouncements.log.FINAL

(5) python3 showHoles-Blocks.py unique-unique-blockAnnouncements.log.FINAL
   prints holes in logs... as well as non-sense and eth classic blocs
   manually locate MIN and MAX valid blocknumbers you want to preserve
(5b) python3 extractWeirdBlocks unique-unique-blockAnnouncements.log.FINAL MIN MAX
   where MIN and MAX are respective blcoks (inlcusive) you want to preserve
   it will generate $1.withoutWeirdBlocks and $1.weirdBlocks  files
   in case move possible broken blocks from the first to the second file
(5c) python3 showHoles-Blocks.py $1.withoutWeirdBlocks
   final check
(5d) manually rename  unique-unique-blockAnnouncements.log.FINAL.withoutWeirdBlocks
     to blocks-stage-0.log

(6) $python3 Step-0-Timestamps.py
 this sets the lowest timestamp of block reception (from both 
 files blocks-stage-0.log and blocksAnnouncements.log)
 Output: blocks-stage-1.log

(7) $python3 Step-1-Import-Missing-Blocks.py blocks-stage-1.log.LOC blocks-stage-1.log.REM
  Output blocks-stage-2.log   (with two more params:  BlockType,CapturedLocally)
 Merges bloks from REM into LOCAL
 (only the blocks that were missing in local machine)
 also adds two new params: BlockType and CapturedLocally
  BlockType will be empty atm-will be set in next step
  CapturedLocally - True - if the block was there; False -> if it was added in this
  script and in this case, the LocalTimestamp does not count...

(7b) python3 Step-1-B-Verify-Holes.py blocks-stage-2.log    # ther must be no HOLES !
     # otherwise, import from etherscan or whatever..

(8) python3 Step-2-Set-Main-Blocks.py blocks-stage-2.log
  goes through blocks-stage-2.log and sets the last block's blocktype as 'Main'
  then it goes to that block's parentHash and sets that block as 'Main',
  recursively it does the same till the first block.
  All remaining blocks will be set to 'Uncle'.
  Input blocks-stage-2.log
  Output blocks-stage-3.log (with set BlockType='Main','Uncle')
  (! if you pass e.g blocks-stage-2.log.ANGAINOR don't forget to rename)
  (! blocks-stage-3.log to blocks-stage-3.log.ANGAINOR)

# !!! For now ommited -> thus blocks-stage-3.log is the final stage
# !!! Block Type is only Main/Uncle      
#(9 TODO) Step-3-Set-Recognized-Uncles.py blocks-stage-3.log
#  sets Uncles that are included in the ListOfUncles property of some block from Main chain as Recognized.
#  Output: blocks-stage-4.log with all blocktypes set : Main/Uncle/Recognized (=recognized uncle)

(10) $python3 BlockTypes.py blocks-stage-3.log
 shows some statistics like this:
  Main: 15098 (Local: 15030 Imported: 68)
  Uncle: 1148 (Local: 1135 Imported: 13)
  Recognized: 0 (Local: 0 Imported: 0)

