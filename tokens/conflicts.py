from collections import OrderedDict
from utils import iotools
from similarity.metrics import item_group_similarity, df_new_keywords_list, sf_simple
from similarity import get_category_dict

__author__ = 'xl'


def get_conflicts(function):
    conflict_list = []
    repo = iotools.load_datasets_dict()
    for name, dataset in repo.items():
        result, message = function(dataset)
        if not result:
            # print "%s:\n\t\t %s\n" % (name, message)
            conflict_list.append((name, message))
    return conflict_list


def anonymization_conflicts(dataset):
    anon_keyword = filter(lambda x: 'anon' in x.lower(), dataset['keywords'])
    anon = dataset['anonymization']
    if len(anon_keyword) == 0:
        return True, None

    if anon == '(none)' and ('No IP Anonymization' not in anon_keyword):
        return False, "No anonymization mentions in 'Anonymization' field, but '%s' mentions in keywords" % (
            ", ".join(anon_keyword))

    return True, None


def format_conflicts(dataset):
    formats_dict = {
        'NetFlow version 5': ['netflow'],
        'DAG': ['dag'],
        'Adjacency list': [],
        'Binary': [],
        'Text': [],
        'argus': ['argus'],
        'Syslog': ['syslog'],
        'pcap (Packet Capture library)': ['pcap'],
        'Address bitstring': [],
        'CSV (comma-separated)': ['csv'],
        'Snort': ['snort'],
    }


    text = dataset['long_desc']
    dataset_format = set(dataset['formats'])
    formats = []
    for format_name, klist in formats_dict.items():
        for keyword in klist:
            if text.lower().find(keyword) >=0:
                formats.append(format_name)
                break
    formats=set(formats)

    if dataset_format.issuperset(formats):
        return True, None

    if len(formats) > 0 and False:
        print dataset_format
        print '---'
        print formats
        print '---'
        print text
        print '---'
        print

    if len(formats-dataset_format) > 0:
        return False, "'%s' format(s) might mentions in long description, but not in formats (%s)" % (
            ", ".join(formats-dataset_format), ", ".join(dataset_format))

    return True, None


category_dict = get_category_dict()
def categories_conflicts(dataset):
    global category_dict
    current_cat = dataset['category']
    options = [df_new_keywords_list, sf_simple]
    similarity_dict = dict([
        (cat, item_group_similarity(dataset, dlist, *options))
        for cat, dlist in category_dict.items()
    ])

    max_cat = max(similarity_dict.items(), key=lambda x: x[1])

    if max_cat[0] != current_cat and len(category_dict[current_cat]) > 1:
        return False, "Dataset is more similar to '%s' category (%4.2f%%) than its own category, '%s' (%4.2f%%)" % (
            max_cat[0], max_cat[1] * 100, current_cat, similarity_dict[current_cat] * 100 )
    return True, None


def all_conflicts():
    ret = OrderedDict()
    for name, conflict in get_conflicts(anonymization_conflicts)+ get_conflicts(categories_conflicts) +\
            get_conflicts(format_conflicts):
        if name not in ret:
            ret[name]=[]
        ret[name].append(conflict)

    return ret


if __name__ == '__main__':
    print get_conflicts(format_conflicts)
    # print all_conflicts()