import os
import sys


def extract_data(file_path):
    print(file_path)


def create_ontology_argparse(args):
    if args.path is None or not (os.path.exists(args.path) and os.path.isfile(args.path)):
        print('Enter a valid path to a file "tree.py"...')
        sys.exit(0)

    extract_data(file_path=args.path)