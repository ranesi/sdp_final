import textrazor
import re


def regex_whitespace(key):
    """Regular expression to extract alphanumeric characters from the key file"""
    filter = '[a-zA-Z0-9]'
    rep = ''
    re.compile(filter)
    return re.sub(rep, key)


def textrazor_topics(text):
    """
    TextRazor API call to get topics.

    This is dependent on access to a TextRazor API key, the free version of which
    is severely limited in regards to daily request numbers.

    The API key itself must be stored in a file called 'key.txt', which should be
    placed into text_analysis/ta_web/
    """
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

    # NOTE: The following assumes that there will NEVER be duplicate
    # topics!
    if len(ret) >= 1:
        for item in ret:
            if not ret.index(item) == len(ret) - 1:
                ret[ret.index(item)] = item + ', '

    return ret


def get_key():
    """Get key from file (returns cleaned string
    - will not work for special characters! (unless you modify the regex)"""
    with open('key.txt', 'r') as f:
        temp = f.read()
    return regex_whitespace(temp)
