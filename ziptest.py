# -*- coding: Shift-JIS -*-

import requests
from io import BytesIO, StringIO,TextIOWrapper
import zipfile
import csv
import pandas as pd
import io
import codecs
"""
with open("xaa","r",encoding="cp932") as f:
            for rec in f:
                print(length(rec))
"""
zip_file = zipfile.ZipFile("data/32000-18.0a.zip")
files = zip_file.namelist()
for filename in files:
    if filename[-4:] == ".csv":
        print(filename)
        zip_file.extract(filename,"aaa.csv")
        with codecs.open("aaa.csv/32000-18.0a/32_2019.csv","r",encoding="cp932") as f:
            for rec in f:
                print(rec)
