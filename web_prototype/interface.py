from collections import OrderedDict
import random
from flask import Flask, render_template, redirect, request
import jsonpickle
from filtering import process_keyword
import similarity
from similarity.metrics import get_dataset_compatibility, get_related_datasets, get_related_datasets_for_dataset
from tokens.conflicts import all_conflicts
from tokens.generate import generate_dataset_keywords_dict
from utils import iotools
import json

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


@app.route("/view-dataset/<int:index>")
def view_by_index(index):
    dataset = None
    repo = iotools.load_datasets_dict()
    if len(repo) > index >= 0:
        dataset = repo.values()[index]

    cats = {}
    for cid, cat in enumerate(similarity.get_categories()):
        cats[cid] = cat
    return render_template('view-dataset.html', cats=cats, dataset=dataset)


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


@app.route("/conflicts")
def get_all_conflicts():
    datasets = {}
    for name, conflictList in all_conflicts().items():
        row = iotools.load_dataset(name)
        row['conflicts'] = conflictList
        category = row['category']
        if category not in datasets:
            datasets[category] = []
        datasets[category].append(row)

    return render_template('all-datasets.html', dataset_dict=datasets)


@app.route("/all-datasets")
def get_all_datasets():
    categories = similarity.get_category_dict()
    return render_template('all-datasets.html', dataset_dict=categories)


@app.route("/dataset-keywords")
def get_all_datasets_with_keywords():
    categories = similarity.get_category_dict()
    keywords = iotools.load_dataset_keywords_dict()
    return render_template('datasets-with-keywords.html', dataset_dict=categories, keywords=keywords)


@app.route("/keywords")
def get_all_keywords():
    keywords = iotools.load_keywords_dict()
    keywords['all'] = OrderedDict(
        [item for item in sorted(keywords['all'].items(), key=lambda x: len(x[1]), reverse=False)])
    for key in keywords['all']:
        keywords['all'][key] = list(set([dataset for dataset, _ in keywords['all'][key]]))
    dataset_ids = dict([(dataset['name'], index) for index, dataset in enumerate(iotools.load_datasets())])
    return render_template('dataset-keywords.html', keywords=keywords, dataset_ids=dataset_ids)


@app.route("/search")
def search():
    return "TODO"  #TODO


@app.route("/keyword-discovery", methods=["GET", "POST"])
def discovery():
    keywords = list(iotools.load_keywords_dict()['all'].keys())

    if 'keyword' in request.form:
        keyword = request.form.get('keyword', None)
    elif 'keyword' in request.args:
        keyword = request.args.get('keyword', None)
    else:
        keyword = None

    result = {}

    if keyword:
        result["stopword"] = process_keyword.get_stopword(keyword)
        result["headword"] = process_keyword.get_headword(keyword)
        result["sans"] = process_keyword.get_sans(keyword)
        result["sans_head"] = process_keyword.get_sans_head(keyword)
        result["symantec"] = process_keyword.get_symantec(keyword)
        result["symantec_head"] = process_keyword.get_symantec_head(keyword)
        result["predict"] = process_keyword.get_predict_keyword(keyword)
        result["capec"] = process_keyword.get_capec(keyword)
        result["capec_head"] = process_keyword.get_capec_head(keyword)

    return render_template("keyword-search.html", suggestions=keywords, keyword=keyword, result=result)


@app.route("/text-processing", methods=["GET", "POST"])
def text_processing():
    title = request.form.get('d_title', None)
    body = request.form.get('d_body', None)

    keywords = None
    categories = None
    datasets = None
    dataset_ids = dict([(dataset['name'], index) for index, dataset in enumerate(iotools.load_datasets())])

    if title or body:
        keywords = generate_dataset_keywords_dict({"name": title, "long_desc": body, "short_desc": ""})
        keywords = sorted(keywords['all'])

        similarity_dict = get_dataset_compatibility(keywords)
        categories = []
        for key, val in sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True):
            if val > 0:
                row = {
                    "name": key,
                    "similarity": "%4.1f%%" % (val * 100,)
                }
                categories.append(row)

        related_datasets = get_related_datasets(keywords)
        datasets = []
        for name, val in sorted(related_datasets[:20], key=lambda x: x[1], reverse=True):
            if val == 0:
                continue
            row = iotools.load_dataset(name)
            row['similarity'] = "%4.1f%%" % (val * 100,)
            datasets.append(row)

    return render_template("text_processing.html", d_title=title, d_body=body, keywords=keywords,
                           categories=categories, related_datasets=datasets, dataset_ids=dataset_ids)


@app.route("/keyword-discovery-online", methods=["POST"])
def get_online_report():
    keyword = request.form.get('keyword', None)

    data = []
    for key, freq in process_keyword.get_google_ranking(keyword).items():
        data.append({"Name": key, "Frequency": freq})

    print data
    return json.dumps(data)


@app.route("/user-study")
def user_study():
    repo = iotools.load_datasets()
    dataset = random.choice(repo)
    while dataset['category'] == "Address Space Allocation Data":
        dataset = random.choice(repo)

    dataset_index = repo.index(dataset)
    print dataset['category']

    related_datasets = get_related_datasets_for_dataset(dataset, True)
    related1 = []
    for data, val in related_datasets[:10]:
        data['index'] = repo.index(data)
        data['similarity'] = "%3.0f%%" % (val * 100,)
        related1.append(data)

    related_datasets = get_related_datasets_for_dataset(dataset, False)
    related2 = []
    for data, val in related_datasets[:10]:
        data['index'] = repo.index(data)
        data['similarity'] = "%3.0f%%" % (val * 100,)
        related2.append(data)

    return render_template('user-study.html', dataset=dataset, dataset_index=dataset_index, related1=related1,
                           related2=related2)


@app.template_filter('newline2br')
def newline2br(s):
    s = s.replace("\r\n", "<br/>")
    s = s.replace("\n", "<br/>")
    return s.replace("\r", "<br/>")


if __name__ == '__main__':
    iotools.pre_load()
    app.run(port=31337, debug=True)
