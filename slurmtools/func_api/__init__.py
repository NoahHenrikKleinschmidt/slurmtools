"""
The main API
"""

from .last_submit import last_submit, reset_last_submit
from .info import raw_job_info, job_info, show_all, info_by_pattern, SlurmJob
from .kill import kill_last, kill_all, kill_job, kill_by_pattern
from .queue import queue, view_queue
from .session import session, scales
from .submit import submit, CmdArgs
from .read import read_stdout, read_stderr
