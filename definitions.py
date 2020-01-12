import os

PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))   # Project root path

TENSORFLOW_PATH = os.path.join(PROJ_ROOT, 'lib/tensorflow')
EXTRACTED_DATA_PATH = os.path.join(PROJ_ROOT, 'res/data.csv')
GROUND_TRUTH_PATH = os.path.join(PROJ_ROOT, 'res/ground-truth.txt')
