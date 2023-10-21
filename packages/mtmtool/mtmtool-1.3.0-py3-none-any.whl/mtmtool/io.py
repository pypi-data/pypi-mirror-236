import pickle
import json
import yaml


def read_pkl(path):
    with open(path, "rb") as f:
        res = pickle.load(f)
    return res


def write_pkl(data, path):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def read_txt(path, encoding="utf8"):
    with open(path, "r", encoding=encoding) as f:
        data = f.read()
    return data


def write_txt(data, path, encoding="utf8"):
    with open(path, "w", encoding=encoding) as f:
        f.write(data)


def read_json(path):
    with open(path, "r", encoding="utf8") as f:
        data = f.read()
    res = json.loads(data)
    return res


def write_json(data, path):
    with open(path, "w") as f:
        f.write(json.dumps(data, separators=(',', ':')))


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.load(f.read(), Loader=yaml.Loader)
    return data
