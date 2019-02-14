#!/bin/sh
# bash dropDuplicates 

# 3 steps in total
# step 1 - separately call dropDuplicates in each txs.log.x  and produce uniqe-txs.log.x
# step 2 - concatenate the unique-txs.log.x ... into one
# step 3 - call dropDuplicates on the final unique-txs.log...

#start debugging from here
set -x


LOG_NAME="$1".log  #pass blocks (blocks.log)   or blocksAnnouncements (blocksAnnouncements.log)
UNIQUE_LOG="unique-"$1   #check  .....   unique-blocks.log
NUM=0

if [ ! -f "$LOG_NAME" ] ; then
    echo "$0: \"$LOG_NAME\" log file does not exist!"
    exit 1
fi

if [ -f "$UNIQUE_LOG.FINAL" ] ; then
    echo "$0: \"$LOG_NAME.FINAL\" already exists!"
    exit 1
fi

# step 1 - separately call dropDuplicates in each txs.log.x  and produce uniqe-txs.log.x
while true
do
    if [ ! -f "$LOG_NAME.$NUM" ]
        then
        break
    fi

    sudo python3 "$1"-dropDuplicates.py $LOG_NAME.$NUM
    NUM=$((NUM+1))
done
sudo python3 "$1"-dropDuplicates.py $LOG_NAME

# step 2 - concatenate the unique-txs.log.x ... into one
sudo touch $UNIQUE_LOG.FINAL
NUM=0
while true
do
    if [ ! -f "$UNIQUE_LOG.$NUM" ]
        then
        break
    fi

    cat $UNIQUE_LOG.$((NUM)) >> $UNIQUE_LOG.FINAL
    NUM=$((NUM+1))
done
cat $UNIQUE_LOG >> $UNIQUE_LOG.FINAL

# step 3 - call dropDuplicates on the final unique-txs.log...
sudo python3 "$1"-dropDuplicates.py $UNIQUE_LOG.FINAL
