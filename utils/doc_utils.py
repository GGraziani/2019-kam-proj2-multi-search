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
    -s <path-to-source> | --source <path-to-source>:
        The path to the source code to analyse. Default is "PROJ_ROOT/lib/tensorflow"
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)
