#! /usr/bin/env python -u
# coding=utf-8
from collections import OrderedDict
import similarity
import similarity.metrics
from utils import iotools

__author__ = 'xl'

import matplotlib.pyplot as plt
import matplotlib.axis as axis


def get_similarity_new_matrix():
    options = [similarity.metrics.df_new_keywords_list, similarity.metrics.sf_simple]
    categories = similarity.get_category_dict()
    ret = OrderedDict()
    for cat1, dlist1 in categories.items():
        ret[cat1] = OrderedDict()
        for cat2, dlist2 in categories.items():
            ret[cat1][cat2] = similarity.metrics.group_group_similarity(dlist1, dlist2, *options)
    return ret


def get_similarity_new_matrix_weighted():
    options = [similarity.metrics.df_new_keywords_list_weighted, similarity.metrics.sf_weight]
    categories = similarity.get_category_dict()
    ret = OrderedDict()
    for cat1, dlist1 in categories.items():
        ret[cat1] = OrderedDict()
        for cat2, dlist2 in categories.items():
            ret[cat1][cat2] = similarity.metrics.group_group_similarity(dlist1, dlist2, *options)
    return ret


def get_similarity_old_matrix():
    options = [similarity.metrics.df_old_keywords_list, similarity.metrics.sf_simple]
    categories = similarity.get_category_dict()
    ret = OrderedDict()
    for cat1, dlist1 in categories.items():
        ret[cat1] = OrderedDict()
        for cat2, dlist2 in categories.items():
            ret[cat1][cat2] = similarity.metrics.group_group_similarity(dlist1, dlist2, *options)
    return ret


def plot(matrix, name=None):
    # plt.xkcd()
    plt.clf()
    indexes = OrderedDict([(cat, index) for index, cat in enumerate(similarity.get_category_dict())])
    size = 3000

    # fig, ax = plt.subplots()
    # ax.xaxis.set_ticks_position('top')
    # plt.tick_params(top=True, bottom=False)

    xoptions = {'rotation': -45, 'horizontalalignment': 'right', 'rotation_mode': 'anchor', 'size': 'x-small'}
    yoptions = {'rotation': -45, 'horizontalalignment': 'right', 'rotation_mode': 'anchor', 'size': 'x-small'}
    plt.xticks(range(0, len(indexes)), indexes.keys(), **xoptions)
    plt.yticks(range(0, len(indexes)), indexes.keys(), **yoptions)
    plt.gcf().axes[0].xaxis.set_ticks_position('top')
    plt.xticks(range(0, len(indexes)), indexes.keys(), **xoptions)

    for cat1 in matrix:
        mcat = max(matrix[cat1], key=lambda x: matrix[cat1][x])
        for cat2, val in matrix[cat1].items():
            color = 'g'
            if cat2 == mcat:
                color = 'r'
            if cat1 == cat2:
                color = 'b'
            plt.scatter(indexes[cat2], indexes[cat1], c=color, s=val * size, alpha=0.5)

    plt.grid(True)
    plt.subplots_adjust(left=0.20, right=0.95, top=0.80, bottom=0.05)
    # plt.show()
    plt.gcf().set_size_inches(10, 10)

    if name:
        iotools.make_dir(name)
        plt.savefig(name, dpi=300)  # save as png


def get_table():
    matrix_new = get_similarity_new_matrix_weighted()
    matrix_old = get_similarity_old_matrix()
    cats = matrix_new.keys()

    ret = {}
    ret_text = "cat, inner-new, inner-old, outer-new, outer-old\n"

    for cat1 in cats:
        ret[cat1] = {"inner-new": 0, "outer-new": 0, "inner-old": 0, "outer-old": 0}
        ret["inner-new"] = matrix_new[cat1][cat1]
        ret["inner-old"] = matrix_old[cat1][cat1]
        ret["outer-new"] = sum([matrix_new[cat1][cat2] for cat2 in cats if cat2 != cat1])/(len(cats)-1)
        ret["outer-old"] = sum([matrix_old[cat1][cat2] for cat2 in cats if cat2 != cat1])/(len(cats)-1)

        ret_text += "%s, %s, %s, %s, %s\n" % (cat1, ret["inner-new"], ret["inner-old"], ret["outer-new"], ret["outer-old"])

    iotools.save_raw(ret_text, 'output/similarity/table.xls')



if __name__ == "__main__":
    # z# plot(get_similarity_new_matrix_weighted(), 'output/similarity/new-keywords-weighted.png')
    get_table()


