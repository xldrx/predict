from utils import iotools
from tokens.weighting import weighting_function

__author__ = 'xl'


def sf_simple(keyword_list1, keyword_list2):
    shared_keyword = len(set(keyword_list1).intersection(keyword_list2))
    all_keywords = len(set(keyword_list1).union(keyword_list2))
    similarity = 1.0 * shared_keyword / all_keywords
    return similarity


def sf_weight(keyword_list1, keyword_list2):
    shared_keyword = set(keyword_list1).intersection(keyword_list2)
    all_keywords = set(keyword_list1).union(keyword_list2)

    shared_keyword_val = sum([keyword_list1[keyword] for keyword in shared_keyword])
    all_keywords_val = sum(
        [keyword_list1[keyword] if keyword in keyword_list1 else keyword_list2[keyword] for keyword in all_keywords])

    similarity = 1.0 * shared_keyword_val / all_keywords_val
    return similarity


def sf_multiple_keyword_set(keyword_dict1, keyword_dict2):
    similarity = 0
    count = 0
    for key in keyword_dict1:
        if key in keyword_dict2:
            count += 1
            similarity += sf_simple(keyword_dict1[key], keyword_dict2[key])

    similarity = 1.0 * similarity / count
    return similarity


def df_old_keywords_list(dataset):
    return dataset['keywords']


def df_new_keywords_list(dataset):
    name = dataset['name']
    return iotools.load_dataset_keywords_dict(name)['all']


def df_new_keywords_list_weighted(dataset):
    name = dataset['name']
    keywords = iotools.load_dataset_keywords_dict(name)['all'].keys()
    weights = [weighting_function(keyword) for keyword in keywords]
    return dict(zip(keywords, weights))


def df_simple_list(keyword_list):
    return keyword_list

