# test_execution.py

import pytest
from pathlib import Path

from src import execution

@pytest.fixture
def simple_commands():
    return [
        [
            'touch file1.txt'
        ],
        [
            'touch file2.txt'
        ],
        [
            'touch file3.txt'
        ]
    ]

def test_run_elements_direct_posix(simple_commands, tmpdir):

    # Test for direct execution in posix environment. Three files should be created.

    execution.run_elements(simple_commands, 'direct', 'posix')

    assert Path('file1.txt').is_file()
    assert Path('file2.txt').is_file()
    assert Path('file3.txt').is_file()

def test_unrecognised_host_os(simple_commands):

    # Test that exception is raised if unknown host OS is requested.

    with pytest.raises(Exception) as e_info:
        execution.run_elements(simple_commands, 'direct', 'foo')

def test_unrecognised_scheduler_posix(simple_commands):

    # Test that exception is raised if unknown posix scheduler is requested.

    with pytest.raises(Exception) as e_info:
        execution.run_elements(simple_commands, 'foo', 'posix')

def test_unrecognised_scheduler_windows(simple_commands):

    # Test that exception is raised if unknown windows scheduler is requested.

    with pytest.raises(Exception) as e_info:
        execution.run_elements(simple_commands, 'foo', 'windows')
      


#def test_run_elements_bad_command():
#
#   execution.run_elements([0,1,2,3,4,5], scheduler='direct', host_os='posix')
