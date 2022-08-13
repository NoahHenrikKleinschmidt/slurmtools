"""
Kill a slurm job
"""

import os
import subprocess
import re 

from .last_submit import last_submit, reset_last_submit
from .info import show_all, SlurmJob


def clear_output( jobid : (int or SlurmJob or list), stdout : bool = True, stderr : bool = True ):
    """
    Clear the output of a job. 
    This will remove the stdout and stderr of a job.

    Parameters
    ----------
    jobid : int SlurmJob or list
        The job-id to clear the output of (or a list of jobids).
    stdout : bool
        Clear the stdout of the job.
    stderr : bool
        Clear the stderr of the job.
    """
    if isinstance( jobid, (list, tuple) ):
        [ clear_output( jobid = j, stdout = stdout, stderr = stderr ) for j in jobid ]
        return 
    if not isinstance( jobid, SlurmJob ):
        jobid = SlurmJob( jobid )
    jobid.clear( stdout = stdout, stderr = stderr )
    print( f"Output of job {jobid} cleared" )
    
def kill_last( clear_stdout : bool = False, clear_stderr : bool = False ):
    """
    Kill the last submitted job

    Parameters
    ----------
    clear_stdout : bool
        Remove the stdout of the job.
    clear_stderr : bool
        Remove the stderr of the job.
    """
    kill_job( last = True, clear_stdout = clear_stdout, clear_stderr = clear_stderr )

def kill_all( clear_stdout : bool = False, clear_stderr : bool = False ):
    """
    Kill all jobs

    Parameters
    ----------
    clear_stdout : bool
        Remove the stdout of the job.
    clear_stderr : bool
        Remove the stderr of the job.
    """
    kill_job( all = True, clear_stdout = clear_stdout, clear_stderr = clear_stderr )

def kill_by_pattern( pattern : str, clear_stdout : bool = False, clear_stderr : bool = False ):
    """
    Kill all jobs matching a pattern either in their id or name.

    Parameters
    ----------
    pattern : str
        The regex pattern to match.
    clear_stdout : bool
        Remove the stdout of the job.
    clear_stderr : bool
        Remove the stderr of the job.
    """
    jobs = show_all()
    jobs = [ job for job in jobs if re.search( pattern, str(job.id) ) or re.search( pattern, job.name ) ]
    print( f"Killing jobs: {jobs}" )
    [ job.kill() for job in jobs ]
    if clear_stdout or clear_stderr:
        [ job.clear( stdout = clear_stdout, stderr = clear_stderr ) for job in jobs ]

def kill_job( jobid : int = None, all : bool = False, last : bool = False, clear_stdout : bool = False, clear_stderr : bool = False ):
    """
    Kill a slurm job. 

    Note
    ----
    This will only kill jobs that have been submitted by the user!

    Parameters
    ----------
    jobid : int
        The job-id to kill.
    all : bool
        Kill all jobs.
    last : bool
        Kill the last submitted job.
    clear_stdout : bool
        Remove the stdout of the job.
    clear_stderr : bool
        Remove the stderr of the job.
    """
    if all: 
        cmd = "-A $USER"
    elif last:
        cmd = last_submit()
        reset_last_submit()
        jobid = cmd
    else:
        cmd = f"-A $USER {jobid}" 
    cmd = f"scancel {cmd}"
    subprocess.run( cmd, shell = True )

    if clear_stdout or clear_stderr:
        clear_output( jobid = jobid, stdout = clear_stdout, stderr = clear_stderr )

    print( f"Job {jobid} killed" )
    