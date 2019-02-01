import sys
if not sys.version_info >= (3, 6):
    sys.exit('Python 3.6 or greater required.')

import argparse

from lab_base.vagrant import (
    get_guests,
    worker,
)


def main():
    parser = argparse.ArgumentParser(description='Lab Base Provisioning')
    parser.add_argument('--provision', help='Provision lab')
    args = parser.parse_args()

    if args.provision:
        print('Gathering vagrant SSH config')
        guests = get_guests()
        data = worker(guests)
        with open('.sshconfig', 'w') as f:
            f.write('\n'.join(data))
        print(f'SSH config saved to file ".sshconfig"')
