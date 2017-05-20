import textrazor
import re


def regex_whitespace(key):
    filter = '[a-zA-Z0-9]'
    rep = ''
    re.compile(filter)
    return re.sub(rep, key)


def get_topics(text):
    # TODO: see if this can be replaced by functionality from the NLTK library
    textrazor.api_key = get_key()

    ret = []
    data = textrazor.TextRazor(extractors=['topics'])

    try:
        resp = data.analyze(text)
        x = 0
        for topic in resp.topics():
            if topic.score >= 0.5:
                ret.append(topic.label)
            if x == 2:
                break
            x += 1
    except textrazor.HTTPError:
        pass

    return ', '.join(ret)


def get_key():
    with open('key.txt', 'r') as f:
        temp = f.read()
    return regex_whitespace(temp)
