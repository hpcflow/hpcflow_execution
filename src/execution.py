from multiprocessing.sharedctypes import Value
import sched
import subprocess
import sunau
import sys
from typing import Type

import scriptgen

def run_elements(commands, scheduler='SGE', host_os='posix'):

    [scriptgen.write_execution_files(command, command_idx, scheduler, host_os) for command, command_idx in enumerate(commands)]
    
    if host_os == 'posix':
        posix_run(commands, scheduler)
    
    elif host_os == 'windows':
        windows_run(commands, scheduler)

    else:
        msg = f'\'{host_os}\' is not a supported OS. Please enter \'windows\' for Windows, or \'posix\' for macOS or Linux.'
        raise ValueError(msg)

def posix_run(commands, scheduler='SGE'):

    host_os = 'posix'
    if scheduler == 'direct':
        run_direct(commands, host_os)

    elif scheduler == 'SLURM':
        run_slurm(commands)

    elif scheduler == 'SGE':
        run_sge(commands)

    else:
        msg = f'{scheduler} is not a supported scheduler on {host_os}. Plese enter \'SGE\' for Sun Grid Engine, \'slurm\' for SLURM, or \'direct\' to run the command locally.'
        raise ValueError(msg)

def windows_run(commands, scheduler='direct'):
    
    host_os = 'windows'
    if scheduler == 'direct':
        run_direct(commands, host_os)

    else:
        msg = f'{scheduler} is not a supported scheduler on {host_os}. Enter \'direct\' to run the command locally.'
        raise ValueError(msg)

def run_direct(commands, host_os):

    if host_os == 'posix':
        for command in commands:
            subprocess.run(command, shell=True)

    elif host_os == 'windows':
        # How will commands be run in windows? Can we assume terminal?
        pass

def run_slurm(commands):
    pass

def run_sge(commands):
    pass