import os
import json


def ensure_dir(dirname):

    if not os.path.exists(dirname):
        os.makedirs(dirname)


def ensure_file(file_path, default_contents):

    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file_object:
            json.dump(default_contents, file_object)