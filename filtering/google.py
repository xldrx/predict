from collections import OrderedDict
import os
import re
from time import sleep
from math import log
import requests

__author__ = 'xl'

import json
import urllib


class Search(object):
    def __init__(self):
        self.last_url = "https://www.google.com/"
        self.session = requests.session()

    def get_number_of_results(self, searchfor):
        try:
            payload = {
                'q': searchfor,
                'hl': 'en',
                'btnG': 'Google Search',
                'inurl': 'https',
            }

            self.session.headers.update({'referer': self.last_url})

            r = self.session.get("https://www.google.com/search", params=payload)
            self.last_url = r.url
            # print self.session.cookies
            # print r.url
            if r.text.find("did not match any documents.") >= 0:
                return 0
            result = re.search("([\d,]*?) results?</div>", r.text).group(1)
            return int(result.replace(",", ""))
        except Exception as ex:
            try:
                if r:
                    print r.url
                    print r.text
            finally:
                raise ex


def get_matrix(name):
    s = Search()
    results = OrderedDict()
    with open("PRs.json", "r") as fp:
        lines = json.load(fp)
    PRs = {}
    for line in lines:
        cat = line["cat"]
        if cat not in PRs:
            PRs[cat] = []
        PRs[cat].append(line)
    val = s.get_number_of_results(name)
    print "> %10d\t%s" % (val, "General")
    results["General"] = val
    for pr in sorted(PRs):
        sleep(10)
        sites = " " + " OR ".join(["site:%s" % (site["link"],) for site in PRs[pr]])
        num = s.get_number_of_results(name + sites)
        print "> %10d\t%s\n  %10d" % (num, pr, num / len(PRs[pr]))
        results[pr] = num / len(PRs[pr])
    with open("words/%s.json" % name, "wb") as fp:
        json.dump(results, fp)
    with open("words/%s.txt" % name, "wb") as fp:
        fp.write("\n".join(["%s\t%s" % (key, val) for key, val in results.items()]))
    for pr in sorted(PRs):
        sites = ", ".join([site["name"] for site in PRs[pr]])
        print "%s (%s): %s" % (pr, len(PRs[pr]), sites)


for word_file in os.listdir("./words/"):
    if not word_file.endswith(".json"):
        continue
    with open("./words/"+word_file, "r") as fp:
        word = json.load(fp)
        print os.path.basename(word_file)[:-5],
        print "\t",
        print word["General"],
        print "\t",
        print log(word["General"], 2),
        print "\t",
        rank = 0
        for key, val in word.items():
            if not key.startswith("PR"):
                continue
            index = int(key[2:])+1
            rank+=(3**index)*log(val+1, 2)/1500.0
        print rank,
        print "\t",
        print "\t".join([str(word[key]) for key in sorted(word) if key != "General"])

