#!/usr/bin/env python3

import re
import unicodedata
import csv
import json
import sys
import requests
import glob
import unicodedata

ooazadict = {}
citydict = {}
postdict = {}

coreurl = "http://localhost:8983/solr/address"

def yuragi(prefname,cityname,ooazaname):
    postalLists = []
    #大字なし対応
    if ooazaname == "八幡浜市の次に番地がくる場合":
        postalLists.append(prefname+cityname+"（大字なし）")
    #丁目対応
    choume = "[０-９|一二三四五六七八九十壱十百千万]丁目"
    if ooazaname[-2:] == "丁目":
        ooazaname_del = re.sub(choume, '', ooazaname)
      
        return prefname+cityname+ooazaname_del
    
    return None

def postalYuragi(prefname,cityname,ooazaname):
    postalLists = []
    #大字なし対応
    if ooazaname == "八幡浜市の次に番地がくる場合":
        postalLists.append(prefname+cityname+"（大字なし）")
    #丁目対応
    choume = "[０-９|一二三四五六七八九十壱十百千万]丁目"
    #if ooazaname[-2:] == "丁目":
        #ooazaname_del = re.sub(choume, '', ooazaname)
        #print(ooazaname_del)
        #postalLists.append(prefname+cityname+ooazaname_del)

    
    return postalLists

def getPostMaster():
    filnename = "data/KEN_ALL.CSV"
    with open(filnename, encoding='sjis') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            #print(line)
            postalkey = line[6]+line[7]+line[8]
            postdict[postalkey] = line
            postalLists = postalYuragi(line[6],line[7],line[8])
            for postal in postalLists:
                postdict[postal] = line
            
        

def getAddressMaster():
    global ooazadict ,citydict
    url = "https://raw.githubusercontent.com/geolonia/japanese-addresses/master/data/latest.csv"
    r = requests.get( url)
    print("get address master {}".format(r.status_code))
    reader = csv.reader(r.text.splitlines())
    header = next(reader)
    for line in reader:
        #print(line)
        ooaza = line[1]+line[5]+line[9]
        city = line[1]+line[5]
        #print(address)
        ooazadict[ooaza] = line
        citydict[city] = line

def makeAddress(line):
    address = line[0]+line[1]+line[2]+line[3]+line[4]
    if line[2]== "（大字なし）":
        address = line[0]+line[1]+line[3]+line[4]
    return address
def getGaiku(filnename,filedump=False):
    global ooazadict ,citydict,postdict
    

    url = coreurl+ "/update?commit=true"
    method = "POST"
    additems = []

    #with open("gomi", encoding='cp932') as f:
    #<input type="button" align="center" value="ダウンロード済み" name="01000-18.0a" onclick="DownLd2('3.7MB','01000-18.0a.zip','
    # /isj/dls/data/18.0a/01000-18.0a.zip',this)">
    with open(filnename, encoding='utf-8') as f:

        reader = csv.reader(f)
        header = next(reader)
        i = 1
        prefcode = filnename[5:7]
  
        for line in reader:
            
            address = makeAddress(line)
            addressid = line[0]+line[1]+line[2]+line[3]+line[4]
            ooaza = line[0]+line[1]+line[2]
            city = line[0]+line[1]
            yomi = None
            postcode = None
            citycode = None
            ooazacode = None
            #print(address)
            #JPMasterと大字レベルでマッチ
            if ooaza in ooazadict.keys():
                acode = ooazadict[ooaza]
                prefcode = acode[0]
                citycode = acode[4]
                ooazacode = acode[8]
                
                
            elif city in citydict.keys():
                acode = citydict[city]
                prefcode = acode[0]
                citycode = acode[4]

            if ooaza in postdict.keys():
                #print(postdict[ooaza])
                zcode = postdict[ooaza]
                postcode = zcode[2]
                yomi = zcode[3]+ zcode[4]+ zcode[5]
            elif yuragi(line[0],line[1],line[2]) in postdict.keys():
                #print(postdict[ooaza])
                zcode = postdict[yuragi(line[0],line[1],line[2]) ]
                postcode = zcode[2]
                yomi = zcode[3]+ zcode[4]+ zcode[5]
  
            
            if len(line) < 11:
                print("length is: {} {}",(len(line),line))
                next
            
            if len( line) <12 :
                daihyo = ""
                print("length is: {} {}",(len(line),line))
                print(line)
            else:
                daihyo = line[11]
            
            item = {
                "id" : addressid,
                "prefname":line[0],
                "cityname":line[1],
                "ooazaname":line[2],
                "azaname":" "  if line[3] is None else line[3],
                "gaikuname":line[4],
                "zahyo":line[5],
                "x":line[6],
                "y":line[7],
                "lat":line[8],
                "lon":line[9],
                "jyuukyo":line[10],
                "daihyo":daihyo,
                #"history1":line[12],
                #"history2":line[13],
                "latlon":str(line[8])+","+str(line[9]),
                "address":address,
                "prefcode":prefcode,
               # "display" : addressid,
                

            }
            #print(address)
            
            if citycode:
                item["citycode"] = citycode
            if ooazacode:
                item["ooazacode"] = ooazacode
            if yomi:

                item["yomi"] = unicodedata.normalize('NFKC', yomi)
            if postcode:
                item["postcode"] = postcode
            
            
            additems.append((item))
                
            

    if filedump == True:
        with open("tmp/post_data_"+filnename[5:],"w", encoding='utf-8') as f:
            for  value in additems:
                f.write("\t".join(value.values())+"\n")
    else:
        data = json.dumps(additems).encode("utf-8")
        headers = {"Content-Type" : "application/json; charset=utf-8"}
        request = requests.post(url, data=data, headers=headers)
        response = request.json()

        print(response)

def deleteAll():

    data = "{'delete': {'query': '*:*'}}"
    print(data)

    url = coreurl+ "/update?commit=true"
    headers = {"Content-Type" : "application/json;"}

    request = requests.post(url, data=data, headers=headers)

    request = requests.post(url)

    response = request.text
    print(response)

def main():
    getPostMaster()
    getAddressMaster()
    deleteAll()
    for filename in glob.glob("data/*.csv"):
        print("import : {}".format(filename))
        getGaiku(filename,filedump=False)


if __name__ == "__main__":
    main()


#エラーデータ
#{'responseHeader': {'rf': 1, 'status': 400, 'QTime': 19551}, 'error': {'metadata': ['error-class', 'org.apache.solr.common.SolrException', 'root-error-class', 'org.apache.solr.common.SolrException'], 'msg': '[doc=兵庫県神戸市西区井吹台北町五丁目] missing required field: gaikuname', 'code': 400}}
