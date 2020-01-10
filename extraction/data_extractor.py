import os
import sys

from utils.misc import traverse

py_files = []
clang_files = []


def extract_data(file_path):
    traverse(file_path, r'\.py$|\.cc$', collect_files)

    print(py_files)
    print(clang_files)


def collect_files(file):
    py_files.append(file) if file.endswith('.py') else clang_files.append(file)


def extract_data_argparse(args):
    if args.path is None or not os.path.exists(args.path):
        print('"%s" is not a valid path, please enter a path to a source code"...' % args.path)
        sys.exit(0)

    extract_data(file_path=args.path)
