"""
Show the job queue
"""

import curses
import os
import subprocess
import time
from datetime import datetime 
from pytermwindows import ScrollWindow
import slurmtools.func_api.info as info

# from termcolor import colored

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

class SlurmQueueViewer( ScrollWindow ):
    """
    This class creates a self-renewing window that displays the Slurm Queue in a scrollable field.

    Parameters
    ----------
    all : bool
        Show all jobs. By default only the user's jobs are shown.
    refresh_rate : int
        The refresh rate in seconds.
    """
    __queue_header__ = "JobID   Partition  JobName     User Status   Time    Nodes Nodelist(Reason)"
    def __init__( self, all : bool = False, refresh_rate : int = 1 ):
        super().__init__( name = "Slurm Queue", height = 30, width = 100, start_line = 4, refresh = refresh_rate, use_color = True )
        self.all = all
        self.queue = self._read_queue()
       
    def _read_queue( self ) -> list:
        """
        Read the queue and return a list of all jobs.
        """
        self.queue = queue( all = self.all )
        self.queue = [ i.strip() for i in self.queue.split("\n")[1:] if i != "" ]
        return self.queue

    def _queue_header( self ) -> str:
        """
        Make the header of the queue.
        """

        user = f"{ os.environ.get('USER') }'s" if not self.all else "The whole"
        total = len( user )
        user = self.colored( user, "green" )
        self.write( 1, 0, user )

        mid = " queue at "
        self.write( 1, total, mid )
        total += len(mid)

        timestamp = str( datetime.now().strftime( "%H:%M:%S") )
        timestamp = self.colored( timestamp, "cyan" )
        self.write( 1, total, timestamp )
        total += len(timestamp[0])

        instructions = f"  |  press q to quit, r to refresh"
        self.write( 1, total, instructions )

        total += len( instructions )
        total = max( total, len(self.__queue_header__) )

        blankline = "-" * total
        self.write( 0,0, blankline )
        self.write( 2, 0, blankline )
        self.write( 3, 0, self.__queue_header__ )
        self.write( 4, 0, blankline )

    # def _add_time_bar( self, line ):
    #     """
    #     Add a time bar to a queue line
    #     """
    #     jobid = int( line.split()[0] )
    #     job = info.SlurmJob( jobid )
    #     elapsed = job.time.seconds
    #     remaining = job.time_remaining.seconds
    #     total = elapsed + remaining
    #     elapsed /= total
    #     remaining /= total
    #     full = 30
    #     elapsed = "█" * int( elapsed * full )
    #     remaining = "░" * int( remaining * full )
    #     time_bar = f"{elapsed}{remaining}"

    #     self.write( self.current_line, self.width - full , time_bar )

    def contents( self, **kwargs ):
        """
        The window contents to show the queue
        """

        self._queue_header()

        if self.can_update() or self.keystring == "r":
            self.queue = self._read_queue()
        
        self.to_first_line
        if len(self.queue) == 0:
            self.write( self.to_next_line, 0, "No jobs in queue", clear = True )
        else:
            queue = self.crop_data_to_scroll_range( self.queue )
            for line in queue:
                self.write( self.to_next_line, 0, line )

        # now clear all remaining lines 
        self.clear_line( range( self.next_line, self.bottom_line ) ) 
            
        self.auto_scroll( restrict = len(self.queue)-1 )
        self.quit_on( keystring = "q" )

        self.update_counter()
        self.refresh()


def view_queue( all : bool = False, n : int = 20, refresh : int = 1 ):
    """
    View the queue.
    
    Parameters
    ----------
    all : bool
        Show all jobs. By default only the user's jobs are shown.
    n : int
        The number of jobs to show. By default 20 jobs are shown at a time.
    refresh : int
        The refresh rate in seconds.
    """
    queue_viewer = SlurmQueueViewer( all = all, refresh_rate = 5 )
    queue_viewer.set_update_interval( 0.1 * refresh )
    queue_viewer.set_scroll_range( n )
    queue_viewer.run()

# def view_queue( all : bool = False, refresh : int = 5, colors : tuple = None ):
#     """
#     Show the job queue but keep the view open and self-refreshing.
    
#     Parameters
#     ----------
#     all : bool
#         Show all jobs. By default only the user's jobs are shown.
#     refresh : int
#         The number of seconds to wait before refreshing the view.
#     colors : tuple
#         The colors to use for the first metadata and the timestamp.
#     """
#     queue_cmd = "squeue"
#     if not all: 
#         queue_cmd += " -A $USER"
#         username = os.environ.get("USER")
#         metadata = [username, "'s queue @ "]
#     else:
#         metadata = ["All jobs", " queued @ "]
    
#     # setup the color scheme
#     colormaps = {
#                     "blue" : curses.COLOR_BLUE,
#                     "green" : curses.COLOR_GREEN,
#                     "red" : curses.COLOR_RED,
#                     "yellow" : curses.COLOR_YELLOW,
#                     "cyan" : curses.COLOR_CYAN,
#                     "magenta" : curses.COLOR_MAGENTA,
#                     "white" : curses.COLOR_WHITE,
#                     "black" : curses.COLOR_BLACK,
#                 }
#     if colors is None:
#         colors = ("cyan", "green")
#     colors = colormaps[ colors[0] ], colormaps[ colors[-1] ]

    

#     # # already apply the coloring here
#     # metadata[0] = colored( metadata[0], colors[0] )

#     try:

#         stdscr = curses.initscr()
#         stdscr.scrollok(True)
#         stdscr.idlok(True)
#         curses.noecho()
#         curses.cbreak()
#         curses.start_color()
#         curses.use_default_colors()
#         curses.init_pair(1, colors[0], -1 )
#         curses.init_pair(2, colors[1], -1 )

#         while True:
        
#             _assemble_viewqueue_output( stdscr, queue_cmd, metadata )
#             time.sleep( refresh )

#     except KeyboardInterrupt:
#         print( "Exiting..." )

#     finally:
#         curses.echo()
#         curses.nocbreak()
#         curses.endwin()

# def _assemble_viewqueue_output( stdscr, queue_cmd : str, metadata : tuple ):
#     """
#     Assemble the output of the view_queue function.

#     Parameters
#     ----------
#     queue_cmd : str
#         The command to run to get the queue.
#     metadata : tuple
#         The metadata to show. This contains the info strings to show before the timestamp.
#     """

#     # get the queue
#     queue = subprocess.run( queue_cmd, shell = True, capture_output = True )
#     queue = queue.stdout.decode("utf-8")
#     q = queue.splitlines()

#     # get the maximal length for blank lines
#     _lengths = [ len(line) for line in q ]
#     # _lengths = [ len(i) for i in queue.splitlines() ]
#     max_length = max( _lengths )

#     # count lines to add blank line at the end
#     lines = len( _lengths )

#     # make blank line
#     blankline = "-" * max_length


#     # get the current time
#     timestamp = datetime.now().strftime("%H:%M:%S")

#     # get coordinates to add header to in order to centralize
#     header_max = len( f"{metadata[0]}{metadata[1]}{timestamp}" )
#     header_start = (max_length - header_max) // 2

#     header_pad = curses.newwin( 4, max_length, 0, 0 )
#     # queue_pad = curses.newpad( lines + 1, max_length )
#     # queue_pad = curses.newwin( lines + 1, max_length, 2,0 )
#     queue_pad = stdscr.subwin( lines + 1, max_length, 2,0 )
    
#     queue_pad.scrollok(True)
#     queue_pad.idlok(True)

#     # now assemble the whole thing

#     header_pad.addstr(0, 0, blankline )

#     header_pad.addstr(1, header_start,  metadata[0], curses.color_pair(1) )
#     header_pad.addstr(1, header_start+len(metadata[0]),  metadata[1] ) 
#     header_pad.addstr(1, header_start+len(metadata[1])+len(metadata[0]), timestamp, curses.color_pair(2) )
    
#     header_pad.addstr(2, 0, blankline )

#     for idx, line in enumerate(q):
#         queue_pad.addstr(lines -1 , 0, line )
#         queue_pad.scroll(1)
#     # stdscr.addstr(3, 0, queue )
#     queue_pad.addstr(lines, 0, blankline)
    
#     queue_pad.refresh()
#     header_pad.refresh()
#     # queue_pad.refresh(0,0, 3,0, 10 , max_length)
#     queue_pad.touchwin()
#     queue_pad.getch()

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