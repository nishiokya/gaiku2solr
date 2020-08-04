#!/usr/bin/env python3

import re
import unicodedata
import csv
import json
import sys
import requests

url = "http://localhost:8983/solr/address/update?commit=true"
method = "POST"
additems = []



#with open("gomi", encoding='cp932') as f:
with open("/Users/nishiokatakaaki/work/solr-8.2.0/23000-17.0a/23_2018.csv", encoding='cp932') as f:

    reader = csv.reader(f)
    header = next(reader)
    i = 1
    
    
    for line in reader:
        #row =(line[:-1]).split(",")
        row = line
        item = {
            "id" : i,
            "prefname":row[0],
            "cityname":row[1],
            "ooazaname":row[2],
            "azaname":row[3],
            "gaikuname":row[4],
            "zahyou":row[5],
            "x":row[6],
            "y":row[7],
            "lat":row[8],
            "lon":row[9],
            "jyuukyo":row[10],
            "daihyou":row[11],
            "history1":row[12],
            "history2":row[13],
            "lonlat":str(row[9])+","+str(row[8])
        }
        i+=1
        additems.append((item))

data = json.dumps(additems).encode("utf-8")
#print(data)
headers = {"Content-Type" : "application/json; charset=utf-8"}

request = requests.post(url, data=data, headers=headers)

response = request.json()