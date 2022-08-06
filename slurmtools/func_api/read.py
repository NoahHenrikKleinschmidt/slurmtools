"""
Functions to read the stdout or stderr of a job.
"""

import os
from .info import SlurmJob

def read_stdout( jobid : int ) -> str:
    """
    Read the stdout of a job.

    Parameters
    ----------
    jobid : int
        The job-id whose stdout to read.
    
    Returns
    -------
    stdout : str
        The stdout of the job.
    """
    job = SlurmJob( jobid )
    if os.path.exists( job.stdout ):
        with open( job.stdout , "r" ) as f:
            stdout = f.read()
    else:
        print( "The stdout file does not exist (yet)." ) 
        return
    return stdout



def read_stderr( jobid : int ) -> str:
    """
    Read the stderr of a job.

    Parameters
    ----------
    jobid : int
        The job-id whose stderr to read.
    
    Returns
    -------
    stderr : str
        The stderr of the job.
    """
    job = SlurmJob( jobid )
    if os.path.exists( job.stderr ):
        with open( job.stderr , "r" ) as f:
            stderr = f.read()
    else:
        print( "The stderr file does not exist (yet)." ) 
        return
    return stderr
