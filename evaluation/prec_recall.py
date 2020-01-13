import os
import sys

import pandas as pd

from definitions import EVALUATION_PATH, PROJ_ROOT
from evaluation.evaluator import Evaluator
from training.search_engine import SearchEngine
from utils.misc import save_to_csv, mkdir


def prec_recall(data, gt):
    search_engine = SearchEngine(data)

    print('\n> Running Evaluation...\n', end='')
    evaluator = Evaluator(search_engine, gt)
    prec, avg_prec_recall = evaluator.evaluate()

    mkdir(EVALUATION_PATH)
    save_to_csv(prec, os.path.join(EVALUATION_PATH, 'precision.csv'))
    save_to_csv(avg_prec_recall, os.path.join(EVALUATION_PATH, 'avg_prec_recall.csv'), index=True)
    print('\n Results of evaluation saved to directory "%s"' % os.path.relpath(EVALUATION_PATH, PROJ_ROOT))

    # print(prec)
    # print(avg_prec_recall)


def prec_recall_argparse(args):
    if args.data is None or not (os.path.exists(args.data) and os.path.isfile(args.data)):
        print('"%s" is not a valid path, please enter a path to a file csv"...' % args.path)
        sys.exit(0)

    if args.gt is None or not (os.path.exists(args.gt) and os.path.isfile(args.gt)):
        print('"%s" is not a valid path, please enter a path to a ground truth file"...' % args.gt)
        sys.exit(0)

    prec_recall(data=pd.read_csv(args.data), gt=args.gt)
