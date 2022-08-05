This folder contains the original pure-shell versions
for the code to generate the *self-refreshing SLURM queue*
as well as the *detachable srun session*.


View the Queue
--------------

The command for the self-refreshing queue is any of these:

> Note:
> This version of `viewmyqueue` does **NOT** support option flags! In only accepts a single argument for the *time in seconds* between each refresh (see example below)!

```
# waits by default 15 seconds between each refresh

viewmyqueue 

# or

viewmyq 20 # ( refreshes every 20 seconds )

# or

vmyq
```

For the default queue (restricted to the user's queue!) the commands are:

```
myqueue

# or

myq
```

Creating `srun` sessions
------------------------

The command to open *srun sessions* is called `qrun` (or `quickrun`). 

> Note:
> This version of the command has slightly different 
> preset scales and default settings!

```
# runs a default detached srun session
qrun -d
```

Available scales and defaults here are:

    ----------------------------------------––––––––––––––-
    -t / --time         Defaults to 05:00:00 
    -c / --cpu          Defaults to 3 cores
    -m / --mem          Defaults to 10G
    -d / --detach       Detaches with tmux
    ---------------------------------------––––––––––––––--
    Quick setup for making a large, medium
    or small-scale run
    --------------------------------------––––––––––––––---
    -s / --scale        Can be:
                        -> B (Big)    = 10:00:00 | 10 | 50G
                        -> b          = 00:30:00 | 10 | 50G

                        -> M (Meidum) = 10:00:00 | 5  | 5G
                        -> m          = 00:30:00 | 5  | 5G

                        -> S (Small)  = 10:00:00 | 1  | 1G
                        -> s          = 00:30:00 | 1  | 1G

                        -> T (Tiny)   = 10:00:00 | 1  | 10M
                        -> t          = 00:30:00 | 1  | 10M
    ----------------------------------––––––––––––––-------