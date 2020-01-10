import ast

import pandas as pd


class Extractor(object):
    def __init__(self, files):
        self._functions = 0
        self._classes = 0
        self._methods = 0

        self._row_list = []
        for file in files:
            self._get_data(file)

    def _get_data(self, f_path):
        raise Exception("Not Implemented")

    def _add_entity(self, name, path, line):
        self._row_list.append([name, path, line])

    def get_df(self):
        return pd.DataFrame(self._row_list)

    def __str__(self):
        return '\n\t- functions: ' + str(self._functions) + \
               '\n\t- classes: ' + str(self._classes) + \
               '\n\t- methods: ' + str(self._methods)


class PyExtractor(Extractor):

    def _get_data(self, f_path):
        with open(f_path) as file:
            node = ast.parse(file.read())

        entities = [e for e in node.body if (isinstance(e, ast.FunctionDef) | isinstance(e, ast.ClassDef))]

        m_count = 0
        for entity in entities:
            self._add_entity(entity.name, f_path, entity.lineno)

            if isinstance(entity, ast.ClassDef):
                self._classes += 1
                methods = [m for m in entity.body if isinstance(m, ast.FunctionDef)]

                for method in methods:
                    self._add_entity(method.name, f_path, method.lineno)
                    m_count += 1
            else:
                self._functions += 1
        self._methods += m_count

    def __str__(self):
        stats = super().__str__()
        return '\tPython extractor found:' + stats

