"""
Show job info
"""

import os
import subprocess
from datetime import datetime
import pandas as pd
import re

import logging

logger = logging.getLogger( "slurmtools" )

from .last_submit import last_submit

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

def info_by_pattern( pattern : str, mine : bool = True, raw : bool = False ):
    """
    Show job info for jobs matching a certain pattern in their names or ids.
    
    Parameters
    ----------
    pattern : str
        The regex pattern to match.
    mine : bool
        Only include jobs owned by the current user.
    raw : bool
        Show raw job info. This will be detailed.
    
    Returns
    -------
    jobs : list or str
        Either the raw string containing the entire info or a list of `SlurmJob` objects.
    """
    jobs = show_all( mine = mine )
    jobs = [ job for job in jobs if re.search( pattern, str(job.id) ) or re.search( pattern, job.name ) ]

    if raw:
        jobs = "\n\n".join( [ job.info for job in jobs ] )
    return jobs

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
    if jobid is None:
        return None

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
    if jobid is None:
        return None
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
    if jobid is None:
        return None

    job = SlurmJob( jobid )
    return job._make_summary()


class SlurmJob:
    """
    A class to represent a slurm job.
    It extracts various details from the slurm info command, 
    and returns them in useable format. 
    Also, the job can be killed via this class.

    Parameters
    ----------
    id : int
        The job-id of the job to be represented.
    """
    def __init__( self, id ):
        if isinstance( id, str ):
            if id == "last":
                id = last_submit()
            else:
                id = int( id )
        elif isinstance( id, float ):
            id = int( id )
    
        if not isinstance( id, int ):
            raise ValueError( "id must be an int or a str that can be converted to int" )

        self.id = id
        self.info = self.get_info()
    
    def kill(self):
        """
        Kill the job
        """
        from .kill import kill_job
        kill_job( self.id )
    
    def get_info( self ) -> str:
        """
        Get raw job info
        """
        self.info = raw_job_info( self.id )
        return self.info

    def summary( self ):
        """
        Prints a shortened version of the job info.
        """
        string = self._make_summary()
        print( string )

    def clear( self, stdout : bool = True, stderr : bool = True ):
        """
        Clear the stdout and stderr of the job. This will remove the job's 
        stdout and stderr files if they exist.

        Parameters
        ----------
        stdout : bool   
            Remove the stdout file.
        stderr : bool
            Remove the stderr file.
        """
        if stdout and os.path.exists( self.stdout ):
            os.remove( self.stdout )
        if stderr and os.path.exists( self.stderr ):
            os.remove( self.stderr )

    @property
    def jobid( self ) -> int:
        """
        Get job-id
        """
        return self.id
    
    @property
    def user( self ) -> str:
        """
        Get user who submitted the job
        """
        pattern = "Account=([a-zA-Z0-9/_\.\\\-]*)"
        user = re.search( pattern, self.info ).group(1)
        return user

    @property
    def name( self ) -> str:
        """
        Get job name
        """
        pattern = "JobName=([a-zA-Z0-9/_\. \\\-]*)"
        name = re.search( pattern, self.info ).group(1)
        return name
    
    @property
    def state( self ):
        """
        Get job state
        """
        pattern = "JobState=([A-Z]*)"
        state = re.search( pattern, self.info )
        if state: 
            state = state.group(1)
        return state
    
    @property
    def state_reason( self ) -> str:
        """
        Get job state reason
        """
        pattern = "Reason=([A-Z0-9a-z()\-_\.,]*)"
        state = re.search( pattern, self.info )
        if state:
            state = state.group(1)
        if state == "None":
            state = None
        return state

    @property
    def time( self ) -> pd.Timedelta:
        """
        Get job runtime
        """
        pattern = "RunTime=([0-9 \- :]*)"
        time = re.search( pattern, self.info ).group(1)
        try: 
            days = 0
            if "-" in time:
                days, time = time.split("-")
                days = int(days)
            hours, minutes, seconds = tuple( map( int, time.split(":") ) ) 
            time = pd.Timedelta( days=days, hours=hours, minutes=minutes, seconds=seconds )
                
        except Exception as e:
            logger.debug( e )
        return time
    
    @property
    def start( self ) -> pd.Timestamp:
        """
        Get job start time
        """
        pattern = "StartTime=([0-9T \- :]*)"
        time = re.search( pattern, self.info ).group(1)
        try: 
            time = pd.to_datetime( time )
        except Exception as e:
            logger.debug( e )
        return time
    
    @property
    def end( self ) -> pd.Timestamp:
        """
        Get job end time
        """
        pattern = "EndTime=([0-9T \- :]*)"
        time = re.search( pattern, self.info ).group(1)
        try: 
            time = pd.to_datetime( time )
        except Exception as e:
            logger.debug( e )
        return time

    @property
    def time_remaining( self ) -> pd.Timedelta:
        """
        Get job's time remaining to finish
        """
        try:
            remaining = self.end - datetime.now()
            remaining = remaining.round( "S" )
            return remaining
        except Exception as e:
            logger.debug( e )
            logger.warning( "Could not establish remaining time. Probably due to unknown string format in end time.")
            return None
    @property
    def nodes( self ) -> str:
        """
        Get job nodes
        """
        pattern = "Nodes=([a-zA-Z0-9/_\.\\\-]*)"
        nodes = re.search( pattern, self.info )
        if nodes:
            nodes = nodes.group(1)
        return nodes
    
    @property
    def cores( self ) -> int:
        """
        Get the number of cores
        """
        pattern = "NumCPUs=([0-9]*)"
        cores = re.search( pattern, self.info )
        if cores:
            cores = cores.group(1)
            cores = int( cores )
        return cores
    
    @property
    def memory( self ) -> int:
        """
        Get the memory assignment
        """
        pattern = "Mem=([0-9]*)"
        memory = re.search( pattern, self.info )
        if memory: 
            memory = memory.group(1)
            memory = int( memory )
        return memory

    @property
    def partition( self ) -> str:
        """
        Get the partition
        """
        pattern = "Partition=([a-zA-Z0-9/_\.\\\-]*)"
        partition = re.search( pattern, self.info )
        if partition:
            partition = partition.group(1)
        return partition
    
    @property
    def command( self ) -> str:
        """
        Get the command
        """
        pattern = "Command=([a-zA-Z0-9 / _ \. \\ \-]*)"
        command = re.search( pattern, self.info ).group(1)
        return command
    
    @property
    def exit_code( self ) -> int:
        """
        Get the exit code
        """
        pattern = "ExitCode=([0-9])"
        exit_code = re.search( pattern, self.info ).group(1)
        exit_code = int( exit_code )
        return exit_code
    
    @property
    def stdin( self ) -> str:
        """
        Get the stdin
        """
        pattern = "StdIn=([a-zA-Z0-9 / _ \. \\ \-]*)"
        stdin = re.search( pattern, self.info )
        if stdin:
            stdin = stdin.group(1)
        return stdin
    
    @property
    def stdout( self ) -> str:
        """
        Get the stdout
        """
        pattern = "StdOut=([a-zA-Z0-9 / _ \. \\ \-]*)"
        stdout = re.search( pattern, self.info )
        if stdout:
            stdout = stdout.group(1)
        return stdout
    
    @property
    def stderr( self ) -> str:
        """
        Get the stderr
        """
        pattern = "StdErr=([a-zA-Z0-9 / _ \. \\ \-]*)"
        stderr = re.search( pattern, self.info )
        if stderr:
            stderr = stderr.group(1)
        return stderr
    
    @property
    def workdir( self ) -> str:
        """
        Get the working directory
        """
        pattern = "WorkDir=([a-zA-Z0-9 / _ \. \\ \-]*)"
        workdir = re.search( pattern, self.info )
        if workdir:
            workdir = workdir.group(1)
        return workdir

    def _make_summary( self ) -> str:
        """
        Generates the summary string for the summary() method.
        """
        state_reason = "" if not self.state_reason else f"({self.state_reason})"
        filler = "### blank line ###"
        string = f"""
{filler}
General Info
{filler}

Job ID:     {self.id}
Job Name:   {self.name}
User:       {self.user}
State:      {self.state} {state_reason}

Runtime:    {self.time}
Time limit: {self.time_remaining} ({self.end})

{filler}
Technical Info
{filler}
Cmd:        {self.command}
Stdin:      {self.stdin}
Stdout:     {self.stdout}
Stderr:     {self.stderr}
{filler}
Resource Info
{filler}
Nodes:      {self.nodes}
Cores:      {self.cores}
Memory:     {self.memory}
Partition:  {self.partition}
{filler}
        """.strip()
        max_length = max( [ len(i) for i in string.split("\n") ] )
        lines = "-" * max_length
        string = string.replace( filler, lines )
        return string

    def __repr__( self ) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
    
    def __str__( self ) -> str:
        return f"[Job {self.id}] {self.name} ({self.state})"