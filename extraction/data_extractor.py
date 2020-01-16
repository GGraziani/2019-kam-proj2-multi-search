import os
import sys

from definitions import EXTRACTED_DATA_PATH, PROJ_ROOT, RES_PATH
from extraction.extractor import PyExtractor, ClangExtractor
from utils.misc import traverse, save_to_csv, mkdir

py_files = []
clang_files = []


def extract_data(file_path):
    print('\n> Extracting names of classes, function and methods (for .cc and .py files) for source "%s"... ' %
          os.path.basename(file_path))

    traverse(file_path, r'\.py$|\.cc$', collect_files)

    py_extractor = PyExtractor(py_files)
    print(py_extractor)

    clang_extractor = ClangExtractor(clang_files)
    print(clang_extractor)

    mkdir(RES_PATH)
    save_to_csv(
        py_extractor.get_df().append(clang_extractor.get_df()),
        EXTRACTED_DATA_PATH,
        columns=["Name", "File", "Path", "Type"])

    print('\n> Extracted data saved to file "%s"' % os.path.relpath(EXTRACTED_DATA_PATH, PROJ_ROOT))


def collect_files(file):
    py_files.append(file) if file.endswith('.py') else clang_files.append(file)


def extract_data_argparse(args):
    if args.path is None or not os.path.exists(args.path):
        print('"%s" is not a valid path, please enter a path to a source code"...' % args.path)
        sys.exit(0)

    extract_data(file_path=args.path)
