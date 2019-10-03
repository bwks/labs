import os

from nornir import InitNornir

USER_HOME = os.path.expanduser('~')
BASE_DIR = os.path.join(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATE_MAP = {
    'vmx': 'juniper-vmx.j2',
    'vqfx': 'juniper-vqfx.j2',
    'veos': 'arista-veos.j2',
    'cvx': 'cumulus-vx.j2',
}


nr = InitNornir(
    core={"num_workers": 100},
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "hosts": hosts,
            "groups": groups,
            # "host_file": "inventory/hosts.yaml",
            # "group_file": "inventory/groups.yaml"
        }
    },
    ssh={"config_file": ".sshconfig"}
)

groups = {
    'base': {
        'connection_options': {
            'naplam': {
                'extras': {
                    'optional_args': {
                        'ssh_config_file': '.sshconfig',
                    }
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
