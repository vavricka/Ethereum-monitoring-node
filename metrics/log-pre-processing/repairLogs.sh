#!/bin/sh
#  bash concatLogs txs.log / blocks.log / whatever.log
#        - whichever log that is divided to more logs..

#### rsyslog log-rotation causes that in some cases the last line
#### of a log-file is incorrectly cut and the rest of the line
#### is in the first line of the succeeding log-file
#### this code looks for such occruences and fixes them

LOG_NAME="$1"   #e.g. "txs.log"
NUM=0

if [ ! -f "$LOG_NAME" ] ; then
    echo "$0: \"$LOG_NAME\" log file does not exist!"
    exit 1
fi

if [ ! -f "$LOG_NAME.$((NUM))" ] ; then
    echo "$0: \"$LOG_NAME\" does not exist! - nothing to do"
    echo "the log-rotation bug appears only when at least"
    echo "one $LOG_NAME.x ($LOG_NAME.0) file exists"
    exit 1
fi

NEXT_LOG=""

while true
do
    if [ -f $LOG_NAME.$((NUM+1)) ]
        then
        NEXT_LOG="$LOG_NAME.$((NUM+1))"
    else
        NEXT_LOG="$LOG_NAME"
    fi

    first_line=$(head -n 1 $NEXT_LOG)
    # all valid logs start with 2019-xxx
    # if it doesn't - we must fix it
    if [[ $first_line != 201* ]]
        then

        #just tmp print
        #echo "$LOG_NAME.$((NUM)) tail: $(tail -n 1 $LOG_NAME.$NUM)"
        #echo "$NEXT_LOG head: $first_line"
        echo "$LOG_NAME.$((NUM)): appending $NEXT_LOG's head to it"
        #end tmp print
        
        #### delete the endline byte from the end of log
        #truncate -s -1 $LOG_NAME.$((NUM))
        #### append first line from succeeding log to the end of curr.
        echo "$first_line" >> $LOG_NAME.$((NUM))
    
        ####  delete first line from $NEXT_LOG
        if [ "$(uname)" == "Darwin" ]; then
            sed -i "" '1d' $NEXT_LOG
        elif [ "$(uname)" == "Linux" ]; then
            sed -i '1d' $NEXT_LOG
        fi
    else
          echo "$LOG_NAME.$((NUM)) is OK"
    fi

    if [ "$NEXT_LOG" = "$LOG_NAME" ]
        then
        break
    fi

    NUM=$((NUM+1))
done


#delete last line in last file if broken
last_line=$(tail -n 1 $LOG_NAME)
if [[ $last_line != 201* ]]
    then
    echo "$LOG_NAME deleting it's tail"
    ####  delete last line
    if [ "$(uname)" == "Darwin" ]; then
        #sed -i "" '1d' $NEXT_LOG
        sed -i '' -e '$ d' $NEXT_LOG
    elif [ "$(uname)" == "Linux" ]; then
        #sed -i '1d' $NEXT_LOG
        sed -i '$ d' $NEXT_LOG
    fi
else
    echo "$LOG_NAME is OK"
fi
