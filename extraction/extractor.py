import ast
import pandas as pd

import clang
import clang.cindex
from clang.cindex import *


clang.cindex.Config.set_library_path("/usr/local/Cellar/llvm/9.0.0_1/lib/")


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
               '\n\t- methods: ' + str(self._methods) + \
               '\n\t- Total entities: ' + str(self._functions + self._classes + self._methods)


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
        return '\n\tPython extractor found:' + stats


class ClangExtractor(Extractor):
    def __init__(self, files):
        self.index = clang.cindex.Index.create()
        super().__init__(files)

    def _get_data(self, f_path):
        cursor = self.index.parse(f_path, ["c++"]).cursor
        self._get_data_helper(cursor, f_path)

    def _get_data_helper(self, cursor, f_path):
        for i in cursor.get_children():
            self._walk(i, f_path)

    def _walk(self, node, f_path):
        if node.is_definition():
            if node.kind == CursorKind.CLASS_DECL:
                self._add_entity(node.spelling, f_path, node.location.line)
                self._classes += 1
            elif node.kind == CursorKind.CXX_METHOD:
                self._add_entity(node.spelling, f_path, node.location.line)
                self._methods += 1
            elif node.kind == CursorKind.FUNCTION_DECL:
                self._add_entity(node.spelling, f_path, node.location.line)
                self._functions += 1

        self._get_data_helper(node, f_path)

    def __str__(self):
        stats = super().__str__()
        return '\n\tClang extractor found:' + stats
