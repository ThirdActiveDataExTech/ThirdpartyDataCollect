import os
import uuid


def make_file_path(url):
    file_name = str(uuid.uuid4()) + ".txt"
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_dir = os.path.join(root_dir, 'scripts')
    file_path = file_dir + file_name
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    return file_path
