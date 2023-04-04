+++
title = "検索と文字"
description = ""
weight = 1
+++

ユーザに検索ウィンドウを提供する際，
ユーザが入力した文字列と完全には一致しない項目も検索ヒットの
対象としたいことがある．前方一致・部分一致はその一例である．

少し違う観点では，異なる文字も同一のものとして扱いたいことがある．
ここでは，その実現方法を述べる．

## collation

MySQL には，collation (照合順序) と呼ばれる概念がある．
文字が一致するかどうかの判定のポリシーを定めるものである．

この演習環境では，原則として，
`utf8_bin` ないしは `utf8mb4_bin` という collation を使用している．
これらの collation では，異なる文字コードの文字を異なるものとして扱う．

`utf8_unicode_ci` ないしは `utf8mb4_unicode_ci` という collation を
用いると，広範囲な文字を同一視する．たとえば以下のものが同一視される．

* 英大文字と小文字．(`A` と `a` など)
* 全角文字と半角文字 (`0` と `０`，`A` と `Ａ` など)
* ひらがなとカタカナ (`あ` と `ア` など)

collation は，テーブル定義の際に指定することができる．

{% panel header="練習51-1" theme="info" %}

<a href="dbe2_3.sql" download>dbe2_3.sql</a> を MySQL にインポートして，
以下の問に答えよ．

(1) インポートすると，データベース dbe2 に，testcoll というテーブルが
追加される．インポートに用いたバックアップファイル dbe2_3.sql を
読み，各フィールドにcollation がどのように指定されているか確認せよ．

(2) phpMyAdmin の「構造」タブの内容を確認せよ．

(3) phpMyAdmin で次のSQL文を実行し，結果を確認せよ．

```sql
SELECT * FROM testcoll WHERE fld2 = 'ABC'
```

```sql
SELECT * FROM testcoll WHERE fld3 = 'ABC'
```

```sql
SELECT * FROM testcoll WHERE fld2 = 'あいうえお'
```

```sql
SELECT * FROM testcoll WHERE fld3 = 'あいうえお'
```

```sql
SELECT * FROM testcoll WHERE fld2 LIKE '12%'
```

```sql
SELECT * FROM testcoll WHERE fld3 LIKE '12%'
```

{% /panel %}

テーブル定義に collation を書き込んでしまうと，
原則的にその collation に従って検索が行われる．
これが望ましくないときには，検索時に collation を指定することもできる．

比較せよ:

```sql
SELECT * FROM testcoll WHERE fld2 = 'あいうえお'
```

```sql
SELECT * FROM testcoll WHERE fld2 collate utf8mb4_unicode_ci = 'あいうえお'
```

フィールドに指定されている charset によっては，collation がうまく
指定できない場合もある． convert 関数を介すと動作することもある:

```sql
-- SELECT * FROM testcoll WHERE fld1 collate utf8mb4_unicode_ci = 'あいうえお' -- これはエラー
SELECT * FROM testcoll WHERE convert(fld1 using utf8mb4) collate utf8mb4_unicode_ci = 'あいうえお'
```

## 異体字検索

MySQL が処理系としてサポートする文字の同一視は collation のみである．
それ以外の同一視を行いたい場合には，自分で工夫をする必要がある．

例として，データベースのテーブルに「田邉一郎」「田辺春子」
というデータを格納するとして，前方一致検索でユーザが
「田辺」，「田邉」，「田邊」のいずれを入力しても，この2件のデータが
ともに表示されるようにするには，どうしたら良いだろうか．

### 正規化

このようなときに有用な考え方に，__正規化__ (normalization) がある．
複数の表現がある際に，標準的な表現を1つ定め，比較対象をすべて
標準的な表現に変換した上で，単純文字列比較を行う，というものである．

上の問題の場合，3つの文字「辺」「邉」「邊」の中から，「辺」をその
代表と定める．そのうえで，正規化関数を，
代表以外の文字 (「邉」「邊」) を代表文字
に置き換えるものとして定義する．
テーブルに比較用のフィールドを一つ設け，そこには
正規化した文字列を格納しておく．

ユーザから検索文字列が送られてきたら，これも正規化した上で，
比較用のフィールドを用いて検索を行う．結果は，当然，正規化する前の
文字列を返さねばならない．

この方針で実装を行った[小さなサンプル](itaiji.zip) を示す．
(データベースも最新版を用いること)

{% panel header="練習51-2" theme="info" %}

(1) このサンプルでは，上述の「辺」の異体字にしか対応していない．
テーブルに登録されている「沢」の異体字や「斉」の異体字にも対応するように
せよ．( flask スクリプトと，テーブルに登録されているデータの双方を
修正する必要がある．)

(2)
実際にこのような検索を行うアプリケーションを構築する際には，
データは CSV ファイルで用意されることがよくある．
[original.csv](original.csv) のような CSV ファイルがあったとして，
これを， [altered.csv](altered.csv) のような 
CSV ファイルに書き換えたいと思うことになるであろう．
これを実現するPythonプログラムを作成せよ．
(ヒント: CSV ファイルを扱うには，
[csvモジュール](https://docs.python.org/ja/3/library/csv.html)
を使用するのが便利である)

(3)
http://kanji-database.sourceforge.net/variants/variants.txt
に定義されている異体字を同一視するように拡張せよ．



{% /panel %}






