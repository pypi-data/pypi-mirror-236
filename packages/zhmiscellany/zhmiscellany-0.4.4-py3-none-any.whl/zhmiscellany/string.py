import string, time


def convert_to_base62(number):
    number = int(str(number).replace('.', ''))
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
    timestamp = str(time.perf_counter_ns()).replace('.', '')
    #else:
    #    timestamp = number
    unique_number = int(timestamp)

    unique_filename = convert_to_base62(unique_number)
    return unique_filename


def multi_replace(string, replaces):
    for i in replaces:
        string = string.replace(i[0], i[1])
    return string


def convert_name_to_filename(name):
    return multi_replace(name, [("/","["), (":","]"), (".","+")])


def convert_filename_to_name(filename):
    return multi_replace(filename, [("[","/"), ("]",":"), ("+",".")])