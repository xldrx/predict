import codecs
from collections import OrderedDict
import os
import json
import jsonpickle
import copy

__author__ = 'xl'

_datasets = None


def pre_load():
    load_datasets()
    load_dataset_keywords_dict()
    load_keywords_dict()


def make_dir(name, trim_name=True):
    dirname = os.path.dirname(name) if trim_name else name
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def save_json(data, name):
    make_dir(name)
    with open(name, "w") as fp:
        # a = jsonpickle.encode(data, unpicklable=False)
        a = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        fp.write(a)


def save_raw(data, name):
    make_dir(name)
    with codecs.open(name, "w", "utf-8") as fp:
    # with open(name, "w") as fp:
        fp.write(data)

def load_raw(name):
    with codecs.open(name, "r", "utf-8") as fp:
        data = fp.read()
    return data


def load_json(name):
    with open(name, "r") as fp:
        a = fp.read()
        return jsonpickle.decode(a)


def exist(name):
    return os.path.exists(name)


def load_datasets(use_cache=True):
    global _datasets
    if use_cache and _datasets:
        return copy.deepcopy(_datasets)
    _datasets = load_json('data/dataset.json')
    for index, dataset in enumerate(_datasets):
        dataset['index']=index
    return copy.deepcopy(_datasets)


def load_datasets_dict():
    datasets = load_datasets()
    ret = OrderedDict()
    for ds in datasets:
        ret[ds['name']] = ds

    return ret


def load_dataset(name):
    return load_datasets_dict()[name]


def get_dataset_names():
    return load_datasets_dict().keys()


def print_dataset(name):
    dataset = load_dataset(name)
    for key, value in dataset.items():
        print "%s:\n\t" % key,
        if type(value) is list:
            print ", ".join(value)
        else:
            print value
        print


_dataset_keywords = None
_keywords = None


def load_dataset_keywords_dict(name=None,use_cache=True):
    global _dataset_keywords
    if not use_cache or not _dataset_keywords:
        _dataset_keywords = load_json('data/dataset-keywords.json')

    if name:
        return copy.deepcopy(_dataset_keywords[name])
    else:
        return copy.deepcopy(_dataset_keywords)


def load_keywords_dict(use_cache=True):
    global _keywords
    if use_cache and _keywords:
        return copy.deepcopy(_keywords)
    _keywords = load_json('data/keywords.json')
    return copy.deepcopy(_keywords)


def get_unique_items(field_name):
    ret = []
    for name, dataset in load_datasets_dict().items():
        field = dataset[field_name]
        if type(field) is list:
            ret += field
        else:
            ret.append(field)

    ret = list(set(ret))
    return ret