import pandas as pd
import requests

# SolrのURLを指定します。
solr_url = "http://localhost:8983/solr/address"

# 都道府県の緯度と経度を取得するためのAPIを指定します。
geocode_url = "https://geocode.csis.u-tokyo.ac.jp/cgi-bin/simple_geocode.cgi"

# 都道府県データが保存されているTSVファイルのパスを指定します。
tsv_path = "prefecture.tsv"

# TSVファイルをpandasで読み込みます。
df = pd.read_csv(tsv_path, delimiter="\t", header=None, names=["prefname", "latlon"])

# latlonカラムを緯度と経度に分割して、それぞれ別のカラムに格納します。
df[["lat", "lon"]] = df["latlon"].str.split(",", expand=True)

# Solrにデータを登録します。
data_list = []
for i, row in df.iterrows():
    # 都道府県名と緯度、経度を取得します。
    pref_name = row["prefname"]
    lat = row["lat"]
    lon = row["lon"]

    # Solrに登録するデータを作成します。
    data = {
        "prefname": pref_name,
        "cityname": "",
        "ooazaname": "",
        "azaname": "",
        "gaikuname": "",
        "zahyo": "1",
        "x": lon,
        "y": lat,
        "lat": lat,
        "lon": lon,
        "jyuukyo": "0",
        "daihyo": "",
        "history1": "",
        "history2": "",
        "latlon": f"{lat},{lon}",
        "prefcode": "",
        "citycode": "",
        "string": f"{lat},{lon}",
        "address": "",
        "postcode": "",
        "yomi": "",
        "level": "1"
    }

    # Solrにデータを登録するためのAPIを呼び出します。
    response = requests.post(f"{solr_url}/update/json/docs", json.dumps(data))
    print(response.text)

# Solrに登録したデータをコミットします。
response = requests.get(f"{solr_url}/update?commit=true")
print(response.text)

# TSVファイルを書き込みモードで開きます。
with open(tsv_path, "w") as f:
    # 都道府県データをTSV形式で保存します。
    for i, row in df.iterrows():
        pref_name = row["prefname"]
        lat = row["lat"]
        lon = row["lon"]
        f.write(f"{pref_name}\t{lat},{lon}\n")