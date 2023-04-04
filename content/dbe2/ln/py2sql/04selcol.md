+++
title = "フィールド名などの選択"
description = ""
weight = 4
alwaysopen = true
+++

プレースホルダーは，文字列，数値，日付などの値の位置を
指示するのに用いることができるが，
フィールド名やテーブル名などの位置で指定することはできない．

たとえば，関数 func51(fldname, id, x) として，
tbl1 の整数型のフィールド名 fldname，文字列 id, 整数 x を引数に取り，
fld10 の値が id であるレコードの，指定されたフィールドの値を x に
変更するような関数を書きたいとしよう．次のように書くことはできない．

```python
def func51(fldname, id, x):
    with connect_db() as cursor:
        sql = "UPDATE tbl1 SET %s = %s WHERE fld10 = %s"
        cursor.execute(sql, [fldname, x, id])
    return
```

値と異なり，フィールド名やテーブル名は少数しか候補がないので，
このような場合には，プログラム中で明示的に指定すれば良い．
例えば，tbl1 における整数型のフィールドというのは，fld11 と fld12 しか
無いのであるから，以下のように書くことができる．

```python
def func51(fldname, id, x):
    with connect_db() as cursor:
        if fldname == 'fld11':
            sql = "UPDATE tbl1 SET fld11 = %s WHERE fld10 = %s"
        elif fldname == 'fld12':
            sql = "UPDATE tbl1 SET fld12 = %s WHERE fld10 = %s"
        else:
            print(f'{fldname} というフィールドはありません．')
            return
        cursor.execute(sql, [x, id])
    return
```

もしくは，次のように書いても良い．

```python
def func51(fldname, id, x):
    with connect_db() as cursor:
        if fldname in ['fld11', 'fld12']:
            sql = f"UPDATE tbl1 SET " + fldname + " = %s WHERE fld10 = %s"
        else:
            print(f'{fldname} というフィールドはありません．')
            return
        cursor.execute(sql, [x, id])
    return
```

先に，引数に渡された文字列を SQL 文の一部として用いてはいけない，と
述べたが，この場合は例外で，引数の値が特定の2つの (自分で把握している)
文字列のいずれかであることを確認しているので，問題ないのである
(とはいえ，事情がよくわかるまで，このようなコードを書くのは控えるのが
無難である)．


