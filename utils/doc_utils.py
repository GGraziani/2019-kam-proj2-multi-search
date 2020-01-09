from utils.misc import indent

DOCSTRING = '''
Knowledge Analysis and Management 2019 - Bad Smells
by Gustavo Graziani

Commands:
{extract_data}


TO SEE DETAILS ON EACH COMMAND, RUN
> python3 bad_smells.py <command>
'''

MODULE_DOCSTRINGS = {
    'extract_data': '''
extract_data:
     Extract names of Python and C++ classes, methods, functions.

    Example usage:
        $ python3 multi_search.py extract_data

    flags:
    -s <path-to-file> | --source <path-to-file>:
        The path to the "tree.py" file. Default is "PROJ_ROOT/lib/tree.py"
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)
