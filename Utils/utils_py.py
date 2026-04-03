import inspect
import json
import os

from loguru import logger

def function_list(module):
    members = inspect.getmembers(module, inspect.isfunction)

    functions = []
    for item in members:
        functions.append(item[0])

    return functions


def init_config():
    default_config = {
        "modules": { },
        "logger": {
            "rotation": "10 MB",
            "compression": "zip",
            "retention": "15 days"
        }
    }
    # if exists
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    else:
        # write
        with open("config.json", "w") as f:
            json.dump(default_config, f)
        return default_config


def add_module_to_config(module_name, global_config, config):
    global_config["modules"][module_name] = config
    with open("config.json", "w") as f:
        logger.info(f"[{module_name}] {config}")
        json.dump(global_config, f)
    return global_config


