# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class Metadata(Item):
    # define the fields for your item here like:
    name = Field()
    category = Field()
    subcategory = Field()
    host = Field()
    short_desc = Field()
    long_desc = Field()
    size = Field()
    formats = Field()
    anonymization = Field()
    keywords = Field()
    access = Field()
    collection_date = Field()
    provider = Field()
    restriction_class = Field()

class SymantecKB(Item):
    severity = Field()
    name = Field()
    types = Field()
    discovered = Field()
    link = Field()

class SymantecKBRest(Item):
    name = Field()

class SansKB(Item):
    name = Field()
    definition = Field()
