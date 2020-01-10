from utils.misc import indent

DOCSTRING = '''
Knowledge Analysis and Management 2019 - Bad Smells
by Gustavo Graziani

Commands:
{extract_data}
{search_data}


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
        The path to the source code to analyse. Default is "PROJ_ROOT/lib/tensorflow".
''',
    'search_data': '''
search_data:
      Represent code entities using four embeddings: frequency, TF-IDF, LSI and Doc2Vec 
      and report the entities most similar to the given query string.

    Example usage:
        $ python3 multi_search.py search_data --data res/data.csv

    flags:
    -d <path-to-data> | --data <path-to-data>:
        The path to the csv file containing all the functions, classes and methods information. Default is 
        "PROJ_ROOT/res/data.csv".
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)
