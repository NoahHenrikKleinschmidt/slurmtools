"""
A class to handle SlurmJobs
"""

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
        pattern = "Account=([a-zA-Z0-9 / _ \. \\ \-]*)"
        user = re.search( pattern, self.info ).group(1)
        return user

    @property
    def name( self ) -> str:
        """
        Get job name
        """
        pattern = "JobName=([a-zA-Z0-9 / _ \. \\ \-]*)"
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
    def time_limit( self ) -> pd.Timestamp:
        """
        Get job time limit
        """
        pattern = "TimeLimit=([0-9 \- :]*)"
        time = re.search( pattern, self.info ).group(1)
        time = pd.to_datetime( time )
        return time
    
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
    def nodes( self ) -> str:
        """
        Get job nodes
        """
        pattern = "Nodes=([a-zA-Z0-9 / _ \. \\ \-]*)"
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
        pattern = "Partition=([a-zA-Z0-9 / _ \. \\ \-]*)"
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
        stdin = re.search( pattern, self.info ).group(1)
        return stdin
    
    @property
    def stdout( self ) -> str:
        """
        Get the stdout
        """
        pattern = "StdOut=([a-zA-Z0-9 / _ \. \\ \-]*)"
        stdout = re.search( pattern, self.info ).group(1)
        return stdout
    
    @property
    def stderr( self ) -> str:
        """
        Get the stderr
        """
        pattern = "StdErr=([a-zA-Z0-9 / _ \. \\ \-]*)"
        stderr = re.search( pattern, self.info ).group(1)
        return stderr
    
    def __repr__( self ) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
    
    def __str__( self ) -> str:
        return f"[Job {self.id}] {self.name} ({self.state})"