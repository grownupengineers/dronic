# TODO consider using TOML or YAML for the configuration

import json
import os

# global config variable
CONFIG = {}

DEFAULT_CONFIG_FILE = ".dronic.cfg"


def load_config(file: str = DEFAULT_CONFIG_FILE):
    global CONFIG

    if not os.path.exists(file):
        # fail silently
        return

    with open(file) as fd:
        CONFIG = json.load(fd)


def dump_config(file: str = DEFAULT_CONFIG_FILE):
    with open(file, "w") as fd:
        json.dump(CONFIG, fd)
