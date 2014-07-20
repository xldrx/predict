#! /usr/bin/env python -u
# coding=utf-8
import logging
from multiprocessing import Process
import os
from utils import iotools

__author__ = 'xl'

from scrapy.cmdline import execute
from scrapy import log


def remove_file(name):
    if os.path.exists(name):
        os.remove(name)


def fix_json(name):
    data = iotools.load_raw(name)
    lines = data.split("\n")
    if lines[-1] == "":
        del lines[-1]
    data = "[%s]" % ",".join(lines)
    iotools.save_raw(data, name)

    data = iotools.load_json(name)
    iotools.save_json(data, name)


def execute_spider(crawler_name, output_file_name):
    # log.setLevel("ERROR")
    execute(argv=['scrapy', 'crawl', crawler_name, '-o', output_file_name, '-s', 'LOG_LEVEL=INFO'])


def run_crawlers(crawler_name, output_file_name):
    remove_file(output_file_name)
    p = Process(target=execute_spider, args=(crawler_name, output_file_name))
    p.start()
    p.join()
    fix_json(output_file_name)


if __name__ == "__main__":
    # run_crawlers("extract-predict", "../data/raw/dataset.json")
    # run_crawlers("symantec", "../data/raw/terms.json")
    run_crawlers("symantec-rest", "../data/raw/terms-rest.json")
    run_crawlers("sans", "../data/raw/sans.json")