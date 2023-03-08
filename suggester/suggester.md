# solrのautocompletion
solrconfig.xmlのsuggestコンポーネントと/suggestリクエストハンドラのサマリーと主要なフィールドの表形式での説明です。


# searchComponent

searchComponentの主な目的は、検索リクエストに対してどのような検索ロジックを実行するかを定義することです。たとえば、searchComponentを使用して、Solrが検索要求を処理する際に使用するクエリー解析、検索フィルタ、ソート、ハイライトなどを指定することができます。

searchComponentは、以下のような主要な属性を持ちます。

|フィールド|説明|
|---|---|
|name| searchComponentの名前を指定します。この名前は、requestHandlerのcomponentセクションで使用されます。|
|class| searchComponentのJavaクラス名を指定します。このクラスは、検索ロジックを実装するために使用されます。|
|version| searchComponentのバージョンを指定します。バージョンが指定されている場合、Solrが起動した際に、バージョンの整合性をチェックします。|


```
<searchComponent name="suggest" class="solr.SuggestComponent">
    <lst name="suggester">
        <str name="name">japaneseSuggester</str>
        <str name="lookupImpl">AnalyzingInfixLookupFactory</str>
        <str name="dictionaryImpl">DocumentDictionaryFactory</str>
        <str name="field">address</str>
        <str name="suggestAnalyzerFieldType">text_ja</str>
        <str name="buildOnStartup">false</str>
        <str name="buildOnCommit">false</str>
        <float name="suggest-accuracy">0.7f</float>
        <str name="suggest-fuzzy">true</str>
        <str name="suggest-fuzzy-min-length">1</str>
        <str name="highlight">false</str>
    </lst>
</searchComponent>

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


```
 <searchComponent name="suggest" class="solr.SuggestComponent">
    <lst name="suggester">
      <str name="name">mySuggester</str>
      <str name="lookupImpl">FuzzyLookupFactory</str>
      <str name="dictionaryImpl">DocumentDictionaryFactory</str>
      <str name="field">cat</str>
      <str name="weightField">level</str>
      <str name="suggestAnalyzerFieldType">string</str>
      <str name="buildOnStartup">false</str>
    </lst>
  </searchComponent>
  
  <requestHandler name="/suggest" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <str name="suggest">true</str>
      <str name="suggest.count">10</str>
    </lst>
    <arr name="components">
      <str>suggest</str>
    </arr>
  </requestHandler>
  ```