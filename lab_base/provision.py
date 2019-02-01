from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks import networking

from lab_base.constants import NORNIR_DIR
init_nornir = InitNornir(
    core={'num_workers': 50},
    inventory={
        'plugin': 'nornir.plugins.inventory.simple.SimpleInventory',
        'options': {
            'host_file': f'{NORNIR_DIR}/hosts.yml',
            'group_file': f'{NORNIR_DIR}/groups.yml',
        },
    },
    ssh={'config_file': '.sshconfig'},
)

routers = init_nornir.filter(role='router')
result = routers.run(task=networking.napalm_configure,
                        filename=f'config/{task.host.hostname}')
print_result(result)
