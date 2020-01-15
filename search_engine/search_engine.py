from training.corpus import Corpus


class SearchEngine:
    def __init__(self, data):
        print('\n> Initializing the search engine... ')
        self.corpus = Corpus(df=data)
        self.query_results = {}

    def query(self, query):
        print('\n> Query: "%s"... ' % query)
        words = query.lower().split()

        self.query_results['freq'] = self.corpus.freq(words)
        self.query_results['tf-idf'] = self.corpus.tf_idf(words)
        self.query_results['lsi'] = self.corpus.lsi(words)
        self.query_results['doc2v'] = self.corpus.doc2v(words)

        self.print_query_results()

        return self.query_results

    def print_query_results(self):
        if len(self.query_results) > 0:
            if self.query_results['freq'] is not None:
                print('\t 1. Freq results...')
                for res in self.query_results['freq']:
                    print('\t\t', res)
            if self.query_results['tf-idf'] is not None:
                print('\t 2. Tf-idf results...')
                for res in self.query_results['tf-idf']:
                    print('\t\t', res)
            if self.query_results['lsi'] is not None:
                print('\t 3. LSI results...')
                for res in self.query_results['lsi']:
                    print('\t\t', res)
            if self.query_results['doc2v'] is not None:
                print('\t 4. Doc2V results...')
                for res in self.query_results['doc2v']:
                    print('\t\t', res)
