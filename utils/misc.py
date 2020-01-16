import os
import re
from collections import defaultdict
from re import finditer

import gensim
import pandas as pd
import seaborn as sns
from gensim import models
from gensim.parsing.preprocessing import STOPWORDS
from matplotlib import pyplot
from sklearn.manifold import TSNE


def indent(text, spaces=4):
    spaces = ' ' * spaces
    return '\n'.join(spaces + line if line.strip() != '' else line for line in text.split('\n'))


def list_get(li, index, fallback=None):
    try:
        return li[index]
    except IndexError:
        return fallback


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_to_csv(df, path, columns=None, index=False):
    if columns is not None and len(columns) > 0:
        df.columns = columns
    df.to_csv(path, index=index)


# ------- EXTRACTION ------- #


def traverse(path, regex, callback):
    regex = re.compile(regex)
    for dirpath, dirnames, filenames in os.walk(path):
        for f_name in filter(regex.search, filenames):
            f_path = os.path.join(dirpath, f_name)
            callback(f_path)


# ------- TRAINING ------- #


def split_name(name):
    if isinstance(name, str):
        words = []

        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', name)
        no_camel = [m.group(0).lower() for m in matches]
        no_snake = []
        for word in no_camel:
            no_snake.extend(word.split("_"))
        for word in no_snake:
            if word not in STOPWORDS and word != '':
                words.append(word)
        return words


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


# ------- VISUALIZATION ------- #


def save_plot(img_name, vectors, hues, sizes):
    td_sne = TSNE(n_components=2, verbose=0, perplexity=2, n_iter=3000)
    e_space = td_sne.fit_transform(vectors)
    df_subset = pd.DataFrame()
    df_subset['x'] = e_space[:, 0]
    df_subset['y'] = e_space[:, 1]

    pyplot.figure(figsize=(9, 9), dpi=300)
    sns.scatterplot(
        x="x", y="y",
        hue=hues,
        size=sizes,
        data=df_subset,
        legend="full",
        alpha=1.0
    )
    for idx, xy in enumerate(zip(e_space[:, 0], e_space[:, 1])):
        if idx % 6 != 0:
            continue
        pyplot.annotate(hues[idx], xy=xy, xytext=(-2, 2),
                        textcoords='offset points', ha='right', va='bottom',
                        fontsize=5)

    pyplot.savefig(img_name + ".png")
