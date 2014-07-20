#! /usr/bin/env python -u
# coding=utf-8
import re
import string
from datetime import date, datetime

from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spider import Spider
from crawlers.items import SymantecKB, SymantecKBRest

__author__ = 'xl'


class Symantec(Spider):
    name = "symantec"
    allowed_domains = ["http://www.symantec.com/security_response/"]

    def __init__(self):
        # self.start_urls = ["http://www.symantec.com/security_response/landing/azlisting.jsp?azid=%s" % (s)
        #                    for s in ["X"]]
        self.start_urls = ["http://www.symantec.com/security_response/landing/azlisting.jsp?azid=%s" % (s)
                           for s in list(string.uppercase)+["_1234567890"]]

    def parse(self, response):
        hxs = Selector(response)

        for row in hxs.xpath("body//tr[@class='odd' or @class='even']"):
            kb = SymantecKB()
            kb['name'] = row.xpath("td[2]/a/text()").extract()[0]
            kb['link'] = row.xpath("td[2]/a/@href").extract()[0]
            types = row.xpath("td[3]/text()").extract()
            kb['types'] = types[0] if len(types)>0 else None
            discovered = row.xpath("td[4]/text()").extract()
            kb['discovered'] = datetime.strptime(discovered[0],"%m/%d/%Y").date() if len(discovered) > 0 else None
            severity = row.xpath("td[1]/img/@src").extract()
            kb['severity'] = int(re.findall("level(.*?)\.png", severity[0])[0]) if len(severity) > 0 else None
            yield kb


class SymantecRest(Spider):
    name = "symantec-rest"
    allowed_domains = ["http://www.symantec.com/security_response/"]

    def __init__(self):
        # self.start_urls = ["http://www.symantec.com/security_response/landing/azlisting.jsp?azid=%s" % (s)
        #                    for s in ["X"]]
        self.start_urls = ["http://www.symantec.com/security_response/landing/azlisting.jsp?azid=%s" % (s)
                           for s in list(string.uppercase)+["_1234567890"]]

    def parse(self, response):
        hxs = Selector(response)
        val = hxs.xpath("body//pre/text()")[0].extract()
        for val in val.split("\n"):
            if val == "":
                continue
            rest = SymantecKBRest()
            rest['name'] = val
            yield rest
