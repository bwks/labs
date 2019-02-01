from napalm import get_network_driver

from lab_base.constants import DRIVER_MAP


def apply_config(device, device_model):
    driver = get_network_driver(DRIVER_MAP[device_model])
    commit_message = 'base-config' if driver == 'junos' else ''

    with driver(device, 'vagrant', 'Vagrant') as dev:
        dev.load_merge_candidate(filename=f'config/{device}-{device_model}.cfg')
        dev.commit_config(commit_message)
