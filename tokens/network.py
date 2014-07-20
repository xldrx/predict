#! /usr/bin/env python -u
# coding=utf-8
from collections import OrderedDict
from math import log
from tokens.weighting import weighting_function
from utils import iotools
import networkx as nx

__author__ = 'xl'


def mylog(val):
    return log(val+1, 2)

def keyword_neighbors(keyword):
    keywords = iotools.load_keywords_dict()
    keyword_weight = weighting_function(keyword)
    related_datasets = set([x[0] for x in keywords['all'][keyword]])
    ret = {}
    for dataset in related_datasets:
        dataset_keywords = iotools.load_dataset_keywords_dict(dataset)['all']
        for keyword2 in dataset_keywords:
            ret[keyword2] = ret.get(keyword2, 0) + 1

    for keyword2, val in ret.items():
        weight = 1.0 * weighting_function(keyword2) * mylog(val) / keyword_weight / mylog(len(related_datasets))
        ret[keyword2] = weight

    return sorted(ret.items(), key=lambda x: x[1], reverse=True)


def all_keywords_neighbors():
    ret = {}
    for keyword in iotools.load_keywords_dict()['all']:
        ret[keyword] = keyword_neighbors(keyword)

    return sorted(ret.items(), key=lambda y: len([x[1] for x in y[1]]), reverse=True)


def generate_network():
    g = nx.Graph()
    matrix = all_keywords_neighbors()

    for keyword1, kwlist in matrix:
        g.add_node(keyword1, weight=weighting_function(keyword1))

        for keyword2, weight in kwlist:
            if weight > 0.30:
                g.add_edge(keyword1, keyword2, weight=weight)

    print len(g.edges())
    nx.write_gexf(g, "output/keyword-graph.gexf")


if __name__ == "__main__":
    generate_network()
    # print dict(all_keywords_neighbors())['worm']