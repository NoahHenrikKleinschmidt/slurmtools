#!bin/bash

# ----------------------------------------------------
# show the slurm queue 
# ----------------------------------------------------
function myqueue {
					squeue -A ${USER}
				}

function myq {
					myqueue 
			}


# A static window that will self-update and show the queue 
# renewed in a given time frame...
function viewmyqueue() {
    # get the number of seconds to sleep
    # if none are specified then just set
    # to default 15 seconds...
    sleeptime=$1
    if [[ $sleeptime == "" ]]; then
        sleeptime=15
    fi

    tput sc
    while [[ 1 -eq 1 ]]; do 

        # get current time
        current_time=$(date +"%H:%M:%S")

        # display the time with some nice colors 
        echo "--------------------------------------"
        tput setaf 2
        echo -n "$USER"
        tput setaf 7
        echo -n "'s queue @ "
        tput setaf 6
        echo "$current_time"
        tput setaf 7
        echo "--------------------------------------"

        # call myq
        q=$(myq)
        echo "$q"
        
        # now sleep and then clear the current 
        # queue for a new one...
        sleep $sleeptime
        tput rc
		tput ed

    done

}

function vmyq() {
					viewmyqueue $1
			}

function viewmyq() {
					viewmyqueue $1
				}