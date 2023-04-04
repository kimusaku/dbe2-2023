+++
title = "mysqlclient"
description = ""
weight = 1
alwaysopen = true
+++


## mysqlclient のインストール

省略．第1回講義資料 (pptx) 参照．

## Jupyter Notebook のインストールと実行．

省略．
インストールについては，第1回講義資料 (pptx) 参照．
実行方法については，「データベース各論I」第1回講義資料を参照．

講義資料のこの章では，Jupyter Notebook を用いて，Python プログラムから
MySQLデータベースにアクセスする．

## 実行

* Xampp コントロールパネルから，MySQLサーバを起動しておくこと．
* <a href="dbe2_3.sql" download>dbe2_3.sql</a> を，
  MySQL にインポートしておくこと．これによって，dbe2 というデータベースが
  作成される．


## テンプレート

Jupyter Notebook では，以下を常に最初に実行しておく必要がある．

```python
import MySQLdb
from MySQLdb.cursors import Cursor
from MySQLdb._exceptions import MySQLError

def connect_db():
    conn = MySQLdb.connect(
          host="localhost",
          user="root",
          passwd="",
          db="dbe2",
          charset='utf8',
          autocommit=True,
    )
    return conn.cursor(Cursor)
```

基本的にこのままコピーペーストすれば良いが，
以下の場合には，適宜変更を行うこと．

* MySQLサーバのデータベース`dbe2`に接続するようになっている．
  他のデータベースを使うときには，パラメタ`db`の値を変更する．
* user, passwd パラメタの値は，必要があれば変更する．

これを実行すると，connect_db という関数が定義される．
定義されただけで実行したわけではないことに注意すること．


## select文の実行

データベース dbe2 の中にある tbl1 にアクセスして，
その内容を画面に表示する関数 func21() を書いてみよう．

```python
def func21():                            # 関数 func21 の定義
    with connect_db() as cursor:         # DBに接続して，cursor を得る．
        sql = "SELECT * FROM tbl1"       # 変数sqlにSQL文を設定する．
        cursor.execute(sql, [])          # 変数sqlの内容を実行する．
        for c in cursor:                 # 実行結果は，cursor を for 文で回して
            print(c)                     # 取得できる．
```

これも，func21 という関数を定義しただけで，SQL文を実行したわけでは
ないことに注意する．実行するには，この関数を呼び出せば良い．

```python
func21()
```

すると，以下の出力結果が得られる．

```none
('d01', 100, 20, 'abc', datetime.date(2018, 3, 5))
('d02', 80, -35, 'xyy', datetime.date(2015, 4, 1))
('d03', 59, 96, 'xyy', datetime.date(2018, 12, 4))
('d04', 60, -15, 'abc', datetime.date(2017, 10, 3))
('d05', 40, 31, 'pqr', datetime.date(2015, 10, 2))
('d06', 39, 128, 'efffs', datetime.date(2017, 12, 31))
('d07', 81, 0, 'abc', datetime.date(2018, 1, 1))
```

phpMyAdmin において，データベース dbe2 のテーブル tbl1 を表示して，
上の結果を見比べてみよ．

* func21() の for 文では，変数 c に，tbl1 の各レコードが順に設定される．
* 各レコードは，5つ組で構成されている．
  これは，tbl1 が，5つのフィールドからなることに対応している．
* 各5つ組の最初のデータはフィールド fld10 の値，
  次のデータはフィールド fld11 の値，... である．
* フィールド fld10, fld13 の型は，各々 char(3) とvarchar(100) である．
  これらに格納された値は，Python プログラムでは，文字列として取得されて
  いる．
* フィールド fld11, fld12 の型は，int である．
  これらに格納された値は，Python プログラムでは，整数として取得されて
  いる．
* フィールド fld14 の型は，date である．
  これに格納された値は，Python プログラムでは，
  datetime モジュールの date オブジェクトとして
  取得されている．

date オブジェクトについては，ここでは説明しない．
興味のある者は (興味を持ってほしい)，
インターネット上に多数のリソースがあるので調査すること．
(`Python datetime` で検索する)


{% exc seq="2-1" %}

func21 で，変数 sql に設定するSELECT文を，以下のように変更してみよ．
実行する前に実行結果を予想せよ．予想通りの結果が得られたか?


```sql
-- (1) 
SELECT * FROM tbl1 WHERE fld14 <= '2017-10-03'

-- (2) 
SELECT fld10, fld12 FROM tbl1

-- (3)
SELECT fld10, fld14, fld24
  FROM tbl1
  JOIN tbl2 ON tbl1.fld10 = tbl2.fld22
  WHERE fld23 < 5000
```

注: (3)のように文字列が長くなるときには，
Python のコード上も改行をしてよい．
その際には，`'～'` や `"～"` ではなく，`'''～'''` や `"""～"""` を用いる．
後者は，複数行の文字列に対応している．

{% /exc %}


{% exc seq="2-2" %}

Python では，文字列を囲う引用符には，`'～'` と `"～"` があり，
どちらも同じ機能を持つ．func21() の `sql = "SELECT * FROM tbl11"` という行で，
`"` を `'` に変更しても，問題なく動作する．
しかし，上の練習2-1 (1) では，`"` を `'` に変更すると，エラーが発生する．
この理由を説明せよ．

{% /exc %}

## 値の取得

実際のアプリケーションでは，上の func21() のように，
画面に結果を表示したいということは，
ほとんどない．
このように表示するのは，プログラムをデバッグするときくらいである．

ほとんどの場合，DBの値を取得する関数を書くことになる．

例として，fld10 の値を与えて，対応する fld13 の値を得る関数を書いてみよう．
具体的には，func22(s) を，文字列 s を引数として，
fld10 の値が s であるレコードの fld13 の値を返す関数として定義する．
下に示す `func22(s)` はその例であり，
たとえば，`func22('d05')` は，`'pqr'` を返す．

```python
def func22(s):
    with connect_db() as cursor:
        sql = "SELECT * FROM tbl1"       # (A)
        cursor.execute(sql, [])
        for c in cursor:
            if c[0] == s:                # (B)
                return c[3]              # (C)
```

この func22 は func21 とほとんど同じコードであるが，(B), (C) のみが
異なる．前述のように，変数 c には5つ組が格納されている．
例えば先頭レコードでは，その内容は以下のようであった．

```
('d01', 100, 20, 'abc', datetime.date(2018, 3, 5))
```

この場合，`c[0]` が，最初の値である `'d01'` を指し，
`c[1]` が 100 を意味し，..., `c[4]` で `datetime.date(2018, 3, 5)`
が参照できる．従って，(B), (C) のようなコードで目的が達せられる．

しかし，このコードはあまり望ましいものではない．
データベースからPythonに余計なデータをたくさん送っているからである．
この例では送られるデータはたかだか10件くらいだから，
データ量は無視できるほど小さい．しかし，
実際にアプリケーションを運用するときには，
データベースのレコードの件数が何百万にも達することが，しばしばある．
必要なデータはたった1件であるとき，
何百万ものデータを転送するというのは，いかにも無駄である．
適切な SQL 文を指定することによって，
合致するデータをできる限り減らすべきである．

今の場合，fld10 と fld13 にしか興味が無いのであるから，
これらのフィールドの値のみを取得するようにすべきである．

```python
def func23(s):
    with connect_db() as cursor:
        sql = "SELECT fld10, fld13 FROM tbl1"       # (A)
        cursor.execute(sql, [])
        for c in cursor:
            if c[0] == s:                # (B)
                return c[1]              # (C)
```

(A)を書き換えたことによって，変数 c には，5つ組ではなく，
2つ組が格納されるようになった．例えば先頭レコードについては，次のようである．

```
('d01', 'abc')
```

したがって，(C) においては，先の `c[3]` ではなく，
`c[1]` をとらなくてはならない．

func23 は func22 よりは良くなったが，まだ大量に無駄がある．
(A) で，WHERE 句を加えて，引数 s に合致するレコードのみを取得する
ようにすべきである．次の節でそれを検討する．


{% exc seq="2-3" %}

(1)
整数 n を引数に取り，tbl2 において fld21 の値が n であるレコードの
fld24 の値を取得する関数を書け．

(2)
整数 n を引数に取り，tbl1 において，fld11 の値が n 以下であるレコードの
数を返す関数を書け．

(3)
文字列 s を引数に取り，tbl1 と tbl2 を fld10 と fld22 で結合した表に
おいて，fld10 の値が s であるレコードの fld21 の値のリストを返す関数を
書け．

{% /exc %}

