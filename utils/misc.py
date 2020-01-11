import os
import re
from collections import defaultdict

import gensim
from gensim import models


def indent(text, spaces=4):
    spaces = ' ' * spaces
    return '\n'.join(spaces + line if line.strip() != '' else line for line in text.split('\n'))


def list_get(li, index, fallback=None):
    try:
        return li[index]
    except IndexError:
        return fallback


def traverse(path, regex, callback):
    regex = re.compile(regex)
    for dirpath, dirnames, filenames in os.walk(path):
        for f_name in filter(regex.search, filenames):
            f_path = os.path.join(dirpath, f_name)
            callback(f_path)


# ------- TRAINING ------- #


def get_not_unique_words(words):
    frequency = defaultdict(int)
    for text in words:
        for token in text:
            frequency[token] += 1
    return [[token for token in text if frequency[token] > 1] for text in words]


def w_2_tagged_doc(words):
    for i, line in enumerate(words):
        line = " ".join(line)
        yield models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])
