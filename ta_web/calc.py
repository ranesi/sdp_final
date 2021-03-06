import re
from nltk.corpus import cmudict

STOPS = '.?!'
dictionary = cmudict.dict()


def regex(text, fltr, s):
    """
        Removes characters specified in filter argument
            https://docs.python.org/2/library/re.html
    """
    r = re.compile(fltr)
    ret = r.sub(s, text) #s = substituted character
    return ret


def analyze_string(text):
    """
        Returns number of sentences, words, syllables,
        characters, polysyllables as tuple.
    """
    stops, syllables, polysyllables, characters = 0, 0, 0, 0

    proc_text = regex(text, '[^a-zA-Z .!?]', ' ')  # spaces will be removed during split operation

    # lower, split processed text
    text_list = proc_text.lower().split()
    words = len(text_list)

    for word in text_list:
        ret_syllables = 0  # number of syllables returned
        stops += check_sentence(word)
        if not is_word(word):
            # skip misc. punctuation
            words -= 1
            stops -= 1
            continue
        temp = regex(word, '[^a-z]', '')
        if temp in dictionary:
            characters += get_characters(temp)
            syllables += get_syllables(temp)
            # if stops <= 30:
            #     # Conditional statement required for SMOG;
            #     # however, this approach fails to take into consideration the
                  # fact that SMOG ideally calculates 30 sentences of a text.
                  # To accurately determine the score, we will need to incorporate
                  # a few extra return values - smog sentences, etc.
                  # To be copacetic with smog's definition, these would be
                  # taken from the beginning, middle, and end of a text
            #     polysyllables += is_polysyllable(get_syllables(temp))
            polysyllables += is_polysyllable(get_syllables(temp))
        else:
            # ignore unrecognized words
            words -= 1

    return (stops, words, syllables, characters, polysyllables)


def get_syllables(word):
    """
        Break word into phonemes, syllables (by trailing digit,
        the count of which yields the number of syllables)
    """
    # http://stackoverflow.com/a/4103234
    try:
        temp_list = [list(y for y in x if y[-1].isdigit()) for x in dictionary[word]]
        value = len(temp_list[0])
        return value
    except KeyError:
        # cmudict is accessed by key
        return 0


def is_word(word):
    if word[0].isalpha():
        return True
    else:
        return False


def check_sentence(word):
    """Checks for a stop; used to increment stop value"""
    if word[-1] in STOPS:
        return 1
    return 0


def is_polysyllable(syllables):
    """Checks for a polysyllable; used to increment polysyllable value"""
    if syllables >= 3:
        return 1
    return 0


def get_characters(text):
    """Return # of alphabetic characters within a text"""
    count = 0
    for char in text:
        if char.isalpha():
            count += 1
    return count


def word_not_found(word):
    """
        Attempts to determine number of syllables by checking vowels
    """
    # TODO incorporate unknown word handling code
    pass
