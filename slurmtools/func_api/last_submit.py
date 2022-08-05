_last_submit = [999099]
"""The last submitted job id"""

def last_submit( jobid = None ):
    """
    Get and/or set the last submitted job id
    """
    if jobid is not None:
        # if we have a new jobid then we have to write it 
        # to the file to ensure it is remembered across command
        # line calls
        with open( __file__ , "r" ) as f: 
            c = f.read().split("\n")
            c[0] = f"_last_submit = [{jobid}]"
            c = "\n".join(c)
        with open( __file__ , "w" ) as f: 
            f.write( c )
    return _last_submit[0]

def reset_last_submit():
    """
    Reset the last submitted job id
    """
    with open( __file__ , "r" ) as f: 
        c = f.read().split("\n")
        c[0] = "_last_submit = [None]"
        c = "\n".join(c)
    with open( __file__ , "w" ) as f: 
        f.write( c )
    return _last_submit[0]