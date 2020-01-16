from utils.misc import indent

DOCSTRING = '''
Knowledge Analysis and Management 2019 - Bad Smells
by Gustavo Graziani

Commands:
{extract_data}
{search_data}


TO SEE DETAILS ON EACH COMMAND, RUN
> python3 bad_smells.py <command> -h/--help
'''

MODULE_DOCSTRINGS = {
    'extract_data': '''
extract_data:
     Extract names of Python and C++ classes, methods, functions.

    Example usage:
        $ python3 multi_search.py extract_data --path lib/tensorflow

    flags:
    -p <path-to-source> | --path <path-to-source>:
        The path to the source code to analyse. Default is "PROJ_ROOT/lib/tensorflow".
''',
    'search_data': '''
search_data:
      Represent code entities using four embeddings: frequency, TF-IDF, LSI and Doc2Vec 
      and report the entities most similar to the given query string.

    Example usage:
        $ python3 multi_search.py search_data --data res/data.csv --query "Optimizer that implements the Adadelta algorithm"

    flags:
    -d <path-to-data> | --data <path-to-data>:
        The path to the csv file containing all the functions, classes and methods information. Default is 
        "PROJ_ROOT/res/data.csv".
''',
    'prec_recall': '''
prec_recall:
      Define the ground truth for a set of queries and measure average precision and recall for the four search 
      engines.

    Example usage:
        $ python3 multi_search.py search_data --data res/data.csv --ground_truth res/gt.txt

    flags:
    -d <path-to-data> | --data <path-to-data>:
        The path to the csv file containing all the functions, classes and methods information. Default is 
        "PROJ_ROOT/res/data.csv".
    -g <path-to-ground-truth> | --ground_truth <path-to-ground-truth>:
        The path to the ground truth file. Default is "PROJ_ROOT/res/gt.txt".
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)
