"""
Interactive slurm sessions (srun) wrapper.
"""

import subprocess
from datetime import datetime

scales = {
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


def session( time : str = "05:00:00", cpu : int = 1, memory : str = "15G", detach : bool = False, partition : str = None, scale : str = None ):
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
    partition : str
        A specific partition to use.   
    detach : bool
        Start the session in detached mode (i.e. detach using `tmux`).
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
    
    session_name = f"session-{datetime.now().strftime( '%Y%m%d-%H%M%S' )}"

    # now make either a detached session or not
    cmd = f"""srun --job-name='{session_name}' --time={time} -c {cpu} --mem={memory}"""
    
    if partition: 
        cmd += f" -p {partition}"
    cmd += " --pty bash"

    if detach:    
        cmd = f"""
tmux new -s {session_name} "{cmd}"  
tmux attach -t {session_name}    
""".strip()

    subprocess.run( cmd, shell = True )