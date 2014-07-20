#! /usr/bin/env python -u
# coding=utf-8
import re
from utils import iotools

__author__ = 'xl'

data = iotools.load_raw("../data/raw/glossary.txt")

ret = {}
for block in re.findall(r"^::: (.+?)$(.*?)(?=\n:::)$", data, re.MULTILINE | re.DOTALL):
    ret[block[0].strip()]=block[1].strip()

print len(ret)