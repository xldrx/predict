#! /usr/bin/env python -u
# coding=utf-8
from math import log
from utils import iotools

__author__ = 'xl'


keywords = iotools.load_keywords_dict()
def weighting_function(keyword):
    global keywords
    keyword_freq = log(len(keywords['all'][keyword])+1, 2)
    weigth = 1/keyword_freq if keyword_freq > 0 else 0
    return weigth


def weight_keywords(keyword_list):
    ret = []
    for keyword in keyword_list:
        ret.append((keyword, weighting_function(keyword)))

    return sorted(ret, key=lambda x: x[1], reverse=False)


def dataset_weighting_function(dataset):
    keywords = iotools.load_dataset_keywords_dict(dataset['name'])['all']
    keywords_weight = weight_keywords(keywords)
    return sum([x[1] for x in keywords_weight])


def weight_all_datasets():
    ret = []
    repo = iotools.load_datasets_dict()
    for name, dataset in repo.items():
        ret.append((name, dataset_weighting_function(dataset)))
    return sorted(ret, key=lambda x: x[1], reverse=False)


def weight_all_keywords():
    return weight_keywords(iotools.load_keywords_dict()['all'])


if __name__ == "__main__":
    keywords_weight = weight_all_keywords()
    print "\n".join(["%s\t%s" % row for row in keywords_weight[:20]])

    print
    dataset_weight = weight_all_datasets()
    print "\n".join(["%s\t%s" % row for row in dataset_weight])
