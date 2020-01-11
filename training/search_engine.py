import gensim
from gensim import corpora, similarities, models

from utils.misc import get_not_unique_words, w_2_tagged_doc, split_name, get_top_five


class SearchEngine:
    def __init__(self, data):
        print('\n> Initializing the search engine... ')
        self.corpus = Corpus(df=data)

    def query(self, query):
        print('\n> Query: "%s"... ' % query)
        results = {}
        words = query.lower().split()


class Corpus:
    def __init__(self, df):
        self._df = df
        self.words = self._process_names(self._df)
        self._train()

    def _process_names(self, df):
        print('\t- Processing filenames... ', end='')

        processed_names = []

        for name in df[df.columns[0]]:
            words = split_name(name)
            if len(words) > 0:
                processed_names.append(words)
        print(' done. Processed %s filenames.' % len(processed_names))
        return processed_names

    def _train(self):
        print('\t- Training the search engine:')
        self._freq_train()
        self._tf_idf_train()
        self._lsi_train()
        # self._doc2v_train()

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
