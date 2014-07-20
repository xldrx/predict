import codecs
import json

__author__ = 'xl'

import nltk
from nltk.corpus import stopwords, wordnet


lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.LancasterStemmer()
stopwords = stopwords.words('english')


def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = lemmatizer.lemmatize(word, 'v')
    word = lemmatizer.lemmatize(word)
    word = stemmer.stem(word)
    return word


def check_word(word, wtype):
    if word.lower() in stopwords:
        print word
        return False

    if 2 > len(word):
        return False

    if wtype[0] != "N" and wtype[0] != "V":
        return False

    return True


def nouns(text):
    sentences = nltk.sent_tokenize(text)
    postoks = []
    for sen in sentences:
        tokens = nltk.word_tokenize(sen)
        postoks += nltk.tag.pos_tag(tokens)

    #print postoks
    return [word for word, wtype in postoks if check_word(word, wtype)]


def update_dataset():
    wordset = set()
    with open('./dataset-fixed.json', 'r') as fp:
        rows = json.load(fp)
    for row in rows:
        string = "\n".join([row['name'], row['long_desc'], row['short_desc']])
        words = nouns(string)
        wordset = wordset.union(set(words))
        row['words'] = words
        print "%s:\n\t\t%s\n\t\t%s\n\t\t%s\n" % (
            row['name'], " : ".join(words), " : ".join(row['keywords']), row["formats"])
    with open('./dataset-words.json', 'w') as fp:
       json.dump(rows, fp)

    with open('./words.json', 'w') as fp:
       json.dump(list(wordset), fp)

    print "\n\n\n%s" % len(wordset)


def load_words():
    with open('./words.json') as fp:
        words = json.load(fp)

    wlist = map(normalise, words)
    wlist = map(unicode, wlist)
    wlist = map(unicode.lower, wlist)
    wlist = list(set(wlist))
    wlist = sorted(wlist)

    print len(wlist)

    for word in wlist:
        lex = wordnet.synsets(word)[0].lexname if len(wordnet.synsets(word)) > 0 else ""
        print "%s:\t%s" % (word, lex)


def load_dswords():
    with open('./dataset-words.json') as fp:
        ds = json.load(fp)

    wordList = []
    wordSet = []
    keywordList = []
    keywordSet = []

    for row in ds:
        words = row["words"]
        wlist = map(normalise, words)
        wlist = map(unicode, wlist)
        wlist = map(unicode.lower, wlist)
        wlist = list(set(wlist))
        wlist = sorted(wlist)

        wordList.append(wlist)
        wordSet += wlist
        keywordList.append(row['keywords'])
        keywordSet += row['keywords']
        row['words-fixed'] = wlist

    return ds

    wordSet = list(sorted(set(wordSet)))
    keywordSet = list(sorted(set(keywordSet)))

    print len(wordSet), len(keywordSet)
    print sum([len(w) for w in wordList]) / 1.0 / len(ds), sum([len(w) for w in keywordList]) / 1.0 / len(ds)
    print sum([len(w) for w in wordList]), sum([len(w) for w in keywordList])


def distance(w1, w2):
    w1 = set(w1)
    w2 = set(w2)
    shared = w1.intersection(w2)
    diff = w1.difference(w2)
    diff = diff.union(w2.difference(w1))

    return 2.0 * len(shared) / (len(w1) + len(w2)), 1.0 * len(diff) / (len(w1) + len(w2))


def generate_network():
    ds = load_dswords()
    with open("nodes.csv", "w") as fp:
        fp.write("id\tName\tCategory\n")
        for i1, d1 in enumerate(ds):
            fp.write("%s\t%s\t%s\n" % (i1, d1['name'], d1['category']))
    with open("graph.csv", "w") as fp:
        fp.write("Source\tTarget\tNew-Sim\tNew-Diff\tOld-Sim\tOld-Diff\n")
        for i1, d1 in enumerate(ds):
            for i2, d2 in enumerate(ds):
                new_dist = distance(d1['words-fixed'], d2['words-fixed'])
                old_dist = distance(d1['keywords'], d2['keywords'])
                fp.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (i1, i2, new_dist[0], new_dist[1], old_dist[0], old_dist[1]))


def get_word_freq():
    with open('./dataset-words.json') as fp:
        ds = json.load(fp)

    words = {}

    for row in ds:
        for word in row["words"]:
            token = normalise(word)
            token = unicode(token)
            token = unicode.lower(token)
            words[token] = words.get(token, list())
            words[token].append(word)

    word_freq = [(token, len(words[token])) for token in words]
    word_freq = sorted(word_freq, cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)

    return words, word_freq

def save_tag_cloud():
    ds = load_dswords()
    words = {'words-fixed': [], 'keywords': []}
    for d in ds:
        for key in words:
            words[key]+= d[key]

    for key, wset in words.items():
        out_str = '\n'.join([unicode(w.replace(' ', '~')) for w in wset])
        out_str = out_str.encode('utf-8','ignore')
        with codecs.open('tagcloud-%s.txt' % key, 'w') as fp:
            fp.write(out_str)

if __name__ == '__main__':
    #update_dataset()
    save_tag_cloud()
    #words, word_freq = get_word_freq()
    ##for i in range(20):
    ##    key, count = word_freq[i]
    ##    print key, count
    ##    print set(words[key])
    ##    print
    #
    #print "\n".join(["%s\t%s" % freq for freq in word_freq])


