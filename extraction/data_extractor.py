import os
import sys

from extraction.extractor import PyExtractor
from utils.misc import traverse

py_files = []
clang_files = []


def extract_data(file_path):
    print('\n> Extracting names of classes, function and methods (for .cc and .py files) for source "%s"... ' %
          os.path.basename(file_path))

    traverse(file_path, r'\.py$|\.cc$', collect_files)

    py_extractor = PyExtractor(py_files)
    print(py_extractor)


def collect_files(file):
    py_files.append(file) if file.endswith('.py') else clang_files.append(file)


def extract_data_argparse(args):
    if args.path is None or not os.path.exists(args.path):
        print('"%s" is not a valid path, please enter a path to a source code"...' % args.path)
        sys.exit(0)

    extract_data(file_path=args.path)
