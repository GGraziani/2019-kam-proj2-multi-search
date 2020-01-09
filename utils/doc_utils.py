from utils.misc import indent

DOCSTRING = '''
Knowledge Analysis and Management 2019 - Bad Smells
by Gustavo Graziani

Commands:
{onto_creator}
{individ_creator}
{find_bad_smells}


TO SEE DETAILS ON EACH COMMAND, RUN
> python3 bad_smells.py <command>
'''

MODULE_DOCSTRINGS = {
    'onto_creator': '''
onto_creator:
     Creates an ontology for Java entities.

    Example usage:
        $ python3 bad_smells.py onto_creator

    flags:
    -s <path-to-file> | --source <path-to-file>:
        The path to the "tree.py" file. Default is "PROJ_ROOT/lib/tree.py"
''',
    'individ_creator': '''
individ_creator:
    Populates the ontology (tree.owl) with instances of ClassDeclaration, MethodDeclaration, FieldDeclaration, 
    Statement subclasses (e.g., IfStatement, WhileStatement, etc.) and FormalParameter.

    Example usage:
        $ python3 bad_smells.py individ_creator

    flags:
    -s <path-to-source> | --source <path-to-source>:
        The path to a directory containing java files. Default is "PROJ_ROOT/lib/android-chess/app/src/main/java/jwtc/chess"
''',
    'find_bad_smells': '''
find_bad_smells:
    Runs Sparql queries to detect bad smells (Long Method, Large Class, Long Parameter List, Switch Statements, Data Class).

    Example usage:
        $ python3 bad_smells.py find_bad_smells
'''
}


def docstring_preview(text):
    return text.split('\n\n')[0]


docstring_headers = {
    key: indent(docstring_preview(value))
    for (key, value) in MODULE_DOCSTRINGS.items()
}

DOCSTRING = DOCSTRING.format(**docstring_headers)
