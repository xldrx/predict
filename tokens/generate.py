from collections import OrderedDict
import nltk
from nltk.corpus import stopwords
from utils import iotools

__author__ = 'xl'

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.LancasterStemmer()


def setup_stopwords():
    global stopwords
    stopwords = stopwords.words('english')
setup_stopwords()


def setup_commonwords():
    global commonwords
    with open('data/common-words.txt') as fp:
        commonwords = fp.read().split("\n")
setup_commonwords()


def get_head_word(word, word_type):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.strip()
    word1 = word
    if word.endswith("'s"):
        word = word[:-2]

    if word.endswith("s") and word[-2].isupper():
        word = word[:-1]

    if word.endswith("."):
        word = word[:-1]

    if word[0].isupper() and word[-1].isupper():
        return word

    word = word.lower()
    if word_type[0] == "V":
        word = lemmatizer.lemmatize(word, 'v')
    else:
        word = lemmatizer.lemmatize(word, 'v')
        word = lemmatizer.lemmatize(word)
        #word = stemmer.stem(word)
    return word


def check_word_description(word, wtype):
    if not check_word_name(word, wtype):
        return False

    if wtype[0] != "N" and wtype[0] != "V":
        return False

    return True


def check_word_name(word, wtype):
    word = word.strip()

    if 2 > len(word):
        return False

    if word.endswith("'s"):
        word = word[:-2]

    if word.endswith("s") and word[-2].isupper():
        word = word[:-1]

    if word.endswith("."):
        word = word[:-1]

    if 2 > len(word):
        return False

    if word.lower() in stopwords:
        return False

    if word.lower() in commonwords:
        return False

    if get_head_word(word, "Other") in commonwords:
        return False

    if not any(c.isalpha() for c in word):
        return False

    return True


def analyse_description(text):
    text = text.replace('/', ', ')

    sentences = nltk.sent_tokenize(text)
    postoks = []
    for sen in sentences:
        tokens = nltk.word_tokenize(sen)
        postoks += nltk.tag.pos_tag(tokens)

    ret = OrderedDict()
    for word, wtype in postoks:
        if not check_word_description(word, wtype):
            continue
        head_word = get_head_word(word, wtype)
        ret[head_word] = ret.get(head_word, [])
        ret[head_word].append(word)
    return ret


def analyse_name(text):
    text = text.replace('_', ' ')
    text = text.replace('-', ' ')
    tokens = nltk.word_tokenize(text)
    postoks = nltk.tag.pos_tag(tokens)

    ret = OrderedDict()
    for word, wtype in postoks:
        if not check_word_name(word, wtype):
            continue
        head_word = get_head_word(word, wtype)
        ret[head_word] = ret.get(head_word, [])
        ret[head_word].append(word)
    return ret


def generate_dataset_keywords_dict(dataset):
    keywords = OrderedDict()
    keywords['long_desc'] = analyse_description(dataset['long_desc'])
    keywords['short_desc'] = analyse_description(dataset['short_desc'])
    keywords['name'] = analyse_name(dataset['name'])

    keywords['all'] = OrderedDict()
    for key in ['long_desc', 'short_desc', 'name']:
        for keyword in keywords[key]:
            if keyword not in keywords['all']:
                keywords['all'][keyword] = []
            keywords['all'][keyword] += keywords[key][keyword]

    return keywords


def generate_all_dataset_keywords_dict():
    ret = OrderedDict()
    for dataset_name, dataset in iotools.load_datasets_dict().items():
        ret[dataset_name] = generate_dataset_keywords_dict(dataset)
    return ret


def generate_keywords_dict():
    ret = OrderedDict()
    for key in ['long_desc', 'short_desc', 'name', 'all']:
        ret[key] = OrderedDict()

    for dataset_name, dataset in iotools.load_datasets_dict().items():
        keywords = generate_dataset_keywords_dict(dataset)
        for key in ['long_desc', 'short_desc', 'name', 'all']:
            for keyword in keywords[key]:
                if keyword not in ret[key]:
                    ret[key][keyword] = []
                ret[key][keyword] += zip(len(keywords[key][keyword])*[dataset_name], keywords[key][keyword])

    for key, keywords in ret.items():
        ret[key] = OrderedDict(sorted(keywords.items(), key=lambda x: x[0].lower(), reverse=False))
    return ret


def save_keywords():
    iotools.save_json(generate_keywords_dict(), 'data/keywords.json')
    iotools.save_json(generate_all_dataset_keywords_dict(), 'data/dataset-keywords.json')


if __name__ == '__main__':
    save_keywords()
    print len(generate_keywords_dict()['all'])
