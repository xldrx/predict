#! /usr/bin/env python -u
# coding=utf-8
import json
from filtering import google
from ontology import capec
import tokens.generate
import tokens.network
from utils import iotools

__author__ = 'xl'


def get_headword(keyword):
    return tokens.generate.analyse_name(keyword)


def get_stopword(keyword):
    ret = [tokens.generate.is_stopword(word) for word in get_headword(keyword)]
    if all(ret):
        return "Yes"
    elif any(ret):
        return "Partially"
    else:
        return "No"


def get_google_ranking(keyword):
    return google.get_matrix(keyword)


def get_sans(keyword):
    with open("./data/raw/sans.json", "r") as fp:
        sans_db = json.load(fp)

    ret = []
    for record in sans_db:
        if keyword.lower() in record["name"].lower():
            ret.append(record)

    return ret


def get_symantec(keyword):
    with open("./data/raw/terms.json", "r") as fp:
        kb = json.load(fp)

    ret = []
    for record in kb:
        if keyword.lower() in record["name"].lower():
            ret.append(record)

    return ret


def get_symantec_head(keyword):
    return list(set([record["types"] for record in get_symantec(keyword)]))


def get_predict_keyword(keyword):
    ret = []
    for word in get_headword(keyword):
        print word
        if word in iotools.load_keywords_dict()['all']:
            ret += tokens.network.keyword_neighbors(word)
    return sorted(ret, key=lambda x: x[1], reverse=True)


def get_capec(keyword):
    kb = capec.get_kb()
    ret = []
    for record in kb["attacks"].values():
        if keyword.lower() in record["Name"].lower():
            ret.append(record)

    return ret


def get_capec_head(keyword):
    ret = []
    for record in get_capec(keyword):
        ret += record["Categories"]
        ret += record["Purposes"]

    return list(set(ret))


if __name__ == "__main__":
    print get_capec_head("sql")