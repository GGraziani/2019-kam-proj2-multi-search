import os
import re


def indent(text, spaces=4):
    spaces = ' ' * spaces
    return '\n'.join(spaces + line if line.strip() != '' else line for line in text.split('\n'))


def listget(li, index, fallback=None):
    try:
        return li[index]
    except IndexError:
        return fallback


def traverse(path, regex, callback):
    regex = re.compile(regex)
    for dirpath, dirnames, filenames in os.walk(path):
        for f_name in filter(regex.search, filenames):
            f_path = os.path.join(dirpath, f_name)
            callback(f_path)
