import re
import os
import sys

from typing import Tuple, List

# Submit just this file, no zip, no additional files
# -------------------------------------------------

# Students:
#     - Ghebache SAMY
#      - HAMROUNE Boualem

"""QUESTIONS/ANSWERS

----------------------------------------------------------
Q1: What are the problem(s) with normalization in our case (Algerian tweets)?

A: It's a non structured dialect, we can change the meaning easily,
non-standard spellings, dialectal variations and the problem of abbreviations + using  brief words without vowels + using numbers to replace some arabic letters (5:خ)

Q2: Why word similarity is based on edit distance and not vectorization such as TF?

A2:
because we are interested in finding the difference between two strings and
edit distance captures differences between strings, suitable for handling spelling variations, unlike TF, which may not account for word form differences.
Q3: Why tweets similarity is proposed as such?
    (not another formula such as the sum of similarity of the first tweet's words with the second's divided by max length)

A3: The tweets similarity formula apply the same idea of attention
for each w1 in T1, we calculate the max similarity with all w2 in T2 and vice-versa
So we try to include all the similarities of each word for each tweets,
that's why we will include all the best similarities and those the final similarity
will be more accurate then the sum of similarity of the first tweet's words with the second's divided by max length
bcs it included all the similarities of w1 with w2 in T2 and vice-versa

Q4: Why blanks are being duplicated before using regular expressions in our case?

A4:

because blanks are included in the regex detection, so if you we don't add them in the regex
we can overwrite other characters like this example :
re.sub(r'(^|\s)@[\w_]+($|\s)', '[USER]','@gladiato2 @rafikh459 @jouuumii' )
if we don't duplicate the spaces, we will get this result [USER]@rafikh459[USER]
bcs when we subtitute, we will start with @ character and not \s character
that's why it's we have to double the spaces.
"""


# TODO Complete words similarity function
def word_sim(w1:str, w2:str) -> float:
    """Calculates Levenstein-based similarity between two words.
    The function's words are interchangeable; i.e. levenstein(w1, w2) = levenstein(w2, w1)

    Args:
        w1 (str): First word.
        w2 (str): Second word.

    Returns:
        float: similarity.
    """

    if len(w1) * len(w2) == 0:
        return 0.0 # If one of them is empty then the distance is the length of the other

    D = []
    D.append([i for i in range(len(w2) + 1)])
    for i in range(len(w1)):
        l = [i+1]
        for j in range(len(w2)):
            s = D[i][j] + (0 if w1[i] == w2[j] else 1)
            m = min([s, D[i][j+1] + 1, l[j] + 1])
            l.append(m)
        D.append(l)
    res = max(len(w1),len(w2))

    return (res - D[-1][-1])/res

TASHKIIL	= [u'ِ', u'ُ', u'َ', u'ْ']
TANWIIN		= [u'ٍ', u'ٌ', u'ً']
OTHER       = [u'ـ', u'ّ']

# TODO Complete text normalization function
def normalize_text(text: str) -> str :
    """Normalize a text

    Args:
	é
        text (str): source text

    Returns:
        str: result text
    """

    result = text.replace(' ', '  ') # duplicate the space
    result = re.sub('['+''.join(TASHKIIL+TANWIIN+OTHER)+']', '', result)
    result = result.lower()

    # SPCIAL
    #we don't need to specify the $ or \s character, bcs it will stop automatically since they
    # are not \w
    result = re.sub(r'(^|\s)@[\w_]+', ' [USER] ', result)
    result = re.sub(r'(^|\s)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', ' [MAIL] ',result)
    result = re.sub(r'(^|\s)#\w+',' [HASH] ', result)
    result = re.sub(r'(^|\s)https://t.co/[A-Za-z0-9]+',' [LINK] ',result)

    # FRENCH/ENGLISH/BERBER

    result = re.sub(r'é|è|ê', 'e', result)
    result = re.sub(r'á|à|â', 'a', result)

    #result = re.sub(r's$', '', result)

    #suffixes are at the end of the sentence

    result = re.sub(r'(\w+)(s)(\s|$)', r'\1 ', result)
    result = re.sub(r'(\w+)(ir|er|ers|ement|ements|ien|iens|euse|euses|eux|ly|al|yas?|en|ing|er)($|\s)', r'\1', result)

    # Delete English suffixes
    #result = re.sub(r'(ly|al)$', '', result)
    #Included in the first #result = re.sub(r'ally$', 'al', result)

    # Delete Berber suffixes
    #result = re.sub(r'(yas|en)$', '', result)

    # Transform English contractions
    result = re.sub(r"(\w+)'s", r'\1 is', result)
    result = re.sub(r"(\w+)n't", r'\1 not', result)

    # Transform French contractions
    result = re.sub(r'(t|d|qu|l|s|j)(\')', r'\1e ', result)
    result = re.sub(r'(.+)(\')(.+)', r'\1e\3 ', result)#pour p'tit => petit
    # DZ ARABIZI
    result = re.sub('(^|\s)ma(\w+)ch($|\s)', r'\2 ', result)

    # Delete suffix k and km variations
    #result = re.sub(r'k$', '', result)
    result = re.sub(r'(ek|k|km)($|\s)', '', result)

    # Delete suffixes a, i, o, ou when the radical is two letters or more
    result = re.sub(r'(\w{2,})(ak|ik|ok|ouk)($|\s)', r'\1 ', result)
    result = re.sub(r'(\w{2,})(a|i|o|ou)($|\s)', r'\1 ', result)

    # Delete suffixes h, ha when the radical is two letters or more
    result = re.sub(r'(\w{2,})(ha?)($|\s)', r'\1 ', result)

    # ARABIC/DZ-ARABIC

    # Rule 1: Split Algerian negation
    result = re.sub(r"(?:مَا|ما|مَ|م)?(\S+)ش\b", r"مَا \g<1>", result)

    result = re.sub(r'\b[ما|م]?(ن\w{1,}?)ش\b', r'\1 ما', result)


    # Rule 2: Delete Al qualifier variants if the rest is 2 or more letters
    result = re.sub(r'(?:بَال|بل|ول|وال|فل|للّ|ال)(\S{2,})', r'\1', result)
    # Rule 3: Remove Standard Arabic plural suffixes and a borrowed suffix from French
    result = re.sub(r'(.*?)((?:ين|ون|ات|ال)\b)', r'\1', result)
    # Rule 4: Delete Arabic object pronouns if the rest is 2 letters or more
    result = re.sub(r'(\w{2,})(ني|ك|ه|ها|نا|كما|كم|كن|هما|هم|هن|وا)(\s|$)', r'\1 ', result)
    # Rule 5: Remove some other Arabic and Algerian suffixes if the rest is 2 letters or more
    result = re.sub(r'(\S{2,})((?:ا|و|ي|ة)\b)', r'\1', result)

    return re.sub(r'[./:,;?!؟…]', ' ', result)


#=============================================================================
#                         IMPLEMANTED FUNCTIONS
#=============================================================================

def get_similar_word(word:str, other_words:List[str]) -> Tuple[str, float]:
    """Get the most similar word with its similarity

    Args:
        word (str): a word
        other_words (List[str]): list of target words

    Returns:
        Tuple[str, float]: the most similar word from the target + its similarity
    """

    mx_sim = 0.
    sim_word = ''
    for oword in other_words:
        sim = word_sim(word, oword)
        if sim > mx_sim:
            mx_sim = sim
            sim_word = oword

    return sim_word, mx_sim


def tweet_sim(tweet1:List[str], tweet2:List[str]) -> float:
    """Similarity between two tweets

    Args:
        tweet1 (List[str]): tokenized tweet 1
        tweet2 (List[str]): tokenized tweet 2

    Returns:
        float: their similarity
    """
    sim = 0.
    for word in tweet1:
        sim += get_similar_word(word, tweet2)[1]

    for word in tweet2:
        sim += get_similar_word(word, tweet1)[1]

    return sim/(len(tweet1) + len(tweet2))


def get_tweets(url:str='DZtweets.txt') -> List[List[str]]:
    """Get tweets from a file, where each tweet is in a line

    Args:
        url (str, optional): the URL of tweets file. Defaults to 'DZtweets.txt'.

    Returns:
        List[List[str]]: A list of tokenized tweets
    """
    result = []
    with open(url, 'r', encoding='utf8') as f:
        for line in f:
            if len(line) > 1:
                line = normalize_text(line)
                tweet = line.split()
                result.append(tweet)
    return result


#=============================================================================
#                             TESTS
#=============================================================================

def _word_sim_test():
    tests = [
        ('amine', 'immature', 0.25),
        ('immature', 'amine', 0.25),
        ('', 'immature', 0.0),
        ('amine', '', 0.0),
        ('amine', 'amine', 1.0),
        ('amine', 'anine', 0.8),
        ('amine', 'anine', 0.8),
    ]

    for test in tests:
        sim = word_sim(test[0], test[1])
        print('-----------------------------------')
        print('similarity between ', test[0], ' and ', test[1])
        print('yours ', sim, ' must be ', test[2])


def _normalize_text_test():
    tests = [
        ('@adlenmeddi @faridalilatfr Est-il en vente a Alger?',
         ['[USER]', '[USER]', 'est-il', 'en', 'vente', 'a', 'alger']),
        ('@Abderra51844745 @officialPACCI @AfcfT @UNDP Many thanks dear friend',
         ['[USER]', '[USER]', '[USER]', '[USER]', 'many', 'than', 'dear', 'friend']),
        ('Info@shahanaquazi.com ; I love your profile.',
         ['[MAIL]', 'i', 'love', 'your', 'profile']),
        ('âme à périt éclairées fète f.a.t.i.g.u.é.é',
         ['ame', 'a', 'perit', 'eclairee', 'fete', 'f', 'a', 't', 'i', 'g', 'u', 'e', 'e']),
        ('palestiniens Manchester dangereuses dangereux écouter complètement vetements',
         ['palestin', 'manchest', 'danger', 'danger', 'ecout', 'complet', 'vet']),
        ('reading followers naturally emotional traditions notably',
         ['read', 'follow', 'natural', 'emotion', 'tradition', 'notab']),
        ('iggarzen Arnuyas',
         ['iggarz', 'arnu']),
        ("it's That's don't doesn't",
         ['it', 'is', 'that', 'is', 'do', 'not', 'does', 'not']),
        ("l'éventail s'abstenir qu'ont t'avoir j'ai D'or D'hier t'en l'aïd p'tit",
         ['le', 'eventail', 'se', 'absten', 'que', 'ont', 'te', 'av', 'je', 'ai', 'de', 'or', 'de', 'hi', "t'", 'le', 'aïd', 'petit']),
        ('mal9itch mata3rfch Bsahtek ywaf9ek ya3tik 3ndk',
         ['l9it', 'ta3rf', 'bsaht', 'ywaf9', 'ya3t', '3nd']),
        ('Khaltiha Khaltih yetfarjou fhamto mousiba wladi  Chawala khmouss',
         ['khalti', 'khalti', 'yetfarj', 'fhamt', 'mousib', 'wlad', 'chawal', 'khmous']),
        ('لَا حـــــــــــــــــــــوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَزِيزُ الْحَكِيمُ،',
         ['لا', 'حول', 'ولا', 'قوة', 'إلا', 'له', 'عزيز', 'حكيم،']),
        ('منلبسوش ميخرجش ميهمناش مايهمنيش قستيهاش فهمتش معليش',
         ['ما', 'نلبس', 'ما', 'يخرج', 'ما', 'يهم', 'ما', 'يهم', 'ما', 'قستي', 'ما', 'فهمت', 'ما', 'عل']),
        ('الطاسيلي للاحباب اللهم المورال الاتحادبات المصلحين والتنازلات الجزائري فالناس للسونترال بروفايلات والصومال',
         ['طاسيل', 'احباب', 'لهم', 'مور', 'اتحادب', 'مصلح', 'تنازل', 'جزائر', 'ناس', 'سونتر', 'بروفايل', 'صوم']),
        ('متشرفين نورمال تيميمون حلقات تركعوا عدوانية يفيقولو وعليكم بصيرته بصيرتها عملها عملهم',
         ['متشرف', 'نورم', 'تيميم', 'حلق', 'تركع', 'عدواني', 'يفيقول', 'وعل', 'بصيرت', 'بصيرت', 'عمل', 'عمل']),
        ('رايحا طحتو توحشتك تبقاو ستوري راهي رميته الزنزانة وجيبوتي',
         ['رايح', 'طحت', 'توحشت', 'تبقا', 'ستور', 'راه', 'رميت', 'زنزان', 'وجيبوت']),
    ]

    for test in tests:
        print('-----------------------------------')
        print('tweet ', test[0])
        print('your norm ', normalize_text(test[0]).split())
        print('must be', test[1])


def _tweet_sim_test():
    tweets = get_tweets() # If it cannot find the file, pass its URL as argument

    tests = [
        (1, 2, 0.45652173913043487),
        (4, 120, 0.40744680851063825),
        (5, 10, 0.3381987577639752),
        (204, 211, 0.4728021978021977),
        (15, 30, 0.48148148148148145),
        (50, 58, 0.3531746031746032),
        (100, 300, 0.5277777777777778),
    ]

    for test in tests:
        print('-----------------------------------')
        print('tweet 1', tweets[test[0]])
        print('tweet 2', tweets[test[1]])
        print('your sim ', tweet_sim(tweets[test[0]], tweets[test[1]]))
        print('must be  ', test[2])




# TODO activate one test at the time
if __name__ == '__main__':
    _word_sim_test()
    _normalize_text_test()
    _tweet_sim_test()
