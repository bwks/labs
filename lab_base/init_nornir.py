from nornir import InitNornir

from lab_base.utils import generate_nornir_inventory


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
