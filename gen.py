#!/usr/bin/env python3

import re
import unicodedata
import csv
import json
import sys
import requests
import glob

ooazadict = {}
citydict = {}

def getAddressMaster():
    global ooazadict ,citydict
    url = "https://raw.githubusercontent.com/geolonia/japanese-addresses/master/data/latest.csv"
    r = requests.get( url)
    print("get address master {}".format(r.status_code))
    reader = csv.reader(r.text.splitlines())
    header = next(reader)
    for line in reader:
        #print(line[9])
        address = line[1]+line[5]+line[9]
        city = line[1]+line[5]
        #print(address)
        ooazadict[address] = line
        citydict[city] = line

def getGaiku(filnename):
    global ooazadict ,citydict
    

    url = "http://localhost:8983/solr/address/update?commit=true"
    method = "POST"
    additems = []

    #with open("gomi", encoding='cp932') as f:
    #<input type="button" align="center" value="ダウンロード済み" name="01000-18.0a" onclick="DownLd2('3.7MB','01000-18.0a.zip','
    # /isj/dls/data/18.0a/01000-18.0a.zip',this)">
    with open(filnename, encoding='cp932') as f:

        reader = csv.reader(f)
        header = next(reader)
        i = 1
        
        
        for line in reader:
            
            address = line[0]+line[1]+line[2]+line[4]
            city = line[0]+line[1]
            #print(address)
            if address in ooazadict.keys():
                acode = ooazadict[address]

                
                item = {
                    "id" : address,
                    "prefname":line[0],
                    "cityname":line[1],
                    "ooazaname":line[2],
                    "azaname":line[3],
                    "gaikuname":line[4],
                    "zahyo":line[5],
                    "x":line[6],
                    "y":line[7],
                    "lat":line[8],
                    "lon":line[9],
                    "jyuukyo":line[10],
                    "daihyo":line[11],
                    #"history1":line[12],
                    #"history2":line[13],
                    "lonlat":str(line[9])+","+str(line[8]),
                    "prefcode":acode[0],
                    "citycode":acode[4],
                    "ooazacode":acode[8],
                    "address":address

                }
                i+=1
                
            elif city in citydict.keys():
                acode = citydict[city]
                item = {
                    "id" : address,
                    "prefname":line[0],
                    "cityname":line[1],
                    "ooazaname":line[2],
                    "azaname":line[3],
                    "gaikuname":line[4],
                    "zahyo":line[5],
                    "x":line[6],
                    "y":line[7],
                    "lat":line[8],
                    "lon":line[9],
                    "jyuukyo":line[10],
                    "daihyo":line[11],
                    #"history1":line[12],
                    #"history2":line[13],
                    "lonlat":str(line[9])+","+str(line[8]),
                    "prefcode":city[0],
                    "citycode":city[4],
                    #"ooazacode":acode[8],
                    "address":address

                }
            else:
                item = {
                    "id" : address,
                    "prefname":line[0],
                    "cityname":line[1],
                    "ooazaname":line[2],
                    "azaname":line[3],
                    "gaikuname":line[4],
                    "zahyo":line[5],
                    "x":line[6],
                    "y":line[7],
                    "lat":line[8],
                    "lon":line[9],
                    "jyuukyo":line[10],
                    "daihyo":line[11],
                    #"history1":line[12],
                    #"history2":line[13],
                    "lonlat":str(line[9])+","+str(line[8]),
                    
                    "address":address

                }
            additems.append((item))
                #print(address)
            
    data = json.dumps(additems).encode("utf-8")
    #print(data)
    headers = {"Content-Type" : "application/json; charset=utf-8"}

    request = requests.post(url, data=data, headers=headers)

    response = request.json()
    print(response)


def main():
    getAddressMaster()
    for filename in glob.glob("data/*.csv"):
        print("import : {}".format(filename))
        getGaiku(filename)


if __name__ == "__main__":
    main()