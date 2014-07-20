import similarity
from similarity.functions import *

__author__ = 'xl'


def group_group_similarity(group1, group2, data_function, similarity_function):
    ret = 0
    count = 0
    for dataset in group1:
        ret += item_group_similarity(dataset, group2, data_function, similarity_function)
        count += 1
    return 1.0 * ret / count if count > 0 else 0


def item_group_similarity(dataset, group, data_function, similarity_function):
    ret = 0
    count = 0
    data1 = data_function(dataset)
    for dataset2 in group:
        if dataset == dataset2:
            continue
        data2 = data_function(dataset2)
        ret += similarity_function(data1, data2)
        count += 1
    return 1.0 * ret / count if count > 0 else 0


def item_item_similarity(dataset1, dataset2, data_function, similarity_function):
    data1 = data_function(dataset1)
    data2 = data_function(dataset2)
    ret = similarity_function(data1, data2)
    return ret


def group_similarity(group1, group2, compare_function, data_function, similarity_function):
    ret = None
    for dataset1 in group1:
        data1 = data_function(dataset1)
        for dataset2 in group2:
            if dataset1 == dataset2:
                continue
            data2 = data_function(dataset2)
            if ret:
                ret = compare_function(similarity_function(data1, data2), ret)
            else:
                ret = similarity_function(data1, data2)
    return ret if ret else 0


def similarity_list_groups():
    category_dict = similarity.get_category_dict()
    for name1, dlist1 in category_dict.items():
        for name2, dlist2 in category_dict.items():
            group_similarity2 = group_group_similarity(dlist1, dlist2, df_old_keywords_list,
                                                       sf_simple)
            group_similarity = group_group_similarity(dlist1, dlist2, df_new_keywords_list,
                                                      sf_simple)
            if name1 == name2:
                print "%s\t%s\n\t\t%s\t(old: %%%4.2f new: %%%4.2f)" % (
                    name1, name2, len(dlist1), group_similarity2 * 100, group_similarity * 100)


def similarity_items():
    option_dict = {"new": [df_new_keywords_list, sf_simple], "old": [df_old_keywords_list, sf_simple]}
    category_dict = similarity.get_category_dict()
    error = {}
    for key, options in option_dict.items():
        error[key] = []
        for name, dataset in iotools.load_datasets_dict().items():
            cat = dataset['category']
            self_sim = item_group_similarity(dataset, category_dict[cat], *options)
            out_sim, cat2 = max(
                [(item_group_similarity(dataset, dlist, *options), cat2) for cat2, dlist in
                 category_dict.items() if cat2 != cat], key=lambda x: x[0])

            if self_sim < out_sim:
                error[key].append(name)
                print "%s\t\t(%s)\n\t\tself: %%%4.2f out: %%%4.2f\t\t(%s)\n" % (name, cat, self_sim, out_sim, cat2)
    shared = len(set(error['new']).intersection(set(error['old'])))
    distinct = len(error['new']) + len(error['old']) - shared
    print shared, distinct


def minmax_similarity_items():
    option_dict = {"new": [df_new_keywords_list, sf_simple], "old": [df_old_keywords_list, sf_simple]}
    category_dict = similarity.get_category_dict()
    for key, options in option_dict.items():
        print key
        print
        print
        for name1, dlist1 in category_dict.items():
            for name2, dlist2 in category_dict.items():
                max_val = group_similarity(dlist1, dlist2, max, *options)
                min_val = group_similarity(dlist1, dlist2, min, *options)
                if name1 == name2:
                    print "%s\t%s" % (len(dlist1), len(dlist2))
                    print "%s\t%s\n\t\min: %%%4.2f max: %%%4.2f\n" % (name1, name2, min_val, max_val)


def get_dataset_compatibility(keyword_list, use_numbering_for_key=False, new_keywords = True):
    options = [df_simple_list, sf_simple]
    category_dict = similarity.get_category_dict()
    similarity_dict = {}
    for name, dlist in category_dict.items():
        if new_keywords:
            dlist_keywords = [iotools.load_dataset_keywords_dict(dataset['name'])['all'] for dataset in dlist]
        else:
            dlist_keywords = [dataset['keywords'] for dataset in dlist]
        similarity_value = item_group_similarity(keyword_list, dlist_keywords, *options)
        similarity_dict[name] = similarity_value

    if use_numbering_for_key:
        ret = {}
        for cid, cat in enumerate(similarity.get_categories()):
            ret[cid] = similarity_dict[cat]
        return ret
    else:
        return similarity_dict


def get_related_datasets(keyword_list, new_keywords = True):
    options = [df_simple_list, sf_simple]
    dataset_dict = iotools.load_datasets_dict()
    similarity_list = []
    for name, dataset in dataset_dict.items():
        if new_keywords:
            dkeywords = iotools.load_dataset_keywords_dict(name)['all']
        else:
            dkeywords = dataset['keywords']
        similarity_value = item_item_similarity(keyword_list, dkeywords, *options)
        similarity_list.append((name, similarity_value))
    similarity_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)
    return similarity_list


def get_related_datasets_for_dataset(dataset, new_keywords = True):
    options = [[df_new_keywords_list, sf_simple],[df_old_keywords_list, sf_simple]]
    dataset_dict = iotools.load_datasets_dict()
    similarity_list = []
    for name, dataset2 in dataset_dict.items():
        if dataset == dataset2:
            continue
        if new_keywords:
            similarity_value = item_item_similarity(dataset, dataset2, *options[0])
        else:
            similarity_value = item_item_similarity(dataset, dataset2, *options[1])

        similarity_list.append((dataset2, similarity_value))
    similarity_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)
    return similarity_list


if __name__ == '__main__':
#similarity_list_groups()
#    similarity_items()
    minmax_similarity_items()


