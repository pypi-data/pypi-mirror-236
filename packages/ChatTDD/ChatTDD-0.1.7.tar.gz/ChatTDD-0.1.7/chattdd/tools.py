import re
import json
import os

CONFIG_FILE_PATH = os.path.join(os.getcwd(), 'chattdd_config.json')


def load_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        # Create config file with default values if it doesn't exist
        default_config = {
            "CHATTDD_MODEL": "text-davinci-003",
            "OUTPUTFOLDER": "chattdd"
        }
        with open(CONFIG_FILE_PATH, 'w') as file:
            json.dump(default_config, file, indent=4)
        return default_config
    else:
        with open(CONFIG_FILE_PATH, 'r') as file:
            return json.load(file)


def update_config(key, value):
    config = load_config()
    config[key] = value
    with open(CONFIG_FILE_PATH, 'w') as file:
        json.dump(config, file, indent=4)


def extract_json(s):
    match = re.search(r'{\s*.*\s*}', s, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            # Optionally, check if it's valid JSON
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            print("Matched string is not valid JSON")
            return None
    else:
        print("No JSON found")
        return None
