#! /usr/bin/env python -u
# coding=utf-8
import string

from scrapy.selector import Selector
from scrapy.spider import Spider
from crawlers.items import SansKB

__author__ = 'xl'


class Sans(Spider):
    name = "sans"
    allowed_domains = ["https://www.sans.org/security-resources/glossary-of-terms/"]

    def __init__(self):
        # self.start_urls = ["http://www.symantec.com/security_response/landing/azlisting.jsp?azid=%s" % (s)
        #                    for s in ["X"]]
        self.start_urls = ["https://www.sans.org/security-resources/glossary-of-terms/?pass=%s" % (s)
                           for s in list(string.lowercase)+["numeric"]]

    def parse(self, response):
        hxs = Selector(response)

        for name, definition in zip(hxs.xpath("body//dt/text()"), hxs.xpath("body//dd/text()")):
            kb = SansKB()
            kb['name'] = name.extract()
            kb['definition'] = definition.extract()
            yield kb