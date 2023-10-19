import json


def create_json_generator(file_path):

    with open(file_path, 'r') as file:

        for json_line in file:
            try:
                json_data = json.loads(json_line)
                yield json_data
            except json.JSONDecodeError:
                continue
