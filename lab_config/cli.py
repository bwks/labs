import sys
import argparse
import json
import pathlib

from nornir.plugins.tasks import networking, text, files
from nornir.plugins.functions.text import print_title, print_result
from nornir.core.filter import F

from lab_config import vagrant
from lab_config import init_nornir
from lab_config import generate_config

if not sys.version_info >= (3, 6):
    sys.exit('Python 3.6 or greater required.')


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


def save_configs(task):
    # Ensure backup path exists
    backup_path = 'config/baseline'
    pathlib.Path(backup_path).mkdir(parents=True, exist_ok=True)

    # Gather config using napalm_get and assign to a variable
    config_result = task.run(task=networking.napalm_get, getters=["config"])

    # Write the configs to a file.
    task.run(
        task=files.write_file,
        content=config_result.result["config"]['running'],
        filename=f"{backup_path}/{task.host}-{task.host['model']}.cfg",
    )


def validate_devices(devices, ssh_config):
    for dev in devices:
        if dev not in ssh_config:
            sys.exit(f'Device: {dev} either not configured or up.')


def main():
    parser = argparse.ArgumentParser(description='Lab Base Provisioning')
    parser.add_argument('--generate-config', default=False, action='store_true',
                        dest='generate_config', help='Generate device config')
    parser.add_argument('--ssh-config', default=False, action='store_true',
                        dest='ssh_config', help='Gather Vagrant SSH config')
    parser.add_argument('--apply-config',
                        dest='apply_config', help='Apply a config to devices')
    parser.add_argument('--save-config', default=False, action='store_true',
                        dest='save_config', help='Save all devices config')
    parser.add_argument("--reload-baseline", default=False, action="store_true",
                        dest="reload_baseline", help="reload the saved baseline config")

    args = parser.parse_args()

    if args.generate_config:
        print('Generating device config.')
        generate_config.make_base_config()
        for config in ['ospf', 'isis', 'mpls']:
            generate_config.make_feature_config(config_type=config)
        print('Config saved to "./config" directory.')

    if args.ssh_config:
        print('Gathering vagrant SSH config')
        guests = vagrant.get_guests()
        ssh_config_dict = vagrant.worker(guests)
        with open('.sshconfig', 'w') as f:
            f.write('\n'.join(vagrant.ssh_config_to_list(ssh_config_dict)))
        with open('.sshconfig.json', 'w') as f:
            f.write(json.dumps(ssh_config_dict))
        print(f'SSH config saved to files ".sshconfig and .sshconfig.json"')

    if args.apply_config:
        print('Applying config to devices.')
        nr = init_nornir.init_nornir()
        devices = nr.filter(F(groups__contains=args.apply_config))
        result = devices.run(task=config_device, config_type=args.apply_config, replace_config=False)
        print_result(result)
        print('Config applied to devices.')

    if args.save_config:
        nr = init_nornir.init_nornir()
        devices = nr.filter(F(groups__contains="base"))
        print_title("Runbook to save rescue config")
        result = devices.run(task=save_configs)
        print_result(result)

    if args.reload_baseline:
        nr = init_nornir.init_nornir()
        devices = nr.filter(F(groups__contains="base"))
        print_title("Runbook to reload baseline configs")
        result = devices.run(task=config_device, config_type="baseline", replace_config=True)
        print_result(result)
