
# gaiku2solr

このプロジェクトは、国土交通省が提供する街区レベル位置参照情報を全文検索エンジンであるSolrに投入し、住所のジオコーディング・リバースジオコーディング機能を提供するためのものです。

**データソース：**
- [国土交通省位置参照情報ダウンロードサイト](https://nlftp.mlit.go.jp/isj/index.html)
- [Geolonia 住所データ](https://github.com/geolonia/japanese-addresses)（市町村コード付与用）
- [郵便番号データ](https://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html)（郵便番号情報用）

## プロジェクト構成

```
gaiku2solr/
├── README.md              # このファイル
├── download.py            # 位置参照情報データのダウンロード
├── gen.py                 # データ変換・Solr投入処理
├── viewer.py              # データ確認用ビューアー
├── add_schema.json        # Solrスキーマ定義
├── report.md              # プロジェクトレポート
├── solr.md                # Solr設定ドキュメント
└── suggester/             # サジェスト機能関連
    ├── get_pref.py        # 都道府県データ取得
    ├── prefecture.tsv     # 都道府県マスタ
    ├── solrconfig.xml     # Solr設定ファイル
    └── suggester.md       # サジェスト機能ドキュメント
```

## 動作環境

- **Apache Solr**: 9.1以上
- **Python**: 3.9.2以上
- **必要なPythonライブラリ**: requests, csv（標準ライブラリ）

|  設定項目   |  値 | 説明  | 
| ---- | ---- |---- |
|  Solrコレクション名   |  address |  住所データを格納するSolrコレクション | 
|  SOLR_URL環境変数  |  http://localhost:8983 |  SolrサーバーのURL |
## セットアップ手順

### 1. Solrコレクションの作成

```bash
bin/solr create -c address -s 2 -rf 2
```

### 2. スキーマの設定

プロジェクトに含まれる`add_schema.json`を使用してSolrスキーマを設定します：

```bash
curl -X POST -H 'Content-type:application/json' -d @add_schema.json http://localhost:8983/solr/address/schema
```

### 3. 郵便番号データの準備

郵便番号データをダウンロードし、`KEN_ALL.CSV`を`data`フォルダに配置してください：

- データ取得先：[郵便番号データダウンロード](https://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html)
- 配置場所：`data/KEN_ALL.CSV`

### 4. 位置参照情報のダウンロード

```bash
python download.py
```

このコマンドにより、令和5年（2023年）の位置参照情報を都道府県ごとにダウンロードします（約10GB必要）。

### 5. データの変換・投入

```bash
python gen.py
```

`data`ディレクトリ内のCSVファイルを変換し、Solrに投入します。大字が存在する場合は[Geolonia 住所データ](https://github.com/geolonia/japanese-addresses)から市町村コードを付与します。

#### オプション：テキスト出力

```bash
python gen.py --dump
```


## データスキーマ

### フィールド定義
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
|postcode|郵便番号|当該住所に対応する郵便番号|100-0005|
|yomi|読み|住所の読み仮名|イタブシチョウ|

## 使用方法

### ジオコーディング（住所→座標）

愛知県の県庁（愛知県名古屋市中区三の丸三丁目1番2号）をジオコーディングする場合：

```
http://localhost:8983/solr/address/select?q=address:愛知県名古屋市中区三の丸三丁目1番2号
```

### リバースジオコーディング（座標→住所）

指定した座標（愛知県庁の位置）から最も近い住所を検索する場合：

```
http://localhost:8983/solr/address/select?q={!func}geodist()&pt=35.180373,136.908547&sort=geodist() asc&sfield=latlon
```

### サジェスト機能

住所の自動補完機能を使用するには、`suggester/solrconfig.xml`の設定をSolrに適用してください。

#### 設定例

```xml
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

#### 使用例

```
http://localhost:8983/solr/address/suggest?suggest=true&suggest.build=true&suggest.dictionary=japaneseSuggester&suggest.q=愛知
```

## 注意事項

- SolrのURLは`SOLR_URL`環境変数で指定します（デフォルト：http://localhost:8983）
- データ投入時はSolrのHTTP APIを使用します
- APIの詳細は[Solr Reference Guide](https://solr.apache.org/guide/solr/latest/index.html)を参照してください

## 参考資料

以下のリソースを利用しています。 
* [国土交通省位置参照情報ダウンロードサイト](https://nlftp.mlit.go.jp/cgi-bin/isj/dls/_choose_method.cgi)
* [Geolonia 住所データ](https://github.com/geolonia/japanese-addresses)
* [郵便番号データダウンロード](https://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html) 
