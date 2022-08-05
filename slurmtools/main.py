"""
This is the main command line interface of slurmtools
"""
import argparse
from .__init__ import *

def setup_parser():
    description = """
        slurmtools is a toolset for slurm.
        It provides a set of commands to manage slurm jobs,
        and is a wrapper around the slurm command line interface.
    """

    parser = argparse.ArgumentParser( description = description )
    command = parser.add_subparsers( dest = "command" )

    new = command.add_parser( 'new', help = 'Submit a new job' )
    submit = command.add_parser( 'submit', help = 'Submit a new job' )
    for p in [ new, submit ]:
        p.add_argument( "file", help = "The job file to submit" )

    interactive = command.add_parser( 'session', help = 'Start an interactive session' )
    run = command.add_parser( 'run', help = 'Start an interactive session' )
    for p in [ new, submit, interactive, run ]:
        p.add_argument( "-t", "--time", help = "The time limit of the job.", default = None )
        p.add_argument( "-n", "--nodes", type = int, help = "The number of nodes to use.", default = None )
        p.add_argument( "-c", "--cores", type = int, help = "The number of cores to use.", default = None )
        p.add_argument( "-m", "--memory", help = "The amount of memory to use.", default = None )
        p.add_argument( "-p", "--partition", help = "The partition to use.", default = None )
    
    for p in [ interactive, run ]:
        p.add_argument( "-d", "--detach", help = "Detach the session using tmux.", action = "store_true" )

    stop = command.add_parser( 'stop', help = 'Kill a job' )
    kill = command.add_parser( 'kill', help = 'Kill a job' )
    for p in [ stop, kill ]:
        p.add_argument( "jobid", help = "The job-id to kill, or 'all' to kill all jobs, or 'last' to kill the last submitted job.", default = None )
       
    show = command.add_parser( 'show', help = 'Show job information' )
    info = command.add_parser( 'info', help = 'Show job information' )
    for p in [ show, info ]:
        p.add_argument( "jobid", help = "The job-id to show, or 'all' to show details of all jobs, or 'last' to show only details of the last submitted job." )

    queue = command.add_parser( 'queue', help = 'Show the queue' )
    for p in [ queue ]:
        p.add_argument( "-a", "--all", action = "store_true", help = "Show all jobs. By default only the user's jobs are shown.", default = False )
        p.add_argument( "-v", "--view", action = "store_true", help = "Keep the queue open as a self-refreshing view" )
        p.add_argument( "-t", "--time", type = int, help = "The number of seconds to wait between refreshs (default = 5s)", default = 5 )
    
    return parser

def get_args():
    """
    Gets the command line arguments
    """
    parser = setup_parser()
    args = parser.parse_args()
    return args



def main():

    # setup the args by default
    args = get_args()

    # ----------------------------------------------------
    # New Job Submission
    # ----------------------------------------------------
    if args.command in ["new", "submit"]:
        
        submit( args.file, args )

    # ----------------------------------------------------
    # Kill Jobs
    # ----------------------------------------------------
    if args.command in ["stop", "kill"]:
        
        last = args.jobid == "last"
        all = args.jobid == "all"
        kill_job( args.jobid, all = all, last = last )

    # ----------------------------------------------------
    # Show Job Information
    # ----------------------------------------------------
    if args.command in ["show", "info"]:
        
        if args.jobinfo == "all":
            raw = show_all( raw = True )
        elif args.jobinfo == "last":
            raw = raw_job_info( last_submit.last_submit() )
        else:
            raw = raw_job_info( args.jobid )
        print( raw )
        
    # ----------------------------------------------------
    # Show Queue
    # ----------------------------------------------------
    if args.command == "queue":

        if not args.view:
            raw = queue( all = args.all )
            print( raw )
        else:
            view_queue( all = args.all, refresh = args.time )

    # ----------------------------------------------------
    # Interactive srun Session
    # ----------------------------------------------------
    if args.command in ["interactive", "run"]:
        session( 
                    time = args.time, 
                    nodes = args.nodes, 
                    cores = args.cores, 
                    memory = args.memory, 
                    partition = args.partition, 
                    detach = args.detach 
                )

if __name__ == "__main__":
    main()