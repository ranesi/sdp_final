import math


ERROR = -1
PRECISION = 2


def fk_re(words, sentences, syllables):
    '''Calculate Flesch Reading Ease'''
    try:
        read_level = (206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words)))
        return round(read_level, PRECISION)
    except:
        return ERROR


def fk_gl(words, sentences, syllables):
    '''Calculate Flesch-Kincaid Grade Level'''
    try:
        grade_level = ((0.39 * (words / sentences)) + (11.8 * (syllables / words)) - 15.59)
        return round(grade_level, PRECISION)
    except:
        return ERROR


def ari(words, sentences, characters):
    '''Calculate ARI score'''
    try:
        ari_level = (4.71 * (characters / words) + (0.5 * (words / sentences))) - 21.43
        return math.ceil(ari_level)
    except ZeroDivisionError:
        return ERROR

#TODO modify the smog equation to operate without using a table
# def smog(sentences, polysyllables):
#     '''Calculate SMOG level'''
#     try:
#         smog_level = math.sqrt((polysyllables * (30 / sentences)) * ((1.0430**2) + 3.1291))
#         return round(smog_level, precision)
#     except ZeroDivisionError:
#         return ERROR

def smog(poly):
    '''
        Alternative SMOG calculation table.
        Source:
            <http://www.hunter.cuny.edu/irb/education-training/smog-readability-formula>
    '''
    gl = 0
    #x <= poly <= y: x,y = lower and upper polysyllabic limitation
    #for a grade level
    if 0 <= poly <= 6:
        gl = 5
    elif 7 <= poly <= 12:
        gl = 6
    elif 13 <= poly <= 20:
        gl = 7
    elif 21 <= poly <= 30:
        gl = 8
    elif 31 <= poly <= 40:
        gl = 9
    elif 43 <= poly <= 56:
        gl = 10
    elif 57 <= poly <= 72:
        gl = 11
    elif 73 <= poly <= 90:
        gl = 12
    elif 91 <= poly <= 110:
        gl = 13
    elif 111 <= poly <= 132:
        gl = 14
    elif 133 <= poly <= 156:
        gl = 16
    elif 157 <= poly <= 182:
        gl = 17
    else:
        gl = 18
    return gl
