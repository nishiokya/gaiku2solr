#<input type="button" align="center" value="ダウンロード済み" name="01000-18.0a" onclick="DownLd2('3.7MB','01000-18.0a.zip','/isj/dls/data/18.0a/01000-18.0a.zip',this)">
import requests
from io import BytesIO, StringIO
import zipfile
import csv

import shutil,os

def csvreader(filename,outfile):
   print(filename)
   with zip_file.open(filename) as f:  
      with open(outfile, 'w', encoding='CP932') as w:  
         for s in f:
            w.write(s.decode('CP932'))
   
version = "18.0a"
os.system('rm tmp/*.csv' )
for i in range(1,48):
   url = "https://nlftp.mlit.go.jp//isj/dls/data/{0}/{1:02d}000-{0}.zip".format(version,i)
   outfile = "{1:02d}000-{0}.csv".format(version,i)
   outzip = "data/{1:02d}000-{0}.zip".format(version,i)
   r = requests.get( url)

   zip_file = zipfile.ZipFile(BytesIO(r.content))
   files = zip_file.namelist()
   for filename in files:
      if filename[-4:] == ".csv":
         #print(f)
         zip_file.extract(filename,"tmp")
         new_path = shutil.move('tmp/'+filename, 'tmp/'+outfile)
         os.system('nkf -w tmp/'+outfile  +' > data/'+outfile )
         #csvreader(filename,outfile)
"""
   handle = open(outzip, "wb")
   #handle.write(r.text)
   for chunk in r.iter_content(chunk_size=512):
      if chunk:  # filter out keep-alive new chunks
         handle.write(chunk)
   handle.close()
"""
"""
32000-18.0a/32_2019.csv
Traceback (most recent call last):
  File "pandas/_libs/parsers.pyx", line 1151, in pandas._libs.parsers.TextReader._convert_tokens
  File "pandas/_libs/parsers.pyx", line 1281, in pandas._libs.parsers.TextReader._convert_with_dtype
  File "pandas/_libs/parsers.pyx", line 1300, in pandas._libs.parsers.TextReader._string_convert
  File "pandas/_libs/parsers.pyx", line 1577, in pandas._libs.parsers._string_box_decode
UnicodeDecodeError: 'cp932' codec can't decode byte 0x91 in position 9: incomplete multibyte sequence

During handling of the above exception, another exception occurred:
https://map.yahoo.co.jp/address?ac=32207&az=20


"島根県","江津市","二宮町神主","","ｲ1220","3","-112803.6","2502.6","34.983185","132.194078","0","1"
"島根県","江津市","二宮町神主","","ｲ1221","3","-112803.6","2502.6","34.983185","132.194078","0","1"
"島根県","江津市","二宮町神主","","ｲ1222","3","-112803.6","2502.6","34.983185","132.194078","0","1"
"島根県","江津市","二宮町神主","","ｲ1223","3","-112803.6","2502.6","34.983185","132.194078","0","1"
"島根県","江津市","二宮町神主","","ｲ1298","3","-112803.6","2502.6","34.983185","132.194078","0","0"
"島根県","江津市","二宮町神主","","2177","3","-112803.6","2502.6","34.983185","132.194078","0","1"
"島根県","江津市","二宮町神主","","2179","3","-112803.6","2502.6","34.983185","132.194078","0","1"
"島根県","江津市","二宮町神主","","ｲ1114続内�","3","-112803.6","2502.6","34.983185","132.194078","0","1"
"島根県","江津市","二宮町神主","","ｲ1115続内�","3","-112803.6","2502.6","34.983185","132.194078","0","1"
"島根県","江津市","二宮町神主","","ｲ1117続内�","3","-112803.6","2502.6","34.983185","132.194078","0","1"

"""
   

   
