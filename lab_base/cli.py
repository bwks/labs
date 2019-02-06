import sys
import argparse
import json

from lab_base import vagrant
from lab_base import provision
from lab_base import generate_base_config
from lab_base import utils

if not sys.version_info >= (3, 6):
    sys.exit('Python 3.6 or greater required.')


def validate_devices(devices, ssh_config):
    for dev in devices:
        if dev not in ssh_config:
            sys.exit(f'Device: {dev} either not configured or up.')


def main():
    parser = argparse.ArgumentParser(description='Lab Base Provisioning')
    parser.add_argument('--device-config', default=False, action='store_true',
                        dest='device_config', help='Generate device config')
    parser.add_argument('--ssh-config', default=False, action='store_true',
                        dest='ssh_config', help='Gather Vagrant SSH config')
    parser.add_argument('--apply-config', nargs='+',
                        dest='apply_config', help='Apply config to devices')
    parser.add_argument('--reload-baseline', nargs='+',
                        dest='reload_baseline', help='Reload baseline config')
    args = parser.parse_args()

    if args.device_config:
        print('Generating device config.')
        generate_base_config.make_config()
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
        ssh_config = utils.load_ssh_config()
        validate_devices(args.apply_config, ssh_config)
        print('Applying config to devices.')
        provision.worker(args.apply_config, 'apply_config')
        print('Config applied to devices.')

    if args.reload_baseline:
        ssh_config = utils.load_ssh_config()
        validate_devices(args.reload_baseline, ssh_config)
        print('Reloading device baselines.')
        provision.worker(args.reload_baseline, 'reload_baseline')
        print('Baseline applied to devices.')
