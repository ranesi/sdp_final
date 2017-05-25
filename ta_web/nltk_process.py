import matplotlib.pyplot as plt
import numpy as np
import nltk
import random
import string
import re

W_LENGTH = 5
L_WORD = 15
OCCURRENCE = 5
MEDIA_DIR = 'ta_web/media/images/'


def regex(text, fltr='[^a-zA-Z ]', s=' '):
    r = re.compile(fltr)
    return re.sub(s, text)


def generate_filename():
    ret = ''.join(
        random.SystemRandom().choice(
            string.ascii_letters + string.digits
        ) for _ in range(10))
    ret = '{0}.png'.format(ret)
    return ret


def tokenize(text):
    return nltk.word_tokenize(regex(text))


def get_frequency_distribution(tokens):
    return nltk.FreqDist(tokens)


def get_most_common(tokens, fdist):
    return sorted(w for w in set(tokens) if len(w) > W_LENGTH and fdist[w] > OCCURRENCE)


def get_longest_words(tokens):
    t = set(tokens)
    return [w for w in t if len(w) > L_WORD]


def fdist_graph(text, title):
    tokens = tokenize(text)
    fdist = get_frequency_distribution(tokens)
    dict_fdist = dict(fdist.most_common(10))
    words = [k for k in dict_fdist.keys()]
    counts = [v for v in dict_fdist.values()]

    y_pos = np.arange(len(words))

    plt.bar(y_pos, counts, align='center', alpha=0.5)
    plt.xticks(y_pos, words)
    plt.ylabel('Word instances')
    plt.title('5 most-used words in {}'.format(title))

    filename = generate_filename()

    plt.savefig(MEDIA_DIR + filename)

    return filename
