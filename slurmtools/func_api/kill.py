"""
Kill a slurm job
"""

import subprocess
from . import last_submit

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

def kill_job( jobid : str = None, all : bool = False, last : bool = False ):
    """
    Kill a slurm job

    Parameters
    ----------
    jobid : str
        The job-id to kill.
    all : bool
        Kill all jobs.
    last : bool
        Kill the last submitted job.
    """
    if all: 
        cmd = "-A $USER"
    elif last:
        cmd = f"{last_submit.last_submit()}"
    else:
        cmd = f"{jobid}"
    cmd = f"scancel {cmd}"
    subprocess.run( cmd, shell = True )
    
  