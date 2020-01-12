import os
import sys

import pandas as pd


def prec_recall(data, gt):
    print(gt)


def prec_recall_argparse(args):
    if args.data is None or not (os.path.exists(args.data) and os.path.isfile(args.data)):
        print('"%s" is not a valid path, please enter a path to a file csv"...' % args.path)
        sys.exit(0)

    if args.gt is None or not (os.path.exists(args.gt) and os.path.isfile(args.gt)):
        print('"%s" is not a valid path, please enter a path to a ground truth file"...' % args.gt)
        sys.exit(0)

    prec_recall(data=pd.read_csv(args.data), gt=args.gt)
