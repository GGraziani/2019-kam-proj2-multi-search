import os
import re
from collections import defaultdict
from re import finditer

import gensim
from gensim import models
from gensim.parsing.preprocessing import STOPWORDS


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


def split_name(name):
    words = []
    if isinstance(name, str):  # ignore random "nan" values
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|.*_.*|$)', name)

        for match in matches:
            words = [match.group(0)]
            if words[0].__contains__('_'):
                words = words[0].split("_")

    return [word.lower() for word in words if word != '' and word not in STOPWORDS]


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


# ------- QUERY ------- #


def get_top_five(df, similarity):
    c = 0
    top_five = []
    for doc_number, score in sorted(enumerate(similarity), key=lambda x: x[1], reverse=True):
        if c >= 5:
            break
        else:
            top_five.append(df.iloc[doc_number].values.tolist())
            c += 1
    return top_five
