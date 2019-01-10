import pathlib


def make_config(pod_number=1):

    for local_router in range(1, 9):
        local_router_name = f'p{pod_number}r{local_router}'
        config = [
            f'set system host-name {local_router_name}',
            'set protocols lldp interface all',
            'set protocols lldp port-id-subtype interface-name',
        ]
        other_routers = [x for x in range(1, 9) if x != local_router]

        for remote_router in other_routers:
            low_router = min(local_router, remote_router)
            high_router = max(local_router, remote_router)

            config.append(f'set interfaces ge-0/0/{remote_router}.0 family inet address 10.{pod_number}.{low_router}{high_router}.{local_router}/24')
            config.append(f'set interfaces ge-0/0/{remote_router}.0 family inet6 address fd00:0:{pod_number}:{low_router}{high_router}::{local_router}/64')

        with open(f'config/{local_router_name}.cfg', 'w') as f:
            f.write('\n'.join(config))


if __name__ == '__main__':
    config_dir = pathlib.Path('config')
    config_dir.mkdir(exist_ok=True)
    for pod in range(1, 5):
        make_config(pod)
