"""
Show the job queue
"""

import subprocess

def queue( all : bool = False ) -> str:
    """
    Show the job queue
    
    Parameters
    ----------
    all : bool
        Show all jobs. By default only the user's jobs are shown.
    
    Returns
    -------
    queue : str
        The job queue as a string.
    """
    cmd = "squeue"
    if not all: 
        cmd += " -A $USER"
    queue = subprocess.run( cmd, shell = True, capture_output = True )
    queue = queue.stdout.decode("utf-8")
    return queue

def view_queue( all : bool = False, refresh : int = 5 ):
    """
    Show the job queue but keep the view open and self-refreshing.
    
    Parameters
    ----------
    all : bool
        Show all jobs. By default only the user's jobs are shown.
    refresh : int
        The number of seconds to wait before refreshing the view.
    """
    queue_cmd = "squeue"
    if not all: 
        queue_cmd += " -A $USER"
        metadata = ("$USER", "'s queue @ ")
    else:
        metadata = ("All jobs", "queued @ ")
        
    cmd = f"""
sleeptime={refresh}

tput sc
while [[ 1 -eq 1 ]]; do 

    # get current time
    current_time=$(date +"%H:%M:%S")

    # display the time with some nice colors 
    echo "--------------------------------------"
    tput setaf 2
    echo -n "{metadata[0]}"
    tput setaf 7
    echo -n "{metadata[1]}"
    tput setaf 6
    echo "$current_time"
    tput setaf 7
    echo "--------------------------------------"

    # call the queue
    q=$({queue_cmd})
    echo "$q"
    
    # now sleep and then clear the current 
    # queue for a new one...
    sleep $sleeptime
    tput rc
    tput ed

    done
    """.strip()
    subprocess.run( cmd, shell = True )