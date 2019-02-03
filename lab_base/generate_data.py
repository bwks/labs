def generate_device_data(device):
    local_pod = int(device[1])
    local_router = int(device[3])
    other_routers = [x for x in range(1, 9) if x != local_router]
    other_pods = [x for x in range(1, 5) if x != local_pod]

    return {
        'local_pod': local_pod,
        'local_router': local_router,
        'other_routers': other_routers,
        'other_pods': other_pods,
    }


def create_p2p(device):
    data = generate_device_data(device)
    local_pod = data['local_pod']
    local_router = data['local_router']

    interfaces = {'p2p_interfaces': {}}
    for remote_router in data['other_routers']:
        low_router = min(data['local_router'], remote_router)
        high_router = max(data['local_router'], remote_router)

        interfaces['p2p_interfaces'][remote_router] = {
            'ipv4_address': f'10.{local_pod}.{low_router}{high_router}.{local_router}/24',
            'ipv6_address': f'fd00:10:{local_pod}:{low_router}{high_router}::{local_router}/64'
        }
    return interfaces


def create_sub_interface(device):
    data = generate_device_data(device)
    local_pod = data['local_pod']
    local_router = data['local_router']

    interfaces = {'sub_interfaces': {}}
    for remote_router in data['other_routers']:
        low_router = min(data['local_router'], remote_router)
        high_router = max(data['local_router'], remote_router)

        interfaces['sub_interfaces'][f'9.{data["local_pod"]}{low_router}{high_router}'] = {
            'ipv4_address': f'10.{local_pod}{local_pod}.{low_router}{high_router}.{local_router}/24',
            'ipv6_address': f'fd00:10:{local_pod}{local_pod}:{low_router}{high_router}::{local_router}/64'
        }

    for remote_pod in data['other_pods']:
        low_pod = min(data['local_pod'], remote_pod)
        high_pod = max(data['local_pod'], remote_pod)
        for remote_router in range(1, 9):
            low_router = min(data['local_router'], remote_router)
            high_router = max(data['local_router'], remote_router)

            interfaces['sub_interfaces'][f'9.{low_pod}{high_pod}{low_router}{high_router}'] = {
                'ipv4_address': f'10.{low_pod}{high_pod}.{low_router}{high_router}.{local_pod}{local_router}/24',
                'ipv6_address': f'fd00:10:{low_pod}{high_pod}:{low_router}{high_router}::{local_pod}{local_router}/64'
            }
    return interfaces


def create_loopback(device):
    data = generate_device_data(device)
    local_pod = data["local_pod"]
    local_router = data["local_router"]
    return {
        'loopbacks': {'0': {
            'ipv4_address': f'10.255.{local_pod}.{local_router}/32',
            'ipv6_address': f'fd00:10:255:{local_pod}::{local_router}/128',
            }
        }
    }


def generate_vlans(data):
    all_vlans = []
    for k, v in data.items():
        for subint in v['sub_interfaces']:
            all_vlans.append(int(subint.split('.')[-1]))

    sorted_vlans = sorted(set(all_vlans))

    interpod_vlans = []
    pod1_vlans = []
    pod2_vlans = []
    pod3_vlans = []
    pod4_vlans = []

    for vlan in sorted_vlans:
        _vlan = str(vlan)
        if len(_vlan) == 3:
            if _vlan.startswith('1'):
                pod1_vlans.append(vlan)
            elif _vlan.startswith('2'):
                pod2_vlans.append(vlan)
            elif _vlan.startswith('3'):
                pod3_vlans.append(vlan)
            elif _vlan.startswith('4'):
                pod4_vlans.append(vlan)
        else:
            interpod_vlans.append(vlan)

    return {
        'all': sorted_vlans,
        'inter-pod': interpod_vlans,
        'pod1': pod1_vlans,
        'pod2': pod2_vlans,
        'pod3': pod3_vlans,
        'pod4': pod4_vlans,
        }


def generate_router_list():
    routers = []
    for pod in range(1, 5):
        for router in range(1, 9):
            routers.append(f'p{pod}r{router}')
    return routers


def generate_data():
    routers = generate_router_list()

    data = {'routers': {}}
    for router in routers:
        interfaces = create_p2p(router)
        sub_interfaces = create_sub_interface(router)
        loopbacks = create_loopback(router)
        data['routers'][router] = {**interfaces, **sub_interfaces, **loopbacks}

    data['vlans'] = generate_vlans(data['routers'])
    return data
