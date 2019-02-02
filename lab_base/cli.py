import sys
if not sys.version_info >= (3, 6):
    sys.exit('Python 3.6 or greater required.')

import argparse
import json

from lab_base.vagrant import (
    get_guests,
    ssh_config_to_list,
    worker,
)


def main():
    parser = argparse.ArgumentParser(description='Lab Base Provisioning')
    parser.add_argument('--ssh-config', help='Provision lab', default=False, action='store_true',
                        dest='ssh_config')
    args = parser.parse_args()

    if args.ssh_config:
        print('Gathering vagrant SSH config')
        guests = get_guests()
        ssh_config_dict = worker(guests)
        with open('.sshconfig', 'w') as f:
            f.write('\n'.join(ssh_config_to_list(ssh_config_dict)))
        with open('.sshconfig.json', 'w') as f:
            f.write(json.dumps(ssh_config_dict))
        print(f'SSH config saved to file ".sshconfig and .sshconfig.json"')
