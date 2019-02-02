import yaml
import json
from multiprocessing.pool import ThreadPool
from napalm import get_network_driver


def driver_switcher(device_model):
    driver_map = {
        'vmx': 'junos',
        'veos': 'eos',
    }
    if device_model in driver_map:
        return driver_map.get(device_model)
    raise ValueError(f'Device model: "{device_model}" does not have an associated driver.')


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
    with open('.sshconfig.json', 'r') as f:
        ssh_config_json = json.load(f)
    host_name = ssh_config_json[device].get('HostName')
    config = f'config/{device}-{device_model}.cfg'
    device_driver = driver_switcher(device_model)
    commit_message = 'base-config' if device_driver == 'junos' else ''
    driver = get_network_driver(device_driver)
    device = driver(hostname=host_name, username='', password='',
                    optional_args={'ssh_config_file': '.sshconfig'})
    device.open()
    device.load_merge_candidate(filename=config)
    device.commit_config(message=commit_message)
    device.close()


def worker(devices):
    device_model_map = get_device_model()
    pool_size = len(devices) if len(devices) < 50 else 50
    pool = ThreadPool(pool_size)

    results = []
    for device in devices:
        result = pool.apply_async(provisioner, (device, device_model_map.get(device)))
        results.append(result)

    pool.close()
    pool.join()

    return [i.get() for i in results]
