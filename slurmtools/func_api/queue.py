"""
Show the job queue
"""

import curses
import os
import subprocess
import time
from datetime import datetime 
from termcolor import colored


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

def view_queue( all : bool = False, refresh : int = 5, colors : tuple = None ):
    """
    Show the job queue but keep the view open and self-refreshing.
    
    Parameters
    ----------
    all : bool
        Show all jobs. By default only the user's jobs are shown.
    refresh : int
        The number of seconds to wait before refreshing the view.
    colors : tuple
        The colors to use for the first metadata and the timestamp.
    """
    queue_cmd = "squeue"
    if not all: 
        queue_cmd += " -A $USER"
        username = os.environ.get("USER")
        metadata = [username, "'s queue @ "]
    else:
        metadata = ["All jobs", " queued @ "]
    
    # setup the color scheme
    colormaps = {
                    "blue" : curses.COLOR_BLUE,
                    "green" : curses.COLOR_GREEN,
                    "red" : curses.COLOR_RED,
                    "yellow" : curses.COLOR_YELLOW,
                    "cyan" : curses.COLOR_CYAN,
                    "magenta" : curses.COLOR_MAGENTA,
                    "white" : curses.COLOR_WHITE,
                    "black" : curses.COLOR_BLACK,
                }
    if colors is None:
        colors = ("cyan", "green")
    colors = colormaps[ colors[0] ], colormaps[ colors[-1] ]

    

    # # already apply the coloring here
    # metadata[0] = colored( metadata[0], colors[0] )

    try:

        stdscr = curses.initscr()
        stdscr.scrollok(True)
        stdscr.idlok(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, colors[0], -1 )
        curses.init_pair(2, colors[1], -1 )

        while True:
        
            _assemble_viewqueue_output( stdscr, queue_cmd, metadata )
            time.sleep( refresh )

    except KeyboardInterrupt:
        print( "Exiting..." )

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()

def _assemble_viewqueue_output( stdscr, queue_cmd : str, metadata : tuple ):
    """
    Assemble the output of the view_queue function.

    Parameters
    ----------
    queue_cmd : str
        The command to run to get the queue.
    metadata : tuple
        The metadata to show. This contains the info strings to show before the timestamp.
    """

    # get the queue
    queue = subprocess.run( queue_cmd, shell = True, capture_output = True )
    queue = queue.stdout.decode("utf-8")
    q = queue.splitlines()

    # get the maximal length for blank lines
    _lengths = [ len(line) for line in q ]
    # _lengths = [ len(i) for i in queue.splitlines() ]
    max_length = max( _lengths )

    # count lines to add blank line at the end
    lines = len( _lengths )

    # make blank line
    blankline = "-" * max_length


    # get the current time
    timestamp = datetime.now().strftime("%H:%M:%S")

    # get coordinates to add header to in order to centralize
    header_max = len( f"{metadata[0]}{metadata[1]}{timestamp}" )
    header_start = (max_length - header_max) // 2

    header_pad = curses.newwin( 4, max_length, 0, 0 )
    # queue_pad = curses.newpad( lines + 1, max_length )
    # queue_pad = curses.newwin( lines + 1, max_length, 2,0 )
    queue_pad = stdscr.subwin( lines + 1, max_length, 2,0 )
    
    queue_pad.scrollok(True)
    queue_pad.idlok(True)

    # now assemble the whole thing

    header_pad.addstr(0, 0, blankline )

    header_pad.addstr(1, header_start,  metadata[0], curses.color_pair(1) )
    header_pad.addstr(1, header_start+len(metadata[0]),  metadata[1] ) 
    header_pad.addstr(1, header_start+len(metadata[1])+len(metadata[0]), timestamp, curses.color_pair(2) )
    
    header_pad.addstr(2, 0, blankline )

    for idx, line in enumerate(q):
        queue_pad.addstr(lines -1 , 0, line )
        queue_pad.scroll(1)
    # stdscr.addstr(3, 0, queue )
    queue_pad.addstr(lines, 0, blankline)
    
    queue_pad.refresh()
    header_pad.refresh()
    # queue_pad.refresh(0,0, 3,0, 10 , max_length)
    queue_pad.touchwin()
    queue_pad.getch()

#     queue_string = f"""
# #blankline#
# {metadata[0]}{metadata[1]}{timestamp}
# #blankline#
# {queue}
# #blankline#
#     """.strip()
    # max_length = max( [ len(line) for line in queue_string.split("\n") ] )
    # blankline = f"""{"-" * max_length}"""
    # queue_string = queue_string.replace( "#blankline#", blankline )
    # return queue_string

# this is the origiginal code from the view_queue function
    # shell code
#     cmd = f"""
# sleeptime={refresh}

# tput sc
# while [[ 1 -eq 1 ]]; do 

#     # get current time
#     current_time=$(date +"%H:%M:%S")

#     # display the time with some nice colors 
#     echo "--------------------------------------"
#     tput setaf 2
#     echo -n "{metadata[0]}"
#     tput setaf 7
#     echo -n "{metadata[1]}"
#     tput setaf 6
#     echo "$current_time"
#     tput setaf 7
#     echo "--------------------------------------"

#     # call the queue
#     q=$({queue_cmd})
#     echo "$q"
    
#     # now sleep and then clear the current 
#     # queue for a new one...
#     sleep $sleeptime
#     tput rc
#     tput ed

#     done
#     """.strip()
#     try: 
#         subprocess.run( cmd, shell = True )
#     except KeyboardInterrupt:
#         print( "Closing view..." )