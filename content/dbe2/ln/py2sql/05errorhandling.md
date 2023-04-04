+++
title = "エラー処理"
description = ""
weight = 5
alwaysopen = true
+++

エラー処理は，一般的に言って難しい話であり，
データベースがからむとより困難がある．ここでは必要最小限の記述に留める．

## 制約違反

文法エラーなどの問題は，開発時に十分デバッグを行うことによって
回避すべきである．しかし，利用者が与えるデータに起因する制約違反
など，実行時にエラーが起こることを回避できない場合もある．

たとえば，前節のfunc32 において，id として，既存のレコードが fld10 で
用いている値が指定された場合，(fld10 は主キーであるから) データベースは
エラーを報告する．このような場合，Python は，例外を投げてくる．

func32の仕様として，その場合にはなにもせずに，
呼び出し側にエラー処理を任せる，とする場合には，特に何もしなくても良い．
しかし，func32の仕様として，「挿入できた場合には True を，そうでない場合には
Falseを返す」を採用したいとすると，自分でエラー処理を書くことになる．
概ね，以下のようなコードになる．

```python
import datetime, sys

def func32A(id, x, y, s):
    sql = "INSERT INTO tbl1 VALUES (%s, %s, %s, %s, %s)"
    try:                             #(A)
        with connect_db() as cursor:
            cursor.execute(sql, [id, x, y, s, datetime.date.today()])
        return True
    except MySQLError as e:          #(B)
        print(str(e), file=sys.stderr)
        return False
```

エラーが起こりうるコードを，(A)のように，try ブロックの中に記述する．
try ブロックの直後に，(B)のように，except ブロックを置く．
except に引き続いて，捕捉したいエラーのクラス名を記述する．
今の場合には，MySQLError である．さらに，`as e` として，変数e を
エラーオブジェクトに束縛する．except ブロックでは，`str(e)` に
よって，エラーの詳細情報を表す文字列にアクセスできる．

Python におけるエラー処理の詳細は，
[公式ドキュメント](https://docs.python.org/ja/3/tutorial/errors.html)
を参照されたい．


{% exc seq="6-1" %}

練習4-1(2)の func35に，エラー処理を追加し，
制約違反によって挿入に失敗した場合には False を返し，
成功した場合には True を返すように改変せよ．

{% /exc %}


