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
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml"
        }
    }
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
}
