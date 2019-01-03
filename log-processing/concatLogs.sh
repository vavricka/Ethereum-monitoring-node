#!/bin/sh
#  bash concatLogs peers.log
#   loops through   peers.log.0   peers.log.1    ..  peers.log.xx  ...  peers.log
# generates     peers.log.FINAL


LOG_NAME="$1"   # log file's full path - e.g.  "/var/log/txs.log"
NUM=0

if [ ! -f "$LOG_NAME" ] ; then
    echo "$0: \"$LOG_NAME\" log file does not exist!"
    exit 1
fi

if [ -f "$LOG_NAME".FINAL ] ; then
    echo "$0: \"$LOG_NAME.FINAL\" already exists!"
    exit 1
fi


while true
do
    if [ ! -f "$LOG_NAME.$NUM" ]
        then
        break
    fi

    cat $LOG_NAME.$((NUM)) >> $LOG_NAME.FINAL

    NUM=$((NUM+1))
done

cat $LOG_NAME >> $LOG_NAME.FINAL
