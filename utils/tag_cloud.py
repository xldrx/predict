from collections import Counter
from utils import iotools
from tokens.weighting import weighting_function

__author__ = 'xl'


def normalized(keyword):
    keyword = keyword.replace(' ', '~')
    return keyword


def tag_cloud_text_old_keywords():
    ret = []
    for dataset in iotools.load_datasets():
        ret += [normalized(keyword) for keyword in dataset['keywords']]
    return ret


def tag_cloud_text_new_keywords_weighted():
    ret = []
    for keyword, klist in iotools.load_keywords_dict()['all'].items():
        val = int(weighting_function(keyword)*1000)
        ret += [normalized(keyword)] * val
    return ret


def tag_cloud_text_new_keywords_simple():
    ret = []
    for dataset, keywords in iotools.load_dataset_keywords_dict().items():
        ret += keywords['all'].keys()
    return ret


def remove_tops(keyword_list, percent):
    counter = Counter(keyword_list)
    counter = [word for word, count in counter.most_common()]

    remove_count = len(counter) * percent / 100.0
    remove_count = int(remove_count)
    keyword_list = filter(lambda x: x not in counter[:remove_count], keyword_list)

    return keyword_list


if __name__ == "__main__":
    keywords_sets = {
        'Old Keywords': tag_cloud_text_old_keywords(),
        'New Keywords': tag_cloud_text_new_keywords_simple(),
        'New Keywords Weighted': tag_cloud_text_new_keywords_weighted(),
    }

    for key, keywords in keywords_sets.items():
        keywords_sets[key + " (Exclude top 10%)"] = remove_tops(keywords, 10)

    for key, keywords in keywords_sets.items():
        iotools.save_raw("\n".join(keywords), 'output/tagcloud/%s.txt' % key)
