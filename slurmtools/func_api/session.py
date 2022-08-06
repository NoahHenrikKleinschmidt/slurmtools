"""
Interactive slurm sessions (srun) wrapper.
"""

import subprocess
from datetime import datetime
import os

def current_conda_env():
    """
    Get the current conda environment.
    """
    env = os.environ[ "CONDA_DEFAULT_ENV" ]
    return env

def activate_conda_env( env_name : str, execute : bool = True ):
    """
    Activate a conda environment.

    Parameters
    ----------
    env_name : str
        The name of the conda environment.
    execute : bool
        Execute the command.
    
    Returns
    -------
    str or None
        The command to activate the conda environment (if not executed).
    """
    cmd = f"conda activate {env_name}"
    if execute:
        subprocess.run( cmd, shell = True )
    else:
        return cmd

scales = {

    # we will use h to display a help message for the scales...
    "h" : {
            "time": None,
            "cpu": None,
            "memory": None,
        },

    "L": {
        "time": "10:00:00",
        "cpu": 20,
        "memory": "100G",
        },
    "l": {
        "time": "00:30:00",
        "cpu": 20,
        "memory": "100G",
        },

    "B": {
        "time": "10:00:00",
        "cpu": 10,
        "memory": "50G",
        },

    "b": {
        "time": "00:30:00",
        "cpu": 10,
        "memory": "50G",
        },
    
    "M": {
        "time": "10:00:00",
        "cpu": 5,
        "memory": "15G",
        },
    
    "m": {
        "time": "00:30:00",
        "cpu": 5,
        "memory": "15G",
        },
    
    "S": {
        "time": "10:00:00",
        "cpu": 1,
        "memory": "5G",
        },
    
    "s": {
        "time": "00:30:00",
        "cpu": 1,
        "memory": "5G",
        },
    
    "T": {
        "time": "10:00:00",
        "cpu": 1,
        "memory": "1G",
        },
    
    "t": {
        "time": "00:30:00",
        "cpu": 1,
        "memory": "1G",
        },
    
    "M": {
        "time": "10:00:00",
        "cpu": 1,
        "memory": "10M",
        },
    
    "m": {
        "time": "00:30:00",
        "cpu": 1,
        "memory": "10M",
        },
}
"""Predefined scales for sessions"""


def session( 
                time : str = "05:00:00", 
                cpu : int = 1, 
                memory : str = "15G", 
                detach : bool = False, 
                partition : str = None, 
                nodes : int = None,
                name : str = None,
                cmd : str = "bash",
                scale : str = None ):
    """
    Start a slurm interactive session.

    Parameters
    ----------
    time : str
        The time limit of the session.
    cpu : int
        The number of cores to use.
    memory : str
        The amount of memory to use.
    detach : bool
        Start the session in detached mode (i.e. detach using `tmux`).
    partition : str
        A specific partition to use.   
    nodes : int
        The number of nodes to use.
    name : str
        The name of the session. 
        By default "session-<timestamp>".
    cmd : str
        The command to execute. By default "bash".
    scale : str
        Use a pre-defined scale to avoid using manual specs.
        Available scales are:
        
    | Symbol     | Time limit | CPUs | Memory |
    | :--------- | :--------- | :--- | :----- |
    | L (Large)  | 10:00:00   | 20   | 100G   |
    | l          | 00:30:00   | 20   | 100G   |
    | B (Big)    | 10:00:00   | 10   | 50G    |
    | b          | 00:30:00   | 10   | 50G    |
    | M (Medium) | 10:00:00   | 5    | 15G    |
    | m          | 00:30:00   | 5    | 15G    |
    | S (Small)  | 10:00:00   | 1    | 5G     |
    | s          | 00:30:00   | 1    | 5G     |
    | T (Tiny)   | 10:00:00   | 1    | 1G     |
    | t          | 00:30:00   | 1    | 1G     |
    | M (Micro)  | 10:00:00   | 1    | 10M    |
    | m          | 00:30:00   | 1    | 10M    |
    """
    if scale is not None:
        time = scales[scale]["time"]
        cpu = scales[scale]["cpu"]
        memory = scales[scale]["memory"]
    
    # add a help message (for CLI use)
    if scale == "h":
        _available_scales()
        return

    # check if we have a name
    if name is None:
        name = f"[{cmd}]-session-{datetime.now().strftime( '%Y%m%d-%H%M%S' )}"

    # now make the command
    _cmd = cmd
    cmd = f"""srun --job-name='{name}'"""
    
    if time: 
        cmd += f" --time={time}"
    if cpu:
        cmd += f" --cpus-per-task={cpu}"
    if memory:
        cmd += f" --mem={memory}"
    if partition: 
        cmd += f" -p {partition}"
    if nodes:
        cmd += f" -N {nodes}"

    cmd += f" --pty {_cmd}"

    if detach:    
        cmd = f"""
tmux new -s {name} "{cmd}"  
tmux attach -t {name}    
""".strip()

    # the conda environment gets reset when using bash!
    # if keep_conda_env:
    #     env = current_conda_env()
    #     env = activate_conda_env( env, execute = False )
    #     cmd = f"{cmd}\n{env}"

    subprocess.run( cmd, shell = True )


def _available_scales():
    """
    Print a help table for the available scales.
    (for CLI use)
    """
    table = """
    
Use any of the available scales defined below by their symbol:

| Symbol     | Time limit | CPUs | Memory |
| :--------- | :--------- | :--- | :----- |
| L (Large)  | 10:00:00   | 20   | 100G   |
| l          | 00:30:00   | 20   | 100G   |
| B (Big)    | 10:00:00   | 10   | 50G    |
| b          | 00:30:00   | 10   | 50G    |
| M (Medium) | 10:00:00   | 5    | 15G    |
| m          | 00:30:00   | 5    | 15G    |
| S (Small)  | 10:00:00   | 1    | 5G     |
| s          | 00:30:00   | 1    | 5G     |
| T (Tiny)   | 10:00:00   | 1    | 1G     |
| t          | 00:30:00   | 1    | 1G     |
| M (Micro)  | 10:00:00   | 1    | 10M    |
| m          | 00:30:00   | 1    | 10M    |
| h (help)   |    display this table      |"""
    print( table )