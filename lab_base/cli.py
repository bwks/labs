import sys
if not sys.version_info >= (3, 6):
    sys.exit('vagrant-tools requires Python 3.6 or greater')

import argparse

from lab_base.vagrant import (
    get_guests,
    worker,
)


def main():
    parser = argparse.ArgumentParser(description='Lab Base Provisioning')
    parser.add_argument('-g', '--get-guest-data', help='Gather guest data', action='store', type=str,
                        nargs='?', const='guest-data.json', metavar='FILENAME', dest='guest_data')
    args = parser.parse_args()

    if args.guest_data:
        print('Gathering vagrant SSH config')
        guests = get_guests()
        data = worker(guests)
        with open('.sshconfig', 'w') as f:
            f.write('\n'.join(data))
        print(f'SSH config saved to file ".sshconfig"')


if __name__ == '__main__':
    main()
