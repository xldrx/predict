__author__ = 'xl'

import nltk
from nltk.corpus import stopwords

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

# Used when tokenizing words
#sentence_re = r'''(?x)      # set flag to allow verbose regexps
#      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
#    | \w+(-\w+)*            # words with optional internal hyphens
#    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
#    | \.\.\.                # ellipsis
#    | [][.,;"'?():-_`]      # these are separate tokens
#'''

text = """The dataset consists of the locations of landing points, the capacity of the cables, dates of construction and expansion, and a log of known outages."""

#Taken from Su Nam Kim Paper...
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)

#toks = nltk.regexp_tokenize(text, sentence_re)
toks = nltk.word_tokenize(text)
postoks = nltk.tag.pos_tag(toks)

print postoks

tree = chunker.parse(postoks)


stopwords = stopwords.words('english')


def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter=lambda t: t.node == 'NP'):
        yield subtree.leaves()


def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    #word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word


def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
    and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [normalise(w) for w, t in leaf if acceptable_word(w)]
        yield term




terms = get_terms(tree)
for term in terms:
    for word in term:
        print word