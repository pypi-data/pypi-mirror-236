import json


def standardize_string(input_str):
    input_str = input_str.replace("'", '"')
    input_str = input_str.replace("\n", "\\n")
    return json.dumps(json.loads(input_str), ensure_ascii=False)