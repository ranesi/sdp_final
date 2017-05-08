import textrazor


def get_topics(text):

    textrazor.api_key = '5eca1d0b51d33cb0b68a07e05ffa32bc76beecb012f67719f2036518'

    ret = []
    data = textrazor.TextRazor(extractors=['topics'])

    try:
        resp = data.analyze(text)
        for topic in resp.topics():
            if topic.score >= 0.5:
                ret.append(topic.label)
    except textrazor.HTTPError:
        pass

    while len(ret) <= 3:
        ret.append('')

    return ret


def get_key():
    with open('key.txt', 'r') as f:
        temp = f.read()
        temp = temp.replace('\n', '')
    return temp