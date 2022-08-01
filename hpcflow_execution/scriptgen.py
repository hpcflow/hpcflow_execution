import subprocess
from pathlib import Path

def write_execution_files(command, command_idx, workflow_path):

    file_list = []

    command_script_filename = f'{command["name"]}_{command_idx}.sh'

    scheduler = command["scheduler"]

    if command["scheduler"] == 'SGE':

        job_script = gen_sge_job_script(command_script_filename)
        sub_command = f'qsub '

    elif command["scheduler"] == 'slurm':

        job_script = gen_slurm_job_script(command_script_filename)
        sub_command = f'sbatch '

        file_list.append(str(workflow_path / job_script_filename))
        to_execute = f'{sub_command}{job_script_filename}'

    if command["scheduler"] == 'SGE' or command["scheduler"] == 'slurm':

        job_script_filename = f'job_{command_idx}.job'
        write_file(job_script, workflow_path / job_script_filename)

        file_list.append(str(workflow_path / job_script_filename))
        to_execute = f'{sub_command}{job_script_filename}'

    elif scheduler == 'direct':

        to_execute = f'./{command_script_filename}'

    command_steps = gen_task_string(command["commands"])

    write_file(command_steps, workflow_path / command_script_filename)
    file_list.append(str(workflow_path / command_script_filename))

    if command["host_os"] == 'posix':
        subprocess.run(f'chmod u+rwx {workflow_path / command_script_filename}', shell=True)
    elif command["host_os"] == 'windows':
        pass
    
    return [to_execute, file_list]

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