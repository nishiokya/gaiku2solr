#<input type="button" align="center" value="ダウンロード済み" name="01000-18.0a" onclick="DownLd2('3.7MB','01000-18.0a.zip','/isj/dls/data/18.0a/01000-18.0a.zip',this)">
import requests
from io import BytesIO, StringIO
import zipfile
import csv
import pandas as pd

def csvreader(filename,outfile):
   print(filename)
   with zip_file.open(filename) as f:  
      csvfile = (pd.read_csv(f, encoding='cp932', sep=","))
      csvfile.to_csv(outfile, index=False, encoding='cp932')
   
version = "18.0a"
for i in range(1,47):
   url = "https://nlftp.mlit.go.jp//isj/dls/data/{0}/{1:02d}000-{0}.zip".format(version,i)
   outfile = "data/{1:02d}000-{0}.csv".format(version,i)
   r = requests.get( url)
   
   zip_file = zipfile.ZipFile(BytesIO(r.content))
   files = zip_file.namelist()
   for filename in files:
      if filename[-4:] == ".csv":
         #print(f)
         csvreader(filename,outfile)
      
   

   
