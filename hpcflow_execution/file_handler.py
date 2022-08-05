import subprocess
from pathlib import Path

import zarr

def create_persistant_workflow(workflow_id, workflow_dict):

    workflow_persistant = zarr.group(store = f"{workflow_id}.zarr")

    workflow_persistant.create_group("workflow")

    for key in workflow_dict.keys():
        workflow_persistant.attrs[key] = workflow_dict[key]

    return workflow_persistant


def write_execution_files(command, command_idx, workflow_persistant):

    file_list = []

    command_script_filename = f'{command["name"]}_{command_idx}.sh'

    scheduler = command["scheduler"]

    workflow_persistant.workflow.create_group(f"task_{command_idx}")
    task_path = Path(workflow_persistant.workflow.store.dir_path()) / "workflow" / f"task_{command_idx}"

    if command["scheduler"] == 'SGE':

        job_script = gen_sge_job_script(command_script_filename)
        sub_command = f'qsub '

    elif command["scheduler"] == 'slurm':

        job_script = gen_slurm_job_script(command_script_filename)
        sub_command = f'sbatch '

    if command["scheduler"] == 'SGE' or command["scheduler"] == 'slurm':

        job_script_filename = f'job_{command_idx}.job'
        write_file(job_script, task_path / job_script_filename)

        file_list.append(str(task_path / job_script_filename))
        to_execute = f'{sub_command}{job_script_filename}'

    elif scheduler == 'direct':

        to_execute = f'./{command_script_filename}'

    command_steps = gen_task_string(command["commands"])

    write_file(command_steps, task_path / command_script_filename)
    file_list.append(str(task_path / command_script_filename))

    if command["host_os"] == 'posix':
        subprocess.run(f'chmod u+rwx {task_path / command_script_filename}', shell=True)
    elif command["host_os"] == 'windows':
        pass
    
    workflow_persistant.attrs["tasks"][command_idx]["execute"] = to_execute
    workflow_persistant.attrs["tasks"][command_idx]["exec_dir"] = str(task_path)
    workflow_persistant.attrs["tasks"][command_idx]["file_list"] = file_list

    return workflow_persistant


def gen_sge_job_script(command):

    # Currently very simple
    script = ''
    script += f'#!/bin/bash --login\n'
    script += f'#$ -cwd\n'
    script += f'./{command}\n'

    return script
    

def gen_slurm_job_script(command):

    # Currently very simple
    script = ''
    script += f'#!/bin/bash --login\n'
    script += f'#SBATCH -p serial\n'
    script += f'#SBATCH -n 1\n'
    script += f'./{command}\n'

    return script


def gen_task_string(task_list):

    task_list_f = [f'{sub_task}\n' for sub_task in task_list]

    task = ''.join(task_list_f)

    return task


def write_file(contents, filename):

    with open(filename, 'a') as file:
        file.write(contents)