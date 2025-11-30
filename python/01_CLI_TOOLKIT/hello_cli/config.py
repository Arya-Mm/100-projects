import json
import os

def load_config(path):
    """
    Load the configuration file.
    If config does not exist, return default settings.
    """
    if not os.path.exists(path):
        return {"greeting": "Hello"}

    with open(path, "r") as f:
        return json.load(f)
