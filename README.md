This package defines some tools to interact with the SLURM job handler on high performance computer clusters via both a python API and command-line interface.

Some of these tools will be just (more readable) synonyms of conventional SLURM tools, others are useful derivatives that make working with SLURM quicker or easier.

Of course, the native SLURM CLI is more powerful and, naturally, not all functionalities will be available through `slurmtools`, however, the purpose of `slurmtools` is merely to provide an easier to handle SLURM interface for most users. 

## Example usage:
`slurmtools` offers the basic functionalities most users will use continuously when working with the SLURM job handler.

```
# to submit a new job
slurmtools new mynewjob.slurm
```

```
# to show the user's SLURM queue
slurmtools queue 
```
> There are two shortcuts available for this command:
> - `myqueue`
> - `myq` 

```
# to show job information
slurmtools info {myjobid}
```

But `slurmtools` also adds some tweaks such as easy/easier undoing of job submissions:

```
# to terminate the last submitted job
slurmtools kill last
```

showing information about the last added job works just the same

```
slurmtools info last
```

Two features that `slurmtools` adds anew are the 
*self-refreshing queue* and the detachable *srun session*.

```
# to keep a self-refreshing queue open
# wich refreshs every 5 seconds
slurmtools queue --view --time=5
```

> There are three shortcuts available for this command:
> - `viewmyqueue`
> - `viewmyq`
> - `vmyq`

The *srun sessions* are configurable but also come with a
number of preset specs that can directly be called upon to avoid the need to manually specify resources.

```
# to open an srun session with 
# 5 cpus, 50Gb memory, for 10 hours
# -> this is pre-defined scale Big (symbol B)
slurmtools session --scale=B
```

Avaliable preset scales are:

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

