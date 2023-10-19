"""
convertor for camel and snake cases.
"""


def camel_to_snake(name: str) -> str:
    """
    Replace each uppercase letter with an
    underscore and the lowercase version of that letter
    """
    result = [name[0].lower()]
    for char in name[1:]:
        if char.isupper():
            result.extend(['_', char.lower()])
        else:
            result.append(char)
    return ''.join(result)


def to_snake_case(d: dict) -> dict:
    """
    utility function for camel_to_snake
    """
    if isinstance(d, dict):
        new_dict = {}
        for key, value in d.items():
            if isinstance(value, dict):
                new_dict[camel_to_snake(key)] = to_snake_case(value)
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, dict):
                        new_list.append(to_snake_case(item))
                    else:
                        new_list.append(item)
                new_dict[camel_to_snake(key)] = new_list
            else:
                new_dict[camel_to_snake(key)] = value
        return new_dict

    elif isinstance(d, list):
        new_list = []
        for item in d:
            if isinstance(item, dict):
                new_list.append(to_snake_case(item))
            else:
                new_list.append(item)
        return new_list
    else:
        return d
