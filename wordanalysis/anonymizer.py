#! /usr/bin/env python -u
# coding=utf-8
import json

__author__ = 'xl'

cats = []
words = []

with open('./dataset-words.json', 'r') as fp:
    rows = json.load(fp)

for row in rows:
    cats.append(row['subcategory'])

    words+=row['words']

catdic = dict([(cat, id) for id,cat in enumerate(set(cats))])
wordsdic = dict([(word, id) for id,word in enumerate(set(words))])

ret = []
for id,row in enumerate(rows):
    dataset = {'id': id}
    dataset['category'] = 'cat%02d' % catdic[row['subcategory']]
    dataset['features'] = ['f%04d' % wordsdic[word] for word in row['words']]
    ret.append(dataset)

with open('./dataset-anonymized.json', 'w') as fp:
    json.dump(ret, fp)

print ret[200]
for row in rows:
    print row
    break


