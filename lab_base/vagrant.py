import csv
import subprocess
import io

from multiprocessing.pool import ThreadPool


def ssh_config_to_dict(guest):
    """
    Returns a dictionary of SSH config for each device.
    :param guests: A list of guests
    :return: Dict of devices SSH config
    """
    config = subprocess.getoutput(f'vagrant ssh-config {guest}')
    guest_config = {guest: {}}
    for i in config.split('\n')[1::]:
        if i:
            j = i.strip().split(' ')
            guest_config[guest].update({j[0]: j[1]})
    return guest_config


def ssh_config_to_list(ssh_config_dict):
    ssh_config_list = []
    for key, value in ssh_config_dict.items():
        ssh_config_list.append(f'Host {key}')
        for k, v in value.items():
            ssh_config_list.append(f'  {k} {v}')
    return ssh_config_list


def get_guests():
    """
    Return a list of running guests reported from the 'vagrant status' command.
    :return: List of guests
    """
    data = []
    output = subprocess.getoutput(f'vagrant status --machine-readable')
    for i in output.split('\n'):
        if i and i[0].isdigit():
            data.append(i)

    guests = []
    f = io.StringIO('\n'.join(data))
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row[1]:
            if row[2] == 'state' and row[3] == 'running':
                guests.append(row[1])

    return sorted(list(set(guests)))


def worker(guests):
    pool_size = len(guests) if len(guests) < 50 else 50
    pool = ThreadPool(pool_size)

    results = []
    for guest in guests:
        result = pool.apply_async(ssh_config_to_dict, (guest,))
        results.append(result)

    pool.close()
    pool.join()

    data = {}
    for i in results:
        data.update(i.get())
    return data
