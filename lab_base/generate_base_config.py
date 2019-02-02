import pathlib

from lab_base.generate_data import generate_data
from lab_base.loaders import render_from_template
from lab_base.constants import TEMPLATES_DIR, TEMPLATE_MAP


def write_to_file(device, device_model, config):
    with open(f'config/{device}-{device_model}.cfg', 'w') as f:
        f.write(config)


def make_config():
    config_dir = pathlib.Path('config')
    config_dir.mkdir(exist_ok=True)

    data = generate_data()
    router_model = 'vmx'
    switch_model = 'veos'
    routers = list(data['routers'].keys())
    switches = [f'p{x}sw1{x}' for x in range(1, 5)]

    pod_map = {
        'p1': 'pod1',
        'p2': 'pod2',
        'p3': 'pod3',
        'p4': 'pod4',
    }

    for router in routers:
        config = render_from_template(
            template_name=TEMPLATE_MAP[router_model],
            template_directory=TEMPLATES_DIR,
            hostname=router,
            interfaces=data['routers'][router]
        )
        write_to_file(router, router_model, config)

    for switch in switches:
        pod = pod_map.get(switch[:2])
        config = render_from_template(
            template_name=TEMPLATE_MAP[switch_model],
            template_directory=TEMPLATES_DIR,
            hostname=switch,
            vlans=data['vlans'],
            pod=pod,
        )
        write_to_file(switch, switch_model, config)
