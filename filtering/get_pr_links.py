import codecs
import csv
import json
import cStringIO

__author__ = 'xl'


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


import requests

url = "http://ddosattackprotection.org/blog/cyber-security-blogs/"
r = requests.get(url)

from bs4 import BeautifulSoup

soup = BeautifulSoup(r.text, "html.parser")
contents = soup.findAll("div", {"class": "entry-content"})[0]
results = []

current_cat = None
for tag in contents:
    if tag.name == "h2":
        current_cat = tag.text

    if tag.name == "h3":
        link = tag.a
        results.append({"name": link.text, "link": link.get('href'), "cat": current_cat})

print len(results)

with open('PRs.csv', 'wb') as fp:
    w = UnicodeWriter(fp)
    w.writerow(results[0].keys())
    for row in results:
        w.writerow(row.values())

with open('PRs.json', 'wb') as fp:
    json.dump(results, fp)