from re import finditer

import gensim
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, similarities, models

from utils.misc import get_not_unique_words, w_2_tagged_doc


class SearchEngine:
    def __init__(self, data):
        self.corpus = Corpus(df=data)


class Corpus:
    def __init__(self, df):
        self.words = self._process_names(df)
        self._train()

    def _process_names(self, df):

        processed_names = []

        for name in df[df.columns[0]]:
            words = self._split_name(name)
            if len(words) > 0:
                processed_names.append(words)

        return processed_names

    def _split_name(self, name):
        words = []
        if isinstance(name, str):  # ignore random nan values
            matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|.*_.*|$)', name)

            for match in matches:
                words = [match.group(0)]
                if words[0].__contains__('_'):
                    words = words[0].split("_")

        return [word.lower() for word in words if word != '' and word not in STOPWORDS]

    def _train(self):
        self._freq_train()

    def _freq_train(self):
        self._freq_dict = corpora.Dictionary(self.words)
        bow_list = [self._freq_dict.doc2bow(text) for text in self.words]
        self._freq_index = similarities.SparseMatrixSimilarity(bow_list, num_features=len(self._freq_dict))

