#!/usr/bin/env python3

import re
import unicodedata
import csv
import json
import sys
import requests
import io


def getAddressMaster():
    global ooazadict 
    url = "https://raw.githubusercontent.com/geolonia/japanese-addresses/master/data/latest.csv"
    r = requests.get( url)
    print("get address master {}".format(r.status_code))
    reader = csv.reader(r.text.splitlines())
    header = next(reader)
    for line in reader:
        #print(line[9])
        address = line[1]+line[5]+line[9]
        #print(address)
        ooazadict[address] = line
        
ooazadict = {}
getAddressMaster()

url = "http://localhost:8983/solr/address/update?commit=true"
method = "POST"
additems = []

#with open("gomi", encoding='cp932') as f:
with open("/Users/nishiokatakaaki/work/solr-8.2.0/23000-17.0a/23_2018.csv", encoding='cp932') as f:

    reader = csv.reader(f)
    header = next(reader)
    i = 1
    
    
    for line in reader:
        
        address = line[0]+line[1]+line[2]
        #print(address)
        if address in ooazadict.keys():
            acode = ooazadict[address]

            
            item = {
                "id" : i,
                "prefname":line[0],
                "cityname":line[1],
                "ooazaname":line[2],
                "azaname":line[3],
                "gaikuname":line[4],
                "zahyou":line[5],
                "x":line[6],
                "y":line[7],
                "lat":line[8],
                "lon":line[9],
                "jyuukyo":line[10],
                "daihyou":line[11],
                "history1":line[12],
                "history2":line[13],
                "lonlat":str(line[9])+","+str(line[8]),
                "prefcode":acode[0],
                "citycode":acode[4],
                "ooazacode":acode[8],
                "address":address

            }
        else:
            print(address)
        i+=1
        additems.append((item))

data = json.dumps(additems).encode("utf-8")
#print(data)
headers = {"Content-Type" : "application/json; charset=utf-8"}

request = requests.post(url, data=data, headers=headers)

response = request.json()