"""
Kill a slurm job
"""

import subprocess
import re 

from .last_submit import last_submit, reset_last_submit
from .info import show_all


def kill_last():
    """
    Kill the last submitted job
    """
    kill_job( last = True )

def kill_all():
    """
    Kill all jobs
    """
    kill_job( all = True )

def kill_by_pattern( pattern : str ):
    """
    Kill all jobs matching a pattern either in their id or name.

    Parameters
    ----------
    pattern : str
        The regex pattern to match.
    """
    jobs = show_all()
    jobs = [ job for job in jobs if re.search( pattern, str(job.id) ) or re.search( pattern, job.name ) ]
    [ kill_job( job.id ) for job in jobs ]

def kill_job( jobid : int = None, all : bool = False, last : bool = False ):
    """
    Kill a slurm job

    Parameters
    ----------
    jobid : int
        The job-id to kill.
    all : bool
        Kill all jobs.
    last : bool
        Kill the last submitted job.
    """
    if all: 
        cmd = "-A $USER"
    elif last:
        cmd = last_submit()
        reset_last_submit()
    else:
        cmd = f"-A $USER {jobid}" 
    cmd = f"scancel {cmd}"
    subprocess.run( cmd, shell = True )
    