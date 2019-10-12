import pathlib

from lab_config.generate_data import generate_data
from lab_config.loaders import render_from_template
from lab_config.constants import TEMPLATES_DIR, TEMPLATE_MAP


def write_to_file(device, device_model, config_type, config):
    with open(f'config/{config_type}/{device}-{device_model}.cfg', 'w') as f:
        f.write(config)


def make_base_config(router_model='vmx', switch_model='vqfx', config_type='base'):
    config_dir = pathlib.Path(f'config/{config_type}')
    config_dir.mkdir(exist_ok=True, parents=True)

    data = generate_data()
    routers = list(data['routers'].keys())
    switches = [f'p{x}sw1' for x in range(1, 5)]

    pod_map = {
        'p1': 'pod1',
        'p2': 'pod2',
        'p3': 'pod3',
        'p4': 'pod4',
    }

    for router in routers:
        config = render_from_template(
            template_name=TEMPLATE_MAP[router_model],
            template_directory=f'{TEMPLATES_DIR}/{config_type}',
            hostname=router,
            device_data=data['routers'][router]
        )
        write_to_file(device=router, device_model=router_model, config_type=config_type, config=config)

    for switch in switches:
        pod = pod_map.get(switch[:2])
        config = render_from_template(
            template_name=TEMPLATE_MAP[switch_model],
            template_directory=f'{TEMPLATES_DIR}/{config_type}',
            hostname=switch,
            vlans=data['vlans'],
            pod=pod,
        )
        write_to_file(device=switch, device_model=switch_model, config_type=config_type, config=config)


def make_feature_config(router_model='vmx', config_type='ospf'):
    config_dir = pathlib.Path(f'config/{config_type}')
    config_dir.mkdir(exist_ok=True, parents=True)

    data = generate_data()
    routers = list(data['routers'].keys())

    for router in routers:
        config = render_from_template(
            template_name=TEMPLATE_MAP[router_model],
            template_directory=f'{TEMPLATES_DIR}/{config_type}',
            hostname=router,
            device_data=data['routers'][router],
        )
        write_to_file(device=router, device_model=router_model, config_type=config_type, config=config)


def make_lab_config():
    lab_configs = [
        'isis-1', 'isis-2', 'isis-3',
        'ospf-1', 'ospf-2', 'ospf-3',
        'bgp-1', 'bgp-2',
    ]
    for config in lab_configs:
        config_dir = pathlib.Path(f'config/{config}')
        config_dir.mkdir(exist_ok=True, parents=True)
        path = pathlib.Path(f'{TEMPLATES_DIR}/{config}')
        for file in path.iterdir():
            with open(f'{file}', 'r') as f:
                with open(f'{config_dir}/{file.name}', 'w') as c:
                    c.writelines(f.readlines())
