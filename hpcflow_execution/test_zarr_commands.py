zarr_flow = [
    'zarr_flow',
    { 'name': 'create_data',
    'command': [
        'zarr_test_task',
        'python ../hpcflow_execution/ZarrTest.py testdata.zarr'],
    'location': 'local',
    'host_os': 'posix',
    'scheduler': 'direct',
    'basefolder': 'NaN',
    'hostname': 'NaN',
    'username': 'mbcxgcf2',
    }
]