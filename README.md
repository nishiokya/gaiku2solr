
# gaiku2solr

街区レベル位置参照情報を全文検索エンジンであるSolrに投入するスクリプト
https://nlftp.mlit.go.jp/isj/index.html

https://github.com/geolonia/japanese-addresses
## 使い方
solr 8.2で動作確認しています

|  環境   |  設定 | 説明  | 
| ---- | ---- |---- |
|  コレクション   |  address |   | 

### コレクションの作成

```
bin/solr create -c address -s 2 -rf 2
```

### Abyssのスキーマの作成
|  フィールド名   |  日本語名  | 説明  | サンプル  |
| ---- | ---- |---- |---- |
|prefname|都道府県名|当該範囲の都道府県名|"福島県"|
|cityname|市区町村名|当該範囲の市区町村名 郡部は郡名、政令指定都市の区名も含む）|"本宮市"|
|ooazaname|大字・丁目名|当該範囲の大字・丁目名（丁目の数字は漢数字）|"岩根"|
|azaname|小字・通称名|当該範囲の小字・通称名|"下桶"|
|gaikuname|街区符号・地番|当該範囲の街区符号・地番（通常は1以上の半角整数。ただし地域により漢字・アルファベット等もある）|"126"|
|zahyo|座標系番号|平面直角座標系の座標系番号（1～19までの半角整数）|"9"
|x|X座標|平面直角座標系の座標系原点からの距離メートル単位、北方向プラス（小数第1位まで、半角）|"164065.1"|
|y|Ｙ座標|平面直角座標系の座標系原点からの距離メートル単位、東方向プラス（小数第1位まで、半角）|"43616.6"|
|lat|緯度|十進経緯度（小数点以下第6位まで、半角）|"37.477545"|
|lon|経度|十進経緯度（小数点以下第6位まで、半角）|"140.326492"|
|jyuukyo|住居表示フラグ|1：住居表示実施、0：住居表示未実施（半角）|"0"|
|daihyo|代表フラグ|1：代表する、0：代表しない（半角）1つの街区符号または地番が複数の代表点に対応付けられる場合などに、そのうちの1つに便宜的に代表フラグを立てる。1つの街区符号または地番に対し1つのデータの場合は、当該データに対して代表フラグを立てる|"1"|
|history1|更新前履歴フラグ|1：新規作成、2：名称変更、3：削除、0：変更なし（半角）|"0"|
|history2|更新後履歴フラグ|1：新規作成、2：名称変更、3：削除、0：変更なし（半角）|"1"|
|lonlat|緯度経度|||

#### スキーマ



```
curl -X POST -H 'Content-type:application/json' -d @add_schema.json  http://localhost:8983/solr/address/schema


```
### 位置参照情報のダウンロード方法データの投入方法

令和元年の位置参照情報を都道府県ごとにダウンロードし、"data"ディレクトリは以下に配置します
```
python download.py
```

### データの投入方法

"data"ディレクトリは以下に配置されたcsvファイルを全て変換します
また、[Geolonia 住所データ](https://github.com/geolonia/japanese-addresses)に存在する大字の場合市町村コードを付与します

```
python gen.py
```

### 検索方法

愛知県の県庁(愛知県名古屋市中区三の丸三丁目1番2号)のジオコーディング
```
http://localhost:8983/solr/address/select?q=address%3A愛知県名古屋市中区三の丸三丁目1番2号
```

愛知県の県庁のリバースジオコーディング
```
http://localhost:8983/solr/address/select?q={!func}geodist()&pt=35.180373,136.908547&sort=geodist() asc&sfield=latlon
```

## Resource

以下を利用
* [国土交通省位置参照情報ダウンロードサイト](https://nlftp.mlit.go.jp/cgi-bin/isj/dls/_choose_method.cgi)
* [Geolonia 住所データ](https://github.com/geolonia/japanese-addresses)