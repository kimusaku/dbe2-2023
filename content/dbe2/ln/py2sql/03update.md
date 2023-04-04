+++
title = "データベースの更新"
description = ""
weight = 3
alwaysopen = true
+++

データベースの更新についても，Select 文と考え方はほとんど
変わらない．

## UPDATE 文

次の関数 func31(id, s) は，tbl1 で，fld10 の値が id である
レコードのfld13 の値を s に変更するものである．

```python
def func31(id, s):
    with connect_db() as cursor:
        sql = "UPDATE tbl1 SET fld13 = %s WHERE fld10 = %s"
        cursor.execute(sql, [s, id])
    return
```

## INSERT 文

次の関数 func32(id, x, y, s) は，
tbl1 に新たなレコードを追加するものである．追加されるレコードの
fld10, fld11, fld12, fld13 の値は，それぞれ id, x, y, s であり，
fld14には，今日の日付が設定される．

```python
import datetime

def func32(id, x, y, s):
    with connect_db() as cursor:
        sql = "INSERT INTO tbl1 VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, [id, x, y, s, datetime.date.today()])
    return
```

## DELETE 文

次の関数 func33(id) は，tbl1 の fld10 の値が id であるレコードを
削除するものである．

```python
def func33(id):
    with connect_db() as cursor:
        sql = "DELETE FROM tbl1 WHERE fld10 = %s"
        cursor.execute(sql, [id])
    return
```

{% exc seq="4-1" %}

tbl2のデータを更新する次の関数を書け．

(1) func34(id, x): fld21 の値が id であるレコードの fld23 の値を x に変更する．

(2) func35(id2, id1, x, s):
fld21, fld22, fld23, fld24 の値がそれぞれ，id2, id1, x, s であるような
レコードを挿入する．

(3) func36(x):
fld23 の値が x 以下であるレコードを削除する．

{% /exc %}


