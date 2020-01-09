import os
import sys


def extract_data(file_path):
    print(file_path)


def extract_data_argparse(args):
    if args.path is None or not os.path.exists(args.path):
        print('Enter a valid path to a source code"...')
        sys.exit(0)

    extract_data(file_path=args.path)