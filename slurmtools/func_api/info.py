"""
Show job info
"""

import subprocess
from .SlurmJob import SlurmJob

def show_all( mine : bool = True, raw : bool = False ): 
    """
    Show all jobs

    Parameters
    ----------

    mine : bool
        Only include jobs owned by the current user.

    raw : bool
        Show raw job info. This will be detailed.
    
    Returns
    -------
    jobs : list or str
        Either the raw string containing the entire info
        or a list of `SlurmJob` objects.
    """
    cmd = "scontrol show job"
    info = subprocess.run( cmd, shell = True, capture_output = True )
    info = info.stdout.decode("utf-8")
    
    # split by JobId=
    info = info.split( "JobId=" )

    # extract all jobs of the users
    if mine:
        username = subprocess.run( "whoami", shell = True, capture_output = True ).stdout.decode("utf-8")
        username = f"Account={username}".strip()
        info = [ i for i in info if username in i ]
    
    # now convert to SlurmJob objects
    if not raw:

        # now split by space and get the jobid
        info = [ int( i.split(" ")[0] ) for i in info ]

        # now assemble the SlurmJob objects
        info = [ SlurmJob( id ) for id in info ]
    
    # or re-assemble the string
    else:
        info = [ f"JobId={i}" for i in info ]
        info = "\n\n".join( info )
    
    return info

def job_info( jobid : int ):
    """
    Get job info

    Parameters
    ----------
    jobid : int
        The job-id whose info to show.
    
    Returns
    -------
    jobinfo : SlurmJob
        The job info as a `SlurmJob` object.
    """
    jobinfo = SlurmJob( jobid )
    return jobinfo

def raw_job_info( jobid : int ):
    """
    Show job info

    Parameters
    ----------
    jobid : int
        The job-id whose info to show.
    
    Returns
    -------
    jobinfo : str
        The job info as a raw string.
    """
    cmd = f"scontrol show jobid -dd {jobid}"
    jobinfo = subprocess.run( cmd, shell = True, capture_output = True )
    jobinfo = jobinfo.stdout.decode("utf-8")
    return jobinfo

def job_summary( jobid : int ):
    """
    Show job summary

    Parameters
    ----------
    jobid : int
        The job-id whose summary to show.
    
    Returns
    -------
    summary : str
        The job summary as a raw string.
    """
    job = SlurmJob( jobid )
    return job._make_summary()