from nornir import InitNornir

from lab_base.utils import (
    load_yaml_file,
    load_json_file,
    driver_switcher
)
from lab_base.constants import MODEL_MAP


def generate_nornir_inventory():
    """
    Generate a Nornir inventory dict from .sshconfig.json and guests.yml files.
    :return: Nornir inventory dict
    """
    ssh_config = load_json_file('.sshconfig.json')
    guests = load_yaml_file('guests.yml')
    exclude_guest_types = ['-vfp', '-pfe']
    inventory = {}
    for host, data in ssh_config.items():
        if any(i in host for i in exclude_guest_types):
            continue
        guest_model = guests[host]['vagrant_box']['name']
        platform = driver_switcher(guest_model)
        inventory.update({
            host: {
                'hostname': host,
                'username': data['User'],
                'password': '',
                'platform': platform,
                'data': {'model': MODEL_MAP[guest_model]},
                'groups': [f'pod{host[1]}', 'base', 'ospf', 'isis', 'mpls', 'bgp'],
            }
        })
    return inventory


def init_nornir():
    hosts = generate_nornir_inventory()
    groups = {
        'base': {
            'connection_options': {
                'naplam': {
                    'extras': {
                        'optional_args': {
                            'ssh_config_file': '.sshconfig',
                        }
                    }
                },
                'netmiko': {
                    'extras': {
                        'ssh_config_file': '.sshconfig',
                    }
                }
            }
        },
        'ospf': {},
        'isis': {},
        'mpls': {},
        'pod1': {},
        'pod2': {},
        'pod3': {},
        'pod4': {},
    }

    return InitNornir(
        core={"num_workers": 100},
        inventory={
            "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
            "options": {
                "hosts": hosts,
                "groups": groups,
            }
        },
        ssh={"config_file": ".sshconfig"}
    )
