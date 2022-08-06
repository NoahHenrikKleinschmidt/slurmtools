"""
A class to handle SlurmJobs
"""

from datetime import datetime
from . import kill, info
import re
import pandas as pd

class SlurmJob:
    def __init__( self, id ):
        self.id = id
        self.info = self.get_info()
    
    def kill(self):
        """
        Kill the job
        """
        kill.kill_job( self.id )
    
    def get_info( self ) -> str:
        """
        Get raw job info
        """
        self.info = info.raw_job_info( self.id )
        return self.info

    def summary( self ):
        """
        Prints a shortened version of the job info.
        """
        string = self._make_summary()
        print( string )

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
        state = re.search( pattern, self.info ).group(1)
        return state
    
    @property
    def state_reason( self ) -> str:
        """
        Get job state reason
        """
        pattern = "Reason=([A-Z0-9a-z()\-_\.,]*)"
        state = re.search( pattern, self.info ).group(1)
        if state == "None":
            state = None
        return state

    @property
    def time( self ) -> pd.Timestamp:
        """
        Get job runtime
        """
        pattern = "RunTime=([0-9 \- :]*)"
        time = re.search( pattern, self.info ).group(1)
        time = pd.to_datetime( time )
        return time
    
    @property
    def start( self ) -> pd.Timestamp:
        """
        Get job start time
        """
        pattern = "StartTime=([0-9T \- :]*)"
        time = re.search( pattern, self.info ).group(1)
        time = pd.to_datetime( time )
        return time
    
    @property
    def end( self ) -> pd.Timestamp:
        """
        Get job end time
        """
        pattern = "EndTime=([0-9T \- :]*)"
        time = re.search( pattern, self.info ).group(1)
        time = pd.to_datetime( time )
        return time

    @property
    def time_remaining( self ) -> pd.Timedelta:
        """
        Get job's time remaining to finish
        """
        return self.end - datetime.now()

    @property
    def nodes( self ) -> str:
        """
        Get job nodes
        """
        pattern = "Nodes=([a-zA-Z0-9/_\.\\\-]*)"
        nodes = re.search( pattern, self.info ).group(1)
        return nodes
    
    @property
    def cores( self ) -> int:
        """
        Get the number of cores
        """
        pattern = "NumCPUs=([0-9]*)"
        cores = re.search( pattern, self.info ).group(1)
        cores = int( cores )
        return cores
    
    @property
    def memory( self ) -> int:
        """
        Get the memory assignment
        """
        pattern = "Mem=([0-9]*)"
        memory = re.search( pattern, self.info ).group(1)
        memory = int( memory )
        return memory

    @property
    def partition( self ) -> str:
        """
        Get the partition
        """
        pattern = "Partition=([a-zA-Z0-9/_\.\\\-]*)"
        partition = re.search( pattern, self.info ).group(1)
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

Runtime:    {self.time.time()}
Time limit: {self.end} ({self.time_remaining})

{filler}
Technical Info
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