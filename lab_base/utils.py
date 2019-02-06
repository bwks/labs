import json


def load_ssh_config():
    with open('.sshconfig.json', 'r') as f:
        return json.load(f)
