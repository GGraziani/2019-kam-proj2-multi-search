import sys
import argparse

from definitions import *
from utils.doc_utils import *
from utils.misc import list_get


# add one gateway function for each functionality

def extract_data_gateway(args):
    from extraction import data_extractor
    data_extractor.extract_data_argparse(args)


def search_data_gateway(args):
    from training import search_data
    search_data.search_data_argparse(args)


def prec_recall_gateway(args):
    from evaluation import prec_recall
    prec_recall.prec_recall_argparse(args)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# add subparser for extract_data
p_extract_data = subparsers.add_parser('extract_data')
p_extract_data.add_argument('-p', '--path', dest='path', default=TENSORFLOW_PATH)
p_extract_data.set_defaults(func=extract_data_gateway)

# add subparser for search_data
p_search_data = subparsers.add_parser('search_data')
p_search_data.add_argument('-d', '--data', dest='data', default=EXTRACTED_DATA_PATH)
p_search_data.add_argument('-q', '--query', dest='query', default='Optimizer that implements '
                                                                  'the Adadelta algorithm')
p_search_data.set_defaults(func=search_data_gateway)

# add subparser for prec_recall
p_prec_recall = subparsers.add_parser('prec_recall')
p_prec_recall.add_argument('-d', '--data', dest='data', default=EXTRACTED_DATA_PATH)
p_prec_recall.add_argument('-g', '--ground_truth', dest='gt', default=GROUND_TRUTH_PATH)
p_prec_recall.set_defaults(func=prec_recall_gateway)


def main(argv):
    helpstrings = {'-h', '--help'}

    command = list_get(argv, 0, '').lower()

    # The user did not enter a command, or the entered command is not recognized.
    if command not in MODULE_DOCSTRINGS:
        print(DOCSTRING)
        if command == '':
            print('You are seeing the default help text because you did not choose a command.')
        elif command not in helpstrings:
            print('You are seeing the default help text because "%s" was not recognized' % command)
        return 1

    # The user entered a command, but no further arguments, or just help.
    argument = list_get(argv, 1, '').lower()
    if argument in helpstrings:
        print(MODULE_DOCSTRINGS[command])
        return 1

    args = parser.parse_args(argv)
    args.func(args)

    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
