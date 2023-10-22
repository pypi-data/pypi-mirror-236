import os
from chattdd.tools import load_config


def write_to_file(content, filename):
    config = load_config()
    output_folder = config['OUTPUTFOLDER']
    file_path = os.path.join(output_folder, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)