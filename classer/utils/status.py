"""
Utilities for setting and getting the status of an environment.
"""

import json


def get_status(status_file):

    status_history = read_status_file(status_file)

    if not status_history:
        return ''

    last_update = status_history[-1]
    return last_update


def get_status_history(status_file):

    status_history = read_status_file(status_file)
    return status_history


def set_status(status_file, status):

    status_history = read_status_file(status_file)
    status_history.append(status)

    if len(status_history) > 5:
        status_history = status_history[-5:]

    with open(status_file, 'w') as status_file_object:
        json.dump(status_history, status_file_object)


def read_status_file(status_file):

    try:
        with open(status_file, 'r') as status_file_object:
            return json.load(status_file_object)

    except IOError:
        # File does not exist
        return []
