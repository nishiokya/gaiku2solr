
# gaiku2solr

このスクリプトは、街区レベル位置参照情報を全文検索エンジンであるSolrに投入するためのものです。
以下のウェブサイトから情報を取得します：[https://nlftp.mlit.go.jp/isj/index.html](https://nlftp.mlit.go.jp/isj/index.html) 

ダウンロード部分は、Geolonia 住所データを参考にしています：[https://github.com/geolonia/japanese-addresses](https://github.com/geolonia/japanese-addresses) 

## 使い方

このスクリプトは、Solr 9.1で動作確認しています。

|  環境   |  設定 | 説明  | 
| ---- | ---- |---- |
|  コレクション   |  address |  SolrのCollectionの名称です | 


### 郵便番号データのダウンロード

郵便番号データをダウンロードし、KEN_ALL.TSVを `data` フォルダに配置してください。データは、以下のウェブサイトから入手できます：[郵便番号データダウンロード](https://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html) 
### コレクションの作成

```python
bin/solr create -c address -s 2 -rf 2
```


### Addressのスキーマ
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
|address|連結した住所文字列||東京都千代田区内幸町１丁目１−１ |
|postcode|||100-0005|
|yomi|読み||イタブシチョウ|

#### スキーマの作成



```
curl -X POST -H 'Content-type:application/json' -d @add_schema.json  http://localhost:8983/solr/address/schema


```
### 位置参照情報のダウンロード方法データの投入方法

事前にKEN_ALL.TSVを配置してください。

```
data/
├── KEN_ALL.CSV

```


データのダウンロードには以下のコマンドを使用します。
download.pyを実行すると令和3年の位置参照情報を都道府県ごとにダウンロードします。
10G程度必要です

```
python download.py
```

### データの投入方法

以下のコマンドを使用すると、"data"ディレクトリに配置されたCSVファイルをすべて変換し、大字が存在する場合は[Geolonia 住所データ](https://github.com/geolonia/japanese-addresses) から市町村コードを付与します。


```
python gen.py
```

### 検索方法

#### Geocoder

愛知県の県庁（愛知県名古屋市中区三の丸三丁目1番2号）をジオコーディングする場合は、以下のようなURLを使用します。
```
http://localhost:8983/solr/address/select?q=address%3A愛知県名古屋市中区三の丸三丁目1番2号
```

#### Reverse Geocoder

愛知県の県庁をリバースジオコーディングする場合は、以下のようなURLを使用します。
```
http://localhost:8983/solr/address/select?q={!func}geodist()&pt=35.180373,136.908547&sort=geodist() asc&sfield=latlon
```

#### Suggester

solrconfig.xmlに以下の設定を追加します
```

  <!-- suggestコンポーネントの定義 -->
<searchComponent name="suggest" class="solr.SuggestComponent">
    <lst name="suggester">
        <str name="name">japaneseSuggester</str>
        <str name="lookupImpl">AnalyzingInfixLookupFactory</str>
        <str name="dictionaryImpl">DocumentDictionaryFactory</str>
        <str name="field">address</str>
        <str name="suggestAnalyzerFieldType">text_ja</str>
        <str name="buildOnStartup">false</str>
        <str name="buildOnCommit">false</str>
        <str name="suggest-accuracy">0.7</str>
        <str name="suggest-fuzzy">true</str>
        <str name="suggest-fuzzy-min-length">1</str>
        <str name="highlight">false</str>
    </lst>
</searchComponent>
  
  <!-- suggestコンポーネントのリクエストハンドラへの追加 -->
  <requestHandler name="/suggest" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <str name="suggest">true</str>
      <str name="suggest.count">10</str>
      <str name="suggest.dictionary">japaneseSuggester</str>
    </lst>
    <arr name="components">
      <str>suggest</str>
    </arr>
  </requestHandler>
```
http://localhost:8983/solr/address/suggest?suggest=true&suggest.build=true&suggest.dictionary=japaneseSuggester&suggest.q=愛知

## Resource

以下のリソースを利用しています。 
* [国土交通省位置参照情報ダウンロードサイト](https://nlftp.mlit.go.jp/cgi-bin/isj/dls/_choose_method.cgi)
* [Geolonia 住所データ](https://github.com/geolonia/japanese-addresses)
* [郵便番号データダウンロード](https://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html) 
