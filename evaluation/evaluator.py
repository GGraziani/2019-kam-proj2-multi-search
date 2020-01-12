

class Evaluator(object):
    def __init__(self, search_engine, gt):

        self._search_engine = search_engine
        self._ground_truth = self._get_ground_truth(gt)
        # self._final_results = \
        self._run_tests()


    def _get_ground_truth(self, gt_path):
        with open(gt_path, 'r') as gt_file:
            gt_content = gt_file.read()

        return [test.split('\n')[:3] for test in gt_content.split('\n\n')]

    def _run_tests(self):

        final_result = {}

        for q in range(len(self._ground_truth)):
            query = self._ground_truth[q]
            query_results = self._search_engine.query(query[0])

            final_result[q] = {}

            for algo, res in query_results.items():
                print(algo)



