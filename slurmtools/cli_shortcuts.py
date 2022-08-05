"""
Defines CLI shortcut functions to run the main CLI with subcommands.
"""

import subprocess
import sys

def viewmyqueue():
    cmd = "slurmtools queue --view "
    cmd += " ".join( sys.argv[1:] )
    subprocess.run( cmd, shell = True )

def myqueue():
    cmd = "slurmtools queue "
    cmd += " ".join( sys.argv[1:] )
    subprocess.run( cmd, shell = True )

def qrun():
    cmd = "slurmtools session "
    cmd += " ".join( sys.argv[1:] )
    subprocess.run( cmd, shell = True )
