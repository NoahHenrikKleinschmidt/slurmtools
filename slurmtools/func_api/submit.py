"""
Submit a new slurm job
"""

import subprocess
from .last_submit import last_submit

class CmdArgs:
    """
    A class to imitate command line arguments returned from a ArgumentParser.
    The properties can either be directly passed or imported from a 
    dictionary after initialization using the `from_dict` method.

    Parameters
    ----------
    time : str
        The time to run the job for.
    nodes : int
        The number of nodes to run the job on.
    cores : int
        The number of cores to run the job on.
    memory : str
        The amount of memory to run the job with.
    partition : str
        The partition to run the job on.
    """
    def __init__(self, time : str = None, nodes : int = None, cores : int = None, memory : str = None, partition : str = None):
        self.time = time
        self.nodes = nodes
        self.cores = cores
        self.memory = memory
        self.partition = partition

    def from_dict(self, d : dict ):
        """
        Initialize the class from a dictionary

        Parameters
        ----------
        d : dict
            The dictionary to initialize the class from.
            This may contain entries for `time`, `nodes`, `cores`, `memory`, and `partition`.
        """
        self.time = d.get( "time", None )
        self.nodes = d.get( "nodes", None )
        self.cores = d.get( "cores", None )
        self.memory = d.get( "memory", None )
        self.partition = d.get( "partition", None )

def submit( filename : str, args ) -> int:
    """
    Submit a new slurm job

    Parameters
    ----------
    filename : str
        The name of the job file.
    args : CmdArgs
        The arguments to pass to the job.
        This can have attributes for `time`, 
        `nodes`, `cores`, `memory`, and `partition`.

    Returns
    -------
    jobid : str
        The job-id of the submitted job.
    """

    time = "-t {args.time} " if args.time else ""
    nodes = "-N {args.nodes} " if args.nodes else ""
    cores = "-c {args.cores} " if args.cores else ""
    memory = "-m {args.memory} " if args.memory else ""
    partition = "-p {args.partition} " if args.partition else ""

    cmd = f"sbatch {time}{cores}{memory}{partition}{nodes}{filename}"
    newjob = subprocess.run( cmd, shell = True, capture_output = True )
    
    newjob = extract_jobid(newjob) 
    last_submit( newjob )
    
    return newjob

def extract_jobid( msg ) -> int:
    """
    Extracts the jobid from the slurm submission message.

    Parameters
    ----------
    msg : CompletedProcess
        The slurm submission message as raw output from `subprocess.run`.
    
    Returns
    -------
    jobid : int
        The job-id of the submitted job.
    """
    msg = msg.stdout.decode("utf-8")
    jobid = int( msg.split(" ")[-1].strip() )
    return jobid
  