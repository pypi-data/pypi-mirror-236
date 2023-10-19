import os, requests
from zhmiscellany import string


def download_file(url, file_path, ext):
    file_path = f'{string.truncate_string(file_path, (260-len(ext)))}{ext}'
    if not os.path.exists(file_path):
        response = requests.get(url)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True
    else:
        return False