#! /usr/bin/env python -u
# coding=utf-8
import re
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spider import Spider
from crawlers.items import Metadata

__author__ = 'xl'


class basic_search(Spider):
    name = "extract-predict"
    allowed_domains = ["https://www.predict.org"]

    keys = {
        "name": "lblDSName",
        "category": "lblCategory",
        "subcategory": "lblSubCategory",
        "host": "lblHostOrg",
        "provider": "lblProviderOrg",
        "short_desc": "lblShortDesc",
        "long_desc": "lblDesc",
        "size": "lblSize",
        "formats": "lblFormats",
        "anonymization": "lblAnon",
        "keywords": "lblKeywords",
        "access": "lblAccessTypes",
        "collection_date": "lblCollectionDate",
        "restriction_class": "RestrictionLabel",
    }

    def __init__(self):
        self.start_urls = ["https://www.predict.org/Default.aspx?tabid=104"]

    def start_requests(self):
        return [FormRequest("https://www.predict.org/Default.aspx?tabid=104",
                            formdata={'__EVENTTARGET': 'dnn$ctr688$PredictPageRouter$ctl00$grdDatasets',
                                      '__EVENTARGUMENT': 'Page$%i' % i}) for i in range(1, 81)]


    def parse(self, response):
        hxs = Selector(response)
        datasets = hxs.xpath(".//table[contains(@id,'grdDatasets')]/tr[contains(@class,'row')]")
        for dataset in datasets:
            item = Metadata()
            for key, name in self.keys.iteritems():
                val = dataset.xpath(".//*[contains(@id,'%s')]/text()" % name).extract()
                val = val[0] if len(val) > 0 else None
                val = val.strip() if val else None
                if key == 'keywords' or key == 'formats':
                    val = val.split(", ")
                item[key] = val
            yield item
