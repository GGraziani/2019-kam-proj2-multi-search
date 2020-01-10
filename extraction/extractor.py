import pandas as pd


class Extractor:
    def __init__(self, files):
        self.m_names = 0
        self.c_names = 0
        self.f_names = 0

        self.files = files
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
        print(' - functions = "%s"\n - classes = "%s"\n - methods = "%s"\n' %
              (str(self.f_names), str(self.c_names), str(self.m_names)))
