import yaml
import json
from multiprocessing.pool import ThreadPool
from napalm import get_network_driver

from lab_base import utils

def driver_switcher(device_model):
    driver_map = {
        'vmx': 'junos',
        'veos': 'eos',
    }
    if device_model in driver_map:
        return driver_map.get(device_model)
    raise ValueError(f'Device model: "{device_model}" does not have an associated driver.')


def baseline_switcher(driver):
    commands = {
        'junos': 'request system configuration rescue save',
        'eos': 'copy running-config checkpoint:base-config',
    }
    return commands.get(driver, '')


def get_config(device, device_model):
    try:
        with open(f'config/{device}-{device_model}.cfg', 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f'Config file: "{device}-{device_model}.cfg" not found.')


def get_device_model():
    with open('guests.yml', 'r') as f:
        guests = yaml.safe_load(f)
    guests_map = {
        'juniper/vmx-vcp': 'vmx',
        'arista/veos': 'veos',
        'CumulusCommunity/cumulus-vx': 'cvx'
    }
    return_data = {}
    for guest, data in guests.items():
        if data['vagrant_box']['name'] in guests_map:
            return_data.update({
                guest: guests_map.get(data['vagrant_box']['name'])
            })
    return return_data


def provisioner(device, device_model):
    ssh_config = utils.load_ssh_config()
    config = f'config/{device}-{device_model}.cfg'
    device_driver = driver_switcher(device_model)

    if device_driver == 'eos':
        device = ssh_config[device].get('HostName')

    commit_message = 'base-config' if device_driver == 'junos' else ''
    driver = get_network_driver(device_driver)
    dev = driver(hostname=device, username='vagrant', password='vagrant',
                 optional_args={'ssh_config_file': '.sshconfig'})
    dev.open()
    dev.load_merge_candidate(filename=config)
    dev.commit_config(message=commit_message)
    dev.cli([baseline_switcher(device_driver)])
    dev.close()


def reload_baseline(device, device_model):
    ssh_config = utils.load_ssh_config()
    device_driver = driver_switcher(device_model)

    if device_driver == 'eos':
        device = ssh_config[device].get('HostName')

    commit_message = 'base-config' if device_driver == 'junos' else ''
    driver = get_network_driver(device_driver)
    dev = driver(hostname=device, username='vagrant', password='vagrant',
                 optional_args={'ssh_config_file': '.sshconfig'})
    dev.open()
    if device_driver == 'junos':
        dev.device.cu.rescue(action="reload")
    elif device_driver == 'eos':
        dev.cli(['configure checkpoint restore base-config'])
    dev.commit_config(message=commit_message)

    dev.close()


def worker(devices, work_type='apply_config'):
    device_model_map = get_device_model()
    pool_size = len(devices) if len(devices) < 50 else 50
    pool = ThreadPool(pool_size)

    results = []
    for device in devices:
        if work_type == 'apply_config':
            result = pool.apply_async(provisioner, (device, device_model_map.get(device)))
        elif work_type == 'reload_baseline':
            result = pool.apply_async(reload_baseline, (device, device_model_map.get(device)))
        else:
            raise ValueError(f'Unknown work type: {work_type}')
        results.append(result)

    pool.close()
    pool.join()

    return [i.get() for i in results]
