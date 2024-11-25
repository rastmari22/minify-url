import json
import os


def get(data, key):
    value = data[key]
    env = os.environ.get(key.upper())
    if env is None:
        return value
    else:
        if isinstance(value, bool):
            return env != "0"
        elif isinstance(value, int):
            return int(env)
        elif isinstance(value, float):
            return float(env)
        else:
            return env


class Configuration:
    def __init__(self):
        filename = os.environ.get("FLASK_CONFIG", "./config.json")
        if os.path.exists(filename):
            with open(filename, encoding="utf8") as data:
                obj = json.load(data)
                for key in obj:
                    setattr(self, key.upper(), get(obj, key))