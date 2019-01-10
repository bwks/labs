import json

from napalm import get_network_driver

driver = get_network_driver('junos')

routers = [
    'p1r1',
    'p1r2',
    'p1r3',
    'p1r4',
    'p1r5',
    'p1r6',
    'p1r7',
    'p1r8',
    'p2r1',
    'p2r2',
    'p2r3',
    'p2r4',
    'p2r5',
    'p2r6',
    'p2r7',
    'p2r8',
]


with open('guest-data.json', 'r') as f:
    devices = json.load(f)


def apply_config():
    for router in routers:
        with driver(devices[router]['HostName'], 'vagrant', 'Vagrant') as dev:
            dev.load_merge_candidate(filename=f'config/{router}.cfg')
            dev.commit_config(message="base-config")


if __name__ == '__main__':
    apply_config()
