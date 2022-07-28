remote_flow = [
    'remote_flow',
    { 'name': 'direct_task',
    'command': [
        'direct_task',
        '/bin/date',
        '/bin/hostname',
        '/bin/sleep 10',
        '/bin/date'
        ],
    'location': 'remote',
    'host_os': 'posix',
    'scheduler': 'direct',
    'basefolder': '/mnt/iusers01/support/mbcxgcf2',
    'hostname': 'csf3.itservices.manchester.ac.uk',
    'username': 'mbcxgcf2',
    },
    {'name': 'queued_task',
    'command': [
        'queued_task',
        '/bin/date',
        '/bin/hostname',
        '/bin/sleep 10',
        '/bin/date'
        ],
    'location': 'remote',
    'host_os': 'posix',
    'scheduler': 'SGE',
    'basefolder': '/mnt/iusers01/support/mbcxgcf2',
    'hostname': 'csf3.itservices.manchester.ac.uk',
    'username': 'mbcxgcf2',
    }
]