"""
Functions to read the stdout or stderr of a job.
"""

from .SlurmJob import SlurmJob

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
    with open( job.stdout , "r" ) as f:
        stdout = f.read()
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
    with open( job.stderr , "r" ) as f:
        stderr = f.read()
    return stderr
