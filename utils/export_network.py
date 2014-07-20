#! /usr/bin/env python -u
# coding=utf-8
from collections import OrderedDict
import similarity.metrics

from utils import iotools
__author__ = 'xl'
import networkx as nx


def get_similarity_new_matrix():
    options = [similarity.metrics.df_new_keywords_list, similarity.metrics.sf_simple]
    datasets = iotools.load_datasets_dict()
    ret = OrderedDict()
    for name1, dataset1 in datasets.items():
        ret[name1] = OrderedDict()
        for name2, dataset2 in datasets.items():
            ret[name1][name2] = similarity.metrics.item_item_similarity(dataset1, dataset2, *options)
    return ret


def get_similarity_new_matrix_weighted():
    options = [similarity.metrics.df_new_keywords_list_weighted, similarity.metrics.sf_weight]
    datasets = iotools.load_datasets_dict()
    ret = OrderedDict()
    for name1, dataset1 in datasets.items():
        ret[name1] = OrderedDict()
        for name2, dataset2 in datasets.items():
            ret[name1][name2] = similarity.metrics.item_item_similarity(dataset1, dataset2, *options)
    return ret


def generate_network(file_name, matrix):
    g = nx.Graph()
    datasets = iotools.load_datasets_dict()

    for name, dataset in datasets.items():
        info = {
            "category": dataset['category'],
            "subcategory": dataset['subcategory'],
        }
        g.add_node(name, info)

    for name1 in matrix:
        for name2 in matrix[name1]:
            weight = matrix[name1][name2]
            if weight > 0.25:
                g.add_edge(name1, name2, weight=weight)

    print len(g.edges())
    nx.write_gexf(g, file_name)


if __name__ == "__main__":
    generate_network("output/graph.gexf", get_similarity_new_matrix())
    generate_network("output/graph-weighted.gexf", get_similarity_new_matrix_weighted())

