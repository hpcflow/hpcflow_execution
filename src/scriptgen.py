import subprocess

def write_execution_files(command, command_idx, scheduler, host_os):

    command_script_filename = f'{command}_{command_idx}.sh'

    if scheduler == 'SGE':

        job_script = gen_sge_job_script(command_script_filename)
        sub_command = f'qsub '

    elif scheduler == 'slurm':

        job_script = gen_slurm_job_script(command_script_filename)
        sub_command = f'sbatch '

    if scheduler == 'SGE' or scheduler == 'slurm':

        job_script_filename = f'job_{command_idx}.job'
        write_file(job_script, job_script_filename)
        to_execute = f'{sub_command}{job_script_filename}'

    elif scheduler == 'direct':

        to_execute = f'./{command_script_filename}'

    command_steps = command_simple()
    
    write_file(command_steps, command_script_filename)
    if host_os == 'posix':
        subprocess.run(f'chmod u+rwx {command_script_filename}', shell=True)
    elif host_os == 'windows':
        pass
    
    return to_execute


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
    # Some more sbatch commands here
    script += f'./{command}\n'

def write_file(contents, filename):

    with open(filename, 'a') as file:
        file.write(contents)

def command_simple():
    
    command = ''
    command += f'/bin/date\n'
    command += f'/bin/hostname\n'
    command += f'/bin/sleep 120\n'
    command += f'/bin/date\n'

    return command