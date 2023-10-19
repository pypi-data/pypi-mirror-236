import json, os, shutil, time, string


def read_json_file(file_path):
    """
    Reads JSON data from a file and returns it as a dictionary.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_json_file(file_path, data):
    """
    Writes a dictionary to a JSON file.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def remove_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)


def base_name_no_ext(file_path):
    base_name = os.path.basename(file_path)
    base_name_without_extension, _ = os.path.splitext(base_name)
    return base_name_without_extension


def convert_to_base62(number):
    # Base 62 characters: digits (0-9), lowercase letters (a-z), and uppercase letters (A-Z)
    base62_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
    if number == 0:
        return base62_chars[0]

    base62_str = ''
    while number > 0:
        number, remainder = divmod(number, 62)
        base62_str = base62_chars[remainder] + base62_str

    return base62_str


def get_universally_unique_string():
    #number = None
    #if not number:
    timestamp = str(time.time()).replace('.', '')
    #else:
    #    timestamp = number
    unique_number = int(timestamp)

    unique_filename = convert_to_base62(unique_number)
    return unique_filename