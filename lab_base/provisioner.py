from nornir import InitNornir
from nornir.plugins.tasks import networking, text, files
from nornir.plugins.functions.text import print_title, print_result
from nornir.core.filter import F

from lab_base.utils import generate_nornir_inventory

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


def config_device(task, config_type="base", replace_config=False):
    # Load in configuration files
    r = task.run(task=text.template_file,
                 name=f"{config_type} Configuration".upper(),
                 template=f"{task.host}-{task.host['model']}.cfg",
                 path=f"config/{config_type}")

    # Save the compiled configuration into a host variable
    task.host["config"] = r.result

    # Deploy that configuration to the device using NAPALM
    task.run(task=networking.napalm_configure,
             name="Loading Configuration on the device",
             replace=replace_config,
             configuration=task.host["config"])


def provision():
    nr = InitNornir(
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

    devices = nr.filter(F(groups__contains='pod1'))
    result = devices.run(task=config_device, config='base', replace_config=False)
    print_result(result)
