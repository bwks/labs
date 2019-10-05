import pathlib

from lab_base.generate_data import generate_data
from lab_base.loaders import render_from_template
from lab_base.constants import TEMPLATES_DIR, TEMPLATE_MAP


def write_to_file(device, device_model, config_type, config):
    with open(f'config/{config_type}/{device}-{device_model}.cfg', 'w') as f:
        f.write(config)


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
            interfaces=data['routers'][router],
            other_routers=data['other_routers'],
        )
        write_to_file(device=router, device_model=router_model, config_type=config_type, config=config)
