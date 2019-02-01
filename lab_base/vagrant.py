import csv
import subprocess
import io

from multiprocessing.pool import ThreadPool


def get_ssh_config(guest):
    """
    Returns a dictionary of SSH config for each device.
    :param guests: A list of guests
    :return: Dict of devices SSH config
    """
    return subprocess.getoutput(f'vagrant ssh-config {guest}')


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
        result = pool.apply_async(get_ssh_config, (guest,))
        results.append(result)

    pool.close()
    pool.join()

    return [i.get() for i in results]
