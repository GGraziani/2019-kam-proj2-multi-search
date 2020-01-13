import os

import pandas as pd

from definitions import LIB_PATH


class Evaluator(object):
    def __init__(self, search_engine, gt):

        self._search_engine = search_engine
        self._ground_truth = self._get_ground_truth(gt)

    def _get_ground_truth(self, gt_path):
        with open(gt_path, 'r') as gt_file:
            gt_content = gt_file.read()

        return [test.split('\n')[:3] for test in gt_content.split('\n\n')]

    def evaluate(self):
        final_result = self._run_tests()

        results_dict = {(k1, k2): v2 for k1, v1 in final_result.items() for k2, v2 in final_result[k1].items()}
        precision_df = pd.DataFrame(
            [results_dict[i] for i in sorted(results_dict)],
            index=pd.MultiIndex.from_tuples([i for i in sorted(results_dict.keys())])).reset_index()
        precision_df.columns = ['query n°', 'algorithm', 'precision']

        df_mean = precision_df.groupby('algorithm')['precision'].mean()
        greater_than_zero_count_df = precision_df.groupby('algorithm')['precision'].apply(lambda x: x[x > 0.0].count())
        all_count_df = precision_df.groupby('algorithm')['precision'].count()
        count_merged_df = pd.merge(
            greater_than_zero_count_df,
            all_count_df, on='algorithm')
        count_merged_df['recall'] = count_merged_df['precision_x'] / count_merged_df['precision_y']
        avg_prec_recall_df = pd.merge(df_mean, count_merged_df, on='algorithm')\
            .drop(['precision_x', 'precision_y'], axis=1)

        return precision_df, avg_prec_recall_df

    def _run_tests(self):

        final_result = {}

        for q in range(len(self._ground_truth)):
            query = self._ground_truth[q]
            search_results = self._search_engine.query(query[0])

            final_result[q] = {}

            for algo, top5 in search_results.items():

                final_result[q][algo] = {}
                final_result[q][algo]["precision"] = 0

                for f in range(len(top5)):
                    file = top5[f]

                    path = os.path.join(LIB_PATH, query[2])

                    if file[0] == query[1] and file[1] == path:
                        final_result[q][algo]['precision'] = 1 / (f+1)
                        break

        return final_result
