import json
import yaml


def load_json_file(json_file):
    """
    Load a JSON file.
    :param json_file: name of file
    :return: dict of data
    """
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def load_yaml_file(yaml_file='guest.yml'):
    """
    Load a YAML file.
    :param yaml_file: name of file
    :return: dict of data
    """
    try:
        with open(yaml_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}


def driver_switcher(guest_model):
    """
    Convert Grifter guest type to Napalm driver type.
    :param guest_model: Grifter guest model
    :return: Napalm driver string
    """
    driver_map = {
        'arista/veos': 'eos',
        'cisco/iosv': 'ios',
        'cisco/iosv-l2': 'ios',
        'cisco/csr1000v': 'ios',
        'juniper/vmx-vcp': 'junos',
        'juniper/vqfx-re': 'junos',
        'juniper/vsrx': 'junos',
        'juniper/vsrx-packetmode': 'junos',
    }
    try:
        return driver_map[guest_model]
    except KeyError:
        raise KeyError(f'Guest model: "{guest_model}" does not have an associated driver.')
