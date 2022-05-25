# Specification for local/remote hybrid workflow

## Introduction

A standard hpcflow workflow should contain parts that can be executed locally and parts that can be executed remotely.
We envisage that rapid pre-processing tasks will be carried out locally, some files transferred to a remote HPC system,
and then the slower work run on the remote system. Finally results will be copied and post-processing carried out 
locally.

## Required info about a task

Some additional info is required about each task in a workflow:

1. What are the commands to be executed (probably a list of strings).
1. Will the task be executed locally or remotely. Locally means in the same location as running instance of hpcflow, 
remote mans on a different machine.
1. How will the task be executed (direct, SGE, slurm, etc.)
1. For remote, what is the hostname?
1. For remote, what is the username?

Consider using dict for each task - `commands` is now a list of dicts, where each dict contains the task strings, target
system, etc.

## Other thoughts

For previous, queue only version the queueing software handled the progression between tasks. For locally executed 
tasks we need something to manage this progression. Current version of task executions uses hpcflow itself and subprocess.
hpcflow waits for each task to complete before executing the next one.

It would be ideal to have a workflow that can pause and save it's position ready to be picked up by another instance of 
hpcflow. This way local and remote instances of hpcflow could pass the workflow between themselves. It could even live 
in a third, cloud-based location and be accessed by both local (i.e. a user's pc) and remote systems.