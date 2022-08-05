"""
Show job info
"""

import subprocess
from .SlurmJob import SlurmJob

def show_all( raw = False ): 
    """
    Show all jobs

    Parameters
    ----------
    raw : bool
        Show raw job info.
    
    Returns
    -------
    jobs : list or str
        Either the raw string containing the entire info
        or a list of `SlurmJob` objects.
    """
    cmd = "scontrol show job"
    info = subprocess.run( cmd, shell = True, capture_output = True )
    info = info.stdout.decode("utf-8")
    
    if not raw:
        # split by JobId=
        info = info.split( "JobId=" )

        # now split by space and get the jobid
        info = [ int( i.split(" ")[0] ) for i in info ]

        # now assemble the SlurmJob objects
        info = [ SlurmJob( id ) for id in info ]
    
    return info

def job_info( jobid ):
    """
    Get job info

    Parameters
    ----------
    jobid : str
        The job-id whose info to show.
    
    Returns
    -------
    jobinfo : SlurmJob
        The job info as a `SlurmJob` object.
    """
    jobinfo = SlurmJob( jobid )
    return jobinfo

def raw_job_info( jobid ):
    """
    Show job info

    Parameters
    ----------
    jobid : str
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
