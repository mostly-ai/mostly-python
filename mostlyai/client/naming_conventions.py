import re
from typing import Callable


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(camel_str: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def convert_case(input_data: dict, conv_func: Callable[[str], str]) -> dict:
    if not isinstance(input_data, dict):
        return input_data

    new_dict = {}
    for key, value in input_data.items():
        new_key = conv_func(key)
        # recursively convert nested dictionaries or lists
        if isinstance(value, dict):
            new_dict[new_key] = convert_case(value, conv_func)
        elif isinstance(value, list):
            new_dict[new_key] = [
                convert_case(item, conv_func) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            new_dict[new_key] = value
    return new_dict


def map_snake_to_camel_case(input_dict: dict) -> dict:
    return convert_case(input_dict, snake_to_camel)


def map_camel_to_snake_case(input_dict: dict) -> dict:
    return convert_case(input_dict, camel_to_snake)
