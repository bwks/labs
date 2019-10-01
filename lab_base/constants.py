import os


BASE_DIR = os.path.join(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATE_MAP = {
    'vmx': 'juniper-vmx.j2',
    'vqfx': 'juniper-vqfx.j2',
    'veos': 'arista-veos.j2',
    'cvx': 'cumulus-vx.j2',
}
