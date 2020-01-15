import gensim
import pandas as pd
from gensim import corpora, similarities, models
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

from utils.misc import get_not_unique_words, w_2_tagged_doc, split_name, get_top_five


class Corpus:
    def __init__(self, df):
        self._df = df
        self.words = self._process_names()

        self._train()

    def _process_names(self):
        print('\t- Processing filenames... ', end='')

        all_names = self._df[self._df.columns[0]]
        processed_names = []
        for name in all_names:
            words = split_name(name)
            if words is not None:
                processed_names.append(words)
        print(' done. Processed %s filenames.' % len(processed_names))
        return processed_names

    def _train(self):
        print('\t- Training the search engine:')
        self._freq_train()
        self._tf_idf_train()
        self._lsi_train()
        self._doc2v_train()

    def _freq_train(self):
        print('\t\t 1. Frequency training...', end='')
        self._freq_dict = corpora.Dictionary(self.words)
        bow_list = [self._freq_dict.doc2bow(text) for text in self.words]
        self._freq_index = similarities.SparseMatrixSimilarity(bow_list, num_features=len(self._freq_dict))
        print(' done.')

    def _tf_idf_train(self):
        print('\t\t 2. TF-IDF training...', end='')
        self._tf_idf_dict = corpora.Dictionary(self.words)
        bow_list = [self._tf_idf_dict.doc2bow(text) for text in self.words]

        self._tf_idf_model = models.TfidfModel(bow_list)
        self._tf_idf_index = similarities.SparseMatrixSimilarity(
            self._tf_idf_model[bow_list],
            num_features=len(self._tf_idf_dict))
        print(' done.')

    def _lsi_train(self):
        print('\t\t 3. LSI training...', end='')
        not_unique_words = get_not_unique_words(self.words)

        self._lsi_dict = corpora.Dictionary(not_unique_words)
        bow_list = [self._lsi_dict.doc2bow(text) for text in not_unique_words]

        tf_idf_model = models.TfidfModel(bow_list)
        tf_idf_corpus = tf_idf_model[bow_list]

        self._lsi_model = models.LsiModel(tf_idf_corpus, id2word=self._lsi_dict, num_topics=200)
        self._lsi_corpus = self._lsi_model[tf_idf_corpus]
        self._lsi_index = similarities.MatrixSimilarity(self._lsi_model[bow_list])
        print(' done.')

    def _doc2v_train(self):
        print('\t\t 4. Doc2Vec training...', end='')
        not_unique_words = get_not_unique_words(self.words)
        self._tagged_docs = list(w_2_tagged_doc(not_unique_words))
        self._d2v_model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=20)
        self._d2v_model.build_vocab(self._tagged_docs)
        self._d2v_model.train(self._tagged_docs, total_examples=self._d2v_model.corpus_count,
                              epochs=self._d2v_model.epochs)
        print(' done.')

    def freq(self, words):
        bow = self._freq_dict.doc2bow(words)
        similarity = self._freq_index[bow]

        return get_top_five(self._df, similarity)

    def tf_idf(self, words):
        bow = self._tf_idf_dict.doc2bow(words)
        similarity = self._tf_idf_index[self._tf_idf_model[bow]]

        return get_top_five(self._df, similarity)

    def lsi(self, words):
        bow = self._lsi_dict.doc2bow(words)
        similarity = self._lsi_index[self._lsi_model[bow]]

        return get_top_five(self._df, similarity)

    def lsi_viz(self, words):
        bow = self._lsi_dict.doc2bow(words)
        vector = self._lsi_model[bow]
        similarity = abs(self._lsi_index[vector])

        c = 0
        ret = [self._lsi_model[bow]]
        for doc_number, score in sorted(enumerate(similarity), key=lambda x: x[1], reverse=True):
            if c >= 5:
                break
            else:
                ret.append(self._lsi_corpus[doc_number])
                c += 1

        return ret

    def doc2v(self, words):
        vector = self._d2v_model.infer_vector(words)
        top_most_similar = self._d2v_model.docvecs.most_similar([vector], topn=5)

        top_five = []
        for label, index in [('FIRST', 0), ('SECOND', 1), ('THIRD', 2), ('FOURTH', 3), ('FIFTH', 4)]:
            top_five.append(self._df.iloc[top_most_similar[index][0]].values.tolist())
        return top_five

    def doc2v_viz(self, words):
        vector = self._d2v_model.infer_vector(words)
        top_most_similar = [doc for doc in self._d2v_model.docvecs.most_similar([vector], topn=5)]

        doc2vec_list = [self._d2v_model.infer_vector(words)]
        for hit_idx, sim in top_most_similar:
            doc_words = self.words[hit_idx]
            doc2vec_list.append(self._d2v_model.infer_vector(doc_words))

        return doc2vec_list

