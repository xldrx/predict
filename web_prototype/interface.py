from collections import OrderedDict
import random
from flask import Flask, render_template, redirect, request
import jsonpickle
import similarity
from similarity.metrics import get_dataset_compatibility, get_related_datasets, get_related_datasets_for_dataset
from tokens.conflicts import all_conflicts
from tokens.generate import generate_dataset_keywords_dict
from utils import iotools

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/registration")
def registration(dataset=None):
    cats = {}
    for cid, cat in enumerate(similarity.get_categories()):
        cats[cid] = cat
    return render_template('registration-form.html', cats=cats, dataset=dataset)


@app.route("/registration/<int:index>")
def registration_by_index(index):
    dataset = None
    repo = iotools.load_datasets_dict()
    if len(repo) > index >= 0:
        dataset = repo.values()[index]

    return registration(dataset)


@app.route("/get-keywords", methods=['POST'])
def get_keywords():
    dataset = {}
    for key in ['name', 'short_desc', 'long_desc']:
        dataset[key] = request.form[key]
    keywords = generate_dataset_keywords_dict(dataset)
    keywords = sorted(keywords['all'])
    return "\n".join(keywords)


@app.route("/get-similarity", methods=['POST'])
def get_similarity():
    keywords = request.form['keywords'].split('\n')
    new_style = 'old_style' not in request.form
    similarity_dict = get_dataset_compatibility(keywords, True, new_style)
    for key, val in similarity_dict.items():
        similarity_dict[key] = "%3.0f%%" % (val * 100,)
    return jsonpickle.encode(similarity_dict, False)


@app.route("/get-related-datasets", methods=['POST'])
def get_related_datasets_html():
    keywords = request.form['keywords'].split('\n')
    new_style = 'old_style' not in request.form
    related_datasets = get_related_datasets(keywords, new_style)
    datasets = []
    for name, val in related_datasets[:20]:
        row = iotools.load_dataset(name)
        row['similarity'] = "%3.0f%%" % (val * 100,)
        datasets.append(row)
    return render_template('related-datasets.html', datasets=datasets)


@app.route("/all")
def get_all_datasets():
    return render_template('all.html', datasets=iotools.load_datasets())


@app.route("/conflicts")
def get_all_conflicts():
    datasets = []
    for name, conflictList in all_conflicts().items():
        row = iotools.load_dataset(name)
        row['conflicts'] = conflictList
        datasets.append(row)
    return render_template('all.html', datasets=datasets)


@app.route("/categories")
def get_all_categories(name=None):
    categories = similarity.get_category_dict()
    return render_template('categories.html', categories=categories)


@app.route("/keywords")
def get_all_keywords():
    keywords = iotools.load_keywords_dict()
    keywords['all'] = OrderedDict([item for item in sorted(keywords['all'].items(), key=lambda x: len(x[1]))])
    dataset_ids = dict([(dataset['name'], index) for index, dataset in enumerate(iotools.load_datasets())])
    return render_template('keywords.html', keywords=keywords, dataset_ids=dataset_ids)


@app.route("/user-study")
def get_all_keywords():
    repo = iotools.load_datasets()
    dataset = random.choice(repo)
    while dataset['category']=="Address Space Allocation Data":
        dataset = random.choice(repo)

    dataset_index = repo.index(dataset)
    print dataset['category']

    related_datasets = get_related_datasets_for_dataset(dataset, True)
    related1=[]
    for data, val in related_datasets[:10]:
        data['index']=repo.index(data)
        data['similarity'] = "%3.0f%%" % (val * 100,)
        related1.append(data)

    related_datasets = get_related_datasets_for_dataset(dataset, False)
    related2=[]
    for data, val in related_datasets[:10]:
        data['index']=repo.index(data)
        data['similarity'] = "%3.0f%%" % (val * 100,)
        related2.append(data)

    return render_template('user-study.html', dataset=dataset, dataset_index=dataset_index, related1=related1, related2=related2)


@app.template_filter('newline2br')
def newline2br(s):
    s = s.replace("\r\n", "<br/>")
    s = s.replace("\n", "<br/>")
    return s.replace("\r", "<br/>")


if __name__ == '__main__':
    iotools.pre_load()
    app.run(port=31337, debug=True)
