from utils import iotools

__author__ = 'xl'


def get_categories():
    return iotools.get_unique_items('category')


def get_datasets_in_category(category_name):
    repo = iotools.load_datasets_dict()
    ret = filter(lambda x: x['category'] == category_name, repo.values())
    return ret


def get_category_dict():
    ret = {}
    for name in get_categories():
        ret[name] = get_datasets_in_category(name)
    return ret
