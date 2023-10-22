def read_file(filename: str):
    with open(filename, 'r') as file:
        data = file.read()
        return data
def write_file(filename: str, content_to_write):
    with open(filename, 'w') as file:
        file.write(content_to_write)
        return
def random(minint, maxint):
    from random import randint
    randint(minint, maxint)
def list_sum(list):
    a = sum(list)
    return a
def print_dict(dictionary: dict):
    data = ''
    for key, value in dictionary.items():
        data += f"{key}: {value}\n"
    return data
