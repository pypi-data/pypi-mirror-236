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
    try:
        start_idx = s.index('{')
        end_idx = s.rindex('}') + 1  
    except ValueError:
        print("No JSON found")
        return None
    
    json_str = s[start_idx:end_idx]
    try:
        json_object = json.loads(json_str)
        return json.dumps(json_object, indent=4) 
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return None
