
# gaiku2solr

街区レベル位置参照情報をsolrに投入するスクリプト
https://nlftp.mlit.go.jp/isj/index.html

## 使い方
solr 8.1が起動されている

|  環境   |  設定 | 説明  | 
| ---- | ---- |---- |
|  環境   |  設定 | 説明  | 

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
<field name="azaname" type="text_general" uninvertible="true" indexed="true" stored="true"/>
  <field name="cityname" type="text_general" uninvertible="true" indexed="true" stored="true"/>
  <field name="daihyo" type="pdouble" uninvertible="true" indexed="true" stored="true"/>
  <field name="gaikuname" type="text_general" uninvertible="true" indexed="true" stored="true"/>
  <field name="history1" type="pint" uninvertible="true" indexed="true" stored="true"/>
  <field name="history2" type="pint" uninvertible="true" indexed="true" stored="true"/>
  <field name="id" type="string" multiValued="false" indexed="true" required="true" stored="true"/>
  <field name="jyuukyo" type="pint" uninvertible="true" indexed="true" stored="true"/>
  <field name="lat" type="pdoubles" uninvertible="true" indexed="true" stored="true"/>
  <field name="lon" type="pdouble" uninvertible="true" indexed="true" stored="true"/>
  <field name="lonlat" type="pint" uninvertible="true" indexed="true" stored="true"/>
  <field name="ooazaname" type="text_ja" uninvertible="true" indexed="true" stored="true"/>
  <field name="prefname" type="text_general" uninvertible="true" indexed="true" stored="true"/>
  <field name="x" type="pdouble" uninvertible="true" indexed="true" stored="true"/>
  <field name="y" type="pdoubles" uninvertible="true" indexed="true" stored="true"/>
  <field name="zahyou" type="pint" uninvertible="true" indexed="true" stored="true"/>
```

```
curl -X POST -H 'Content-type:application/json' -d @add_schema.json  http://localhost:8983/solr/address/schema


```
### データの投入方法
```
python gen.py
```

### 検索方法

