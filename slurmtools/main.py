"""
This is the main command line interface of slurmtools
"""
import argparse
from .__init__ import *


description = """
    slurmtools is a toolset to facilitate working with the SLURM job handler on HPC clusters.
    It provides a set of commands to create, kill, or inspect slurm jobs, and handle the SLURM queue.
    slurmtools is a wrapper around the native SLURM command line interface.
"""

# setup the CLI parser
parser = argparse.ArgumentParser( description = description )
_command = parser.add_subparsers( dest = "command" )

_new = _command.add_parser( 'new', help = 'Submit a new job' )
_new.add_argument( "file", help = "The job file to submit" )

_kill = _command.add_parser( 'kill', help = 'Kill a job' )
_kill.add_argument( "jobid", help = "The job-id to kill, or 'all' to kill all jobs, or 'last' to kill the last submitted job.", default = None )
_kill.add_argument( "-p", "--pattern", help = "Kill all jobs matching a regex pattern in their name or id.", action = "store_true" )

_info = _command.add_parser( 'info', help = 'Show job information' )
_info.add_argument( "jobid", help = "The job-id, or 'all' for all jobs, or 'last' to select only last submitted job." )
_info.add_argument( "-d","--details", help = "Show detailed job info. By default a shortened summary is shown.", action = "store_true" )
_info.add_argument( "-a", "--all", help = "Show all jobs (including ones not from the user)", action = "store_true" )
_info.add_argument( "-p", "--pattern", help = "Show infos to jobs matching a regex pattern in their name or id.", action = "store_true" )

_read = _command.add_parser( 'read', help = "Read a job's stdout or stderr" )
_read.add_argument( "-o", "--stdout", action  = 'store_true', help = "Read the stdout of the job (default)", default = None )
_read.add_argument( "-e", "--stderr", action  = 'store_true', help = "Read the stderr of the job", default = False )
_read.add_argument( "jobid", help = "The job-id whose stdout or stderr to read, or 'last' to read from the last submitted job." )

_interactive = _command.add_parser( 'session', help = 'Start an interactive session' )
_interactive.add_argument( "-d", "--detach", help = "Detach the session using tmux.", action = "store_true" )
_interactive.add_argument( "-s", "--scale", help = "Use a pre-set scale for the interactive session. Use '-s h' / '--scale=h' to view available scales. ", default = None )
_interactive.add_argument( "--name", help = "The name of the session. Defaults to the command used and a timestamp.", default = None )

srun_command = _interactive.add_mutually_exclusive_group()
srun_command.add_argument( "-py", "--python", help = "Activate a python terminal session.", action = "store_true", default = False )
srun_command.add_argument( "-ipy", "--ipython", help = "Activate an ipython terminal session.", action = "store_true", default = False )
srun_command.add_argument( "-r", "--R", help = "Activate an R terminal session.", action = "store_true", default = False )
srun_command.add_argument( "-cmd", "--command", dest = "srun_cmd", help = "The command to run in the srun session. By default 'bash' is used.", default = "bash" )

for p in ( _new, _interactive ) :
    p.add_argument( "-t", "--time", help = "The time limit of the job.", default = None )
    p.add_argument( "-n", "--nodes", type = int, help = "The number of nodes to use.", default = None )
    p.add_argument( "-c", "--cores", type = int, help = "The number of cores to use.", default = None )
    p.add_argument( "-m", "--memory", help = "The amount of memory to use.", default = None )
    p.add_argument( "-p", "--partition", help = "The partition to use.", default = None )

_queue = _command.add_parser( 'queue', help = 'Show the queue' )
_queue.add_argument( "-a", "--all", action = "store_true", help = "Show all jobs. By default only the user's jobs are shown.", default = False )
_queue.add_argument( "-v", "--view", action = "store_true", help = "Keep the queue open as a self-refreshing view" )
_queue.add_argument( "-t", "--time", type = int, help = "The number of seconds to wait between refreshs (default = 5s)", default = 5 )


def main():

    # setup the args by default
    args = parser.parse_args()

    # ----------------------------------------------------
    # New Job Submission
    # ----------------------------------------------------
    if args.command == "new" :
        
        submit( args.file, args )

    # ----------------------------------------------------
    # Kill Jobs
    # ----------------------------------------------------
    if args.command == "kill" :
        
        if args.pattern:
            kill_by_pattern( args.jobid )
        else:
            last = args.jobid == "last"
            all = args.jobid == "all"
            kill_job( args.jobid, all = all, last = last )

    # ----------------------------------------------------
    # Show Job Information
    # ----------------------------------------------------
    if args.command == "info" :
        
        if args.pattern:
            raw = info_by_pattern( args.jobid, mine = not args.all, raw = args.details )
            if not args.details:
                raw = "\n\n".join( [ i._make_summary() for i in raw ] )
            print( raw )
            return            

        if args.jobid == "all":
            raw = show_all( mine = not args.all, raw = args.details )
            if not args.details:
                raw = "\n\n".join( [ i._make_summary() for i in raw ] )
            print( raw )
            return

        jobid = args.jobid
        if args.jobid == "last":
            jobid = last_submit()

            if jobid is None:
                print( "No last job was found. Make sure that you submit jobs using 'slurmtools new' because 'sbatch' submitted jobs are not recorded!" )
                return

        if args.details:
            raw = raw_job_info( jobid )
        else:
            raw = job_info( jobid )
            raw = raw._make_summary()
       
        print( raw )
        
    # ----------------------------------------------------
    # Show Queue
    # ----------------------------------------------------
    if args.command == "queue" :

        if not args.view:
            raw = queue( all = args.all )
            print( raw )
        else:
            view_queue( all = args.all, refresh = args.time )

    # ----------------------------------------------------
    # Interactive srun Session
    # ----------------------------------------------------
    if args.command == "session" :
        
        if args.python:
            srun_command = "python"
        elif args.ipython:
            srun_command = "ipython"
        elif args.R:
            srun_command = "R"
        else:
            srun_command = args.srun_cmd
        
        session( 
                    scale = args.scale,
                    time = args.time, 
                    cpu = args.cores, 
                    memory = args.memory, 
                    detach = args.detach,
                    partition = args.partition, 
                    nodes = args.nodes, 
                    cmd = srun_command,
                    name = args.name,
                )

    # ----------------------------------------------------
    # Read Job Output
    # ----------------------------------------------------
    if args.command == "read" :

        jobid = args.jobid
        if jobid == "last":
            jobid = last_submit()
            if jobid is None:
                print( "No last job was found. Make sure that you submit jobs using 'slurmtools new' because 'sbatch' submitted jobs are not recorded!" )
                return
    
        if args.stdout or ( args.stdout is None and not args.stderr ):
            raw = read_stdout( jobid )
            print( raw )
        if args.stderr:
            raw = read_stderr( jobid )
            print( raw )


if __name__ == "__main__":
    main()