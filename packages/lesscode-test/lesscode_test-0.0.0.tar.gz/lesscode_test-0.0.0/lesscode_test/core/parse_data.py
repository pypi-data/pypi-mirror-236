import json

import yaml


def parse_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
    return data


def parse_json(path):
    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data
