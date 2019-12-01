#!/bin/sh

LOG_NAME="$1"   # log file's full path - e.g.  "/var/log/txs.log"
NUM=0

if [ ! -f "$LOG_NAME" ] ; then
    echo "$0: \"$LOG_NAME\" log file does not exist!"
    exit 1
fi

while true
do
    if [ ! -f "$LOG_NAME.$NUM.lzma" ]
        then
        break
    fi
    NUM=$((NUM+1))
done

mv -f $LOG_NAME $LOG_NAME.$((NUM))

lzma -z $LOG_NAME.$((NUM))
